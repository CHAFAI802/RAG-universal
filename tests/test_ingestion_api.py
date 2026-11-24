import asyncio
import json
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID

import pytest
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.base import Base
from app.core.config import settings
from app.core.dependencies import get_db
from app.main import app
from app.modules.ingestion.dependencies import get_authenticated_user
from app.modules.credentials.models import CredentialOwnerType
from app.modules.credentials.services import CredentialService
from app.modules.identity.models import Identity, IdentityStatus, IdentityType
from app.modules.ingestion.models import Ingestion, IngestionStatus
from app.modules.ingestion.services import (
    IngestionReceiveError,
    IngestionService,
)
from app.modules.users.models import User, UserStatus
from starlette.requests import ClientDisconnect


USER_PASSWORD = "IngestionUserPassword-2026!"


@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def account(test_engine):
    with Session(test_engine) as db:
        identity = Identity(
            identity_type=IdentityType.HUMAN,
            display_name="Ingestion test identity",
        )
        db.add(identity)
        db.flush()
        user = User(identity_id=identity.identity_id)
        db.add(user)
        db.flush()
        credential = CredentialService(db).create_username_password_credential(
            identity_id=identity.identity_id,
            username="ingestion-user",
            password=USER_PASSWORD,
            owner_type=CredentialOwnerType.USER,
            user_id=user.user_id,
        )
        db.commit()
        return identity.identity_id, user.user_id, credential.credential_id


@pytest.fixture
def client(test_engine, monkeypatch, tmp_path):
    monkeypatch.setattr(settings, "AUTH_TOKEN_SECRET", "test-only-secret-" + "x" * 32)
    monkeypatch.setattr(settings, "AUTH_TOKEN_TTL_SECONDS", 900)
    monkeypatch.setattr(
        settings,
        "INGESTION_TEMP_STORAGE_PATH",
        str(tmp_path / "temporary"),
    )
    monkeypatch.setattr(settings, "INGESTION_MAX_FILE_SIZE_BYTES", 16)
    monkeypatch.setattr(
        settings,
        "INGESTION_ALLOWED_EXTENSIONS",
        "txt,json,csv,pdf,docx,odt,xml",
    )

    def override_get_db():
        with Session(test_engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def user_token(client, account):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "ingestion-user", "password": USER_PASSWORD},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def _headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _create_ingestion(client, token, *, filename="source.txt", **extra):
    payload = {
        "document_name": filename,
        "source_type": "UPLOAD",
        **extra,
    }
    return client.post(
        "/api/v1/ingestions",
        json=payload,
        headers=_headers(token),
    )


def test_ingestion_requires_a_user_bearer_token(client, account):
    response = client.post(
        "/api/v1/ingestions",
        json={"document_name": "source.txt"},
    )
    invalid = client.post(
        "/api/v1/ingestions",
        json={"document_name": "source.txt"},
        headers=_headers("invalid-token"),
    )

    assert response.status_code == 401
    assert invalid.status_code == 401


def test_identity_admin_token_cannot_ingest(client, test_engine):
    with Session(test_engine) as db:
        identity = Identity(
            identity_type=IdentityType.HUMAN,
            display_name="Admin identity",
        )
        db.add(identity)
        db.flush()
        CredentialService(db).create_username_password_credential(
            identity_id=identity.identity_id,
            username="ingestion-admin",
            password=USER_PASSWORD,
        )
        db.commit()

    token = client.post(
        "/api/v1/auth/login",
        json={"username": "ingestion-admin", "password": USER_PASSWORD},
    ).json()["access_token"]
    response = _create_ingestion(client, token)

    assert response.status_code == 403


def test_expired_user_token_is_rejected(client, account):
    from datetime import datetime, timedelta, timezone

    import jwt

    from app.modules.auth.tokens import TOKEN_ALGORITHM

    valid_token = client.post(
        "/api/v1/auth/login",
        json={"username": "ingestion-user", "password": USER_PASSWORD},
    ).json()["access_token"]
    claims = jwt.decode(
        valid_token,
        options={"verify_signature": False},
        algorithms=[TOKEN_ALGORITHM],
    )
    claims["iat"] = datetime.now(timezone.utc) - timedelta(minutes=2)
    claims["exp"] = datetime.now(timezone.utc) - timedelta(minutes=1)
    expired = jwt.encode(
        claims,
        settings.AUTH_TOKEN_SECRET,
        algorithm=TOKEN_ALGORITHM,
    )

    response = _create_ingestion(client, expired)

    assert response.status_code == 401


def test_disabled_identity_or_user_cannot_ingest(
    client,
    account,
    test_engine,
    user_token,
):
    with Session(test_engine) as db:
        db.get(User, account[1]).status = UserStatus.DISABLED
        db.commit()

    response = _create_ingestion(client, user_token)
    assert response.status_code == 401

    with Session(test_engine) as db:
        db.get(User, account[1]).status = UserStatus.ACTIVE
        db.get(Identity, account[0]).status = IdentityStatus.DISABLED
        db.commit()

    response = _create_ingestion(client, user_token)
    assert response.status_code == 401


@pytest.mark.parametrize("owner_field", ["identity_id", "user_id"])
def test_request_cannot_choose_ingestion_owner(
    client,
    account,
    user_token,
    owner_field,
):
    response = _create_ingestion(
        client,
        user_token,
        **{owner_field: str(UUID(int=0))},
    )

    assert response.status_code == 422


def test_user_receives_and_retrieves_own_original(client, account, user_token, test_engine):
    created = _create_ingestion(client, user_token)
    assert created.status_code == 201
    ingestion_id = created.json()["ingestion_id"]
    assert created.json()["status"] == "PENDING"
    assert created.json()["identity_id"] == str(account[0])
    assert created.json()["user_id"] == str(account[1])

    received = client.put(
        f"/api/v1/ingestions/{ingestion_id}/source",
        content=b"original text",
        headers=_headers(user_token),
    )

    assert received.status_code == 200
    metadata = received.json()
    assert metadata["status"] == "RECEIVED"
    assert metadata["size_bytes"] == len(b"original text")
    assert metadata["content_type"] == "text/plain"
    assert metadata["temporary_location"]

    downloaded = client.get(
        f"/api/v1/ingestions/{ingestion_id}/source",
        headers=_headers(user_token),
    )
    assert downloaded.status_code == 200
    assert downloaded.content == b"original text"

    with Session(test_engine) as db:
        ingestion = db.get(Ingestion, UUID(ingestion_id))
        assert ingestion.status == IngestionStatus.RECEIVED
        stored_path = Path(settings.INGESTION_TEMP_STORAGE_PATH) / ingestion.storage_path
        assert stored_path.read_bytes() == b"original text"


def test_text_ingestion_is_stored_as_an_original(client, user_token):
    response = client.post(
        "/api/v1/ingestions/text?document_name=note.txt",
        content="texte source".encode("utf-8"),
        headers=_headers(user_token),
    )

    assert response.status_code == 201
    assert response.json()["source_type"] == "TEXT"
    assert response.json()["status"] == "RECEIVED"
    assert response.json()["size_bytes"] == len("texte source".encode("utf-8"))
    assert response.json()["temporary_location"]


def test_local_folder_metadata_stays_relative_to_the_selected_folder(
    client,
    user_token,
):
    response = _create_ingestion(
        client,
        user_token,
        filename="report.txt",
        source_type="LOCAL_FOLDER",
        source_identifier="chosen-folder/subfolder/report.txt",
    )

    assert response.status_code == 201
    assert response.json()["source_identifier"] == (
        "chosen-folder/subfolder/report.txt"
    )
    assert "/home/" not in response.json()["source_identifier"]


def test_browser_folder_client_requires_confirmation_and_uses_scoped_picker(client):
    response = client.get("/api/v1/ingestions/folder-client")

    assert response.status_code == 200
    assert "showDirectoryPicker" in response.text
    assert "root.resolve(entry)" in response.text
    assert "Je confirme l'envoi" in response.text
    assert "localStorage" not in response.text
    assert response.headers["content-security-policy"]


def test_browser_folder_client_exposes_chromium_and_firefox_selection(client):
    text = client.get("/api/v1/ingestions/folder-client").text

    assert "showDirectoryPicker" in text
    assert 'id="folder-input"' in text
    assert "webkitdirectory" in text
    assert "multiple" in text
    assert 'document.querySelector("#choose")' in text
    assert "supportsDirectoryPicker" in text
    assert "folderInput.click()" in text


def test_browser_folder_client_keeps_chromium_root_resolution(client):
    text = client.get("/api/v1/ingestions/folder-client").text

    assert "await root.resolve(entry)" in text
    assert "resolvedPath === null" in text
    assert "entry.getFile()" in text


def test_browser_folder_client_uses_webkit_relative_path_for_firefox(client):
    text = client.get("/api/v1/ingestions/folder-client").text

    assert "file.webkitRelativePath" in text
    assert "collectFirefoxSelection(folderInput.files)" in text
    assert "selectionMode = \"firefox\"" in text


def test_browser_folder_client_validates_relative_paths(client):
    text = client.get("/api/v1/ingestions/folder-client").text

    assert "function validateRelativePath" in text
    assert 'rawPath.startsWith("/")' in text
    assert 'rawPath.endsWith("/")' in text
    assert 'rawPath.startsWith("\\\\")' in text
    assert 'rawPath.includes("\\\\")' in text
    assert 'rawPath.includes("//")' in text
    assert 'segment === ""' in text
    assert 'segment === "."' in text
    assert 'segment === ".."' in text
    assert "String.fromCharCode(0)" in text
    assert "function isHiddenPath" in text
    assert 'startsWith(".")' in text


def test_browser_folder_client_confirms_before_reading_any_content(client):
    text = client.get("/api/v1/ingestions/folder-client").text

    assert text.count("getFile(") == 1
    assert text.count("collectFiles(") == 3
    assert "if (!accessToken || !consent.checked || busy) return;" in text
    assert "if (!hasSelection()) return;" in text
    upload_body = text.split('uploadButton.addEventListener("click"', 1)[1]
    assert "collectFirefoxSelection" not in upload_body
    assert "await collectFiles(" in upload_body


def test_browser_folder_client_uses_same_endpoints_for_both_methods(client):
    text = client.get("/api/v1/ingestions/folder-client").text

    assert text.count('fetch("/api/v1/ingestions",') == 1
    assert text.count('"/api/v1/ingestions/" + metadata.ingestion_id + "/source"') == 1
    assert text.count('source_type: "LOCAL_FOLDER"') == 1
    assert text.count("source_identifier: item.relativePath") == 1


def test_browser_folder_client_resets_selection_after_transfer(client):
    text = client.get("/api/v1/ingestions/folder-client").text

    assert "function resetSelection()" in text
    assert text.count("resetSelection();") == 4
    finally_block = text.split("} finally {", 1)[1]
    assert "busy = false;" in finally_block
    assert "resetSelection();" in finally_block
    assert 'folderInput.value = "";' in text
    assert "consent.checked = false;" in text
    assert "selectedDirectory = null;" in text
    assert "firefoxFiles = [];" in text


FOLDER_CLIENT_NODE_STUBS = """
const __elements = new Map();
function __element(selector) {
  if (!__elements.has(selector)) {
    __elements.set(selector, {
      selector,
      textContent: "",
      value: "",
      checked: false,
      hidden: false,
      disabled: false,
      addEventListener() {},
      click() {}
    });
  }
  return __elements.get(selector);
}
globalThis.window = {};
globalThis.document = {querySelector: __element};
"""


def _folder_client_javascript(client):
    html = client.get("/api/v1/ingestions/folder-client").text
    return html.split("<script>", 1)[1].split("</script>", 1)[0]


def _run_folder_client_javascript(client, tmp_path, body):
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is required to exercise the browser folder client")
    harness = tmp_path / "folder_client_harness.js"
    harness.write_text(
        FOLDER_CLIENT_NODE_STUBS
        + _folder_client_javascript(client)
        + "\n"
        + body,
        encoding="utf-8",
    )
    completed = subprocess.run(
        [node, str(harness)], capture_output=True, text=True
    )
    assert completed.returncode == 0, completed.stderr
    return json.loads(completed.stdout)


def _firefox_selection_body(entries):
    return (
        "const selection = collectFirefoxSelection("
        f"{json.dumps(entries)});\n"
        'console.log(JSON.stringify({'
        '"files": selection.files.map(item => item.relativePath),'
        '"rejected": selection.rejected}));\n'
    )


def _chromium_collection_body(tree):
    return (
        "function fileEntry(name) {\n"
        '  return {kind: "file", name, async getFile() { return {name}; }};\n'
        "}\n"
        "function dirEntry(name, children) {\n"
        '  return {kind: "directory", name, async *entries() {\n'
        "    for (const child of children) yield [child.name, child];\n"
        "  }};\n"
        "}\n"
        "(async () => {\n"
        "  const root = "
        + tree
        + ";\n"
        '  root.resolve = async entry => "resolved/" + entry.name;\n'
        "  const files = [];\n"
        "  const rejected = [];\n"
        '  await collectFiles(root, root, "", files, rejected);\n'
        "  console.log(JSON.stringify({\n"
        "    files: files.map(item => item.relativePath).sort(),\n"
        "    rejected\n"
        "  }));\n"
        "})();\n"
    )


def test_firefox_folder_client_strips_root_for_a_file_at_the_root(client, tmp_path):
    data = _run_folder_client_javascript(
        client,
        tmp_path,
        _firefox_selection_body(
            [
                {
                    "name": "document1.txt",
                    "webkitRelativePath": "root/document1.txt",
                }
            ]
        ),
    )

    assert data["files"] == ["document1.txt"]
    assert data["rejected"] == []


def test_firefox_folder_client_strips_root_for_a_subfolder_file(client, tmp_path):
    data = _run_folder_client_javascript(
        client,
        tmp_path,
        _firefox_selection_body(
            [
                {
                    "name": "guide.txt",
                    "webkitRelativePath": "root/docs/guide.txt",
                }
            ]
        ),
    )

    assert data["files"] == ["docs/guide.txt"]
    assert data["rejected"] == []


def test_firefox_folder_client_keeps_nested_relative_paths(client, tmp_path):
    data = _run_folder_client_javascript(
        client,
        tmp_path,
        _firefox_selection_body(
            [
                {
                    "name": "c.txt",
                    "webkitRelativePath": "root/a/b/c.txt",
                }
            ]
        ),
    )

    assert data["files"] == ["a/b/c.txt"]
    assert data["rejected"] == []


def test_firefox_folder_client_rejects_inconsistent_root_folders(client, tmp_path):
    data = _run_folder_client_javascript(
        client,
        tmp_path,
        _firefox_selection_body(
            [
                {"name": "one.txt", "webkitRelativePath": "root-a/one.txt"},
                {"name": "two.txt", "webkitRelativePath": "root-b/two.txt"},
                {"name": "three.txt", "webkitRelativePath": "root-a/three.txt"},
            ]
        ),
    )

    assert data["files"] == ["one.txt", "three.txt"]
    assert len(data["rejected"]) == 1
    assert "root-b/two.txt" in data["rejected"][0]
    assert "dossier racine différent" in data["rejected"][0]


def test_firefox_folder_client_rejects_absolute_and_parent_paths(client, tmp_path):
    data = _run_folder_client_javascript(
        client,
        tmp_path,
        _firefox_selection_body(
            [
                {"name": "passwd", "webkitRelativePath": "/etc/passwd"},
                {"name": "win.ini", "webkitRelativePath": "C:/Windows/win.ini"},
                {"name": "secret.txt", "webkitRelativePath": "root/../secret.txt"},
                {"name": "b.txt", "webkitRelativePath": "root/a/../../b.txt"},
                {"name": "outside.txt", "webkitRelativePath": "../outside.txt"},
            ]
        ),
    )

    assert data["files"] == []
    assert len(data["rejected"]) == 5


def test_firefox_folder_client_rejects_files_in_hidden_folders(client, tmp_path):
    data = _run_folder_client_javascript(
        client,
        tmp_path,
        _firefox_selection_body(
            [
                {"name": "config", "webkitRelativePath": "root/.git/config"},
                {"name": ".env", "webkitRelativePath": "root/.env"},
                {"name": ".env", "webkitRelativePath": "root/docs/.env"},
                {"name": "readme.txt", "webkitRelativePath": "root/docs/readme.txt"},
            ]
        ),
    )

    assert data["files"] == ["docs/readme.txt"]
    assert len(data["rejected"]) == 3


def test_chromium_folder_client_does_not_walk_hidden_folders(client, tmp_path):
    tree = (
        'dirEntry("root", ['
        'fileEntry("document1.txt"), '
        'dirEntry("docs", [fileEntry("guide.txt"), fileEntry(".env")]), '
        'dirEntry(".git", [fileEntry("config")]), '
        'dirEntry("a", [dirEntry("b", [fileEntry("c.txt")])])'
        "])"
    )
    data = _run_folder_client_javascript(
        client, tmp_path, _chromium_collection_body(tree)
    )

    assert data["files"] == ["a/b/c.txt", "docs/guide.txt", "document1.txt"]
    assert any(item.startswith(".git :") for item in data["rejected"])
    assert not any(".git/config" in item for item in data["rejected"])
    assert any(item.startswith("docs/.env :") for item in data["rejected"])


def test_firefox_and_chromium_produce_identical_relative_paths(client, tmp_path):
    firefox_body = (
        "const selection = collectFirefoxSelection("
        + json.dumps(
            [
                {
                    "name": "document1.txt",
                    "webkitRelativePath": "root/document1.txt",
                },
                {
                    "name": "guide.txt",
                    "webkitRelativePath": "root/docs/guide.txt",
                },
                {"name": "c.txt", "webkitRelativePath": "root/a/b/c.txt"},
            ]
        )
        + ");\n"
        "const firefoxPaths = selection.files"
        ".map(item => item.relativePath).sort();\n"
        "function fileEntry(name) {\n"
        '  return {kind: "file", name, async getFile() { return {name}; }};\n'
        "}\n"
        "function dirEntry(name, children) {\n"
        '  return {kind: "directory", name, async *entries() {\n'
        "    for (const child of children) yield [child.name, child];\n"
        "  }};\n"
        "}\n"
        "(async () => {\n"
        '  const root = dirEntry("root", [fileEntry("document1.txt"), '
        'dirEntry("docs", [fileEntry("guide.txt")]), '
        'dirEntry("a", [dirEntry("b", [fileEntry("c.txt")])])]);\n'
        '  root.resolve = async entry => "resolved/" + entry.name;\n'
        "  const files = [];\n"
        "  const rejected = [];\n"
        '  await collectFiles(root, root, "", files, rejected);\n'
        "  console.log(JSON.stringify({\n"
        "    firefox: firefoxPaths,\n"
        "    chromium: files.map(item => item.relativePath).sort(),\n"
        "    rejected\n"
        "  }));\n"
        "})();\n"
    )
    data = _run_folder_client_javascript(client, tmp_path, firefox_body)

    assert data["chromium"] == data["firefox"]
    assert data["firefox"] == ["a/b/c.txt", "docs/guide.txt", "document1.txt"]
    assert data["rejected"] == []


def test_failed_empty_and_oversized_receipts_are_tracked(
    client,
    user_token,
    test_engine,
):
    for body, expected_status, expected_code in (
        (b"", 422, "empty_file"),
        (b"x" * 17, 413, "file_too_large"),
    ):
        created = _create_ingestion(client, user_token)
        ingestion_id = created.json()["ingestion_id"]
        response = client.put(
            f"/api/v1/ingestions/{ingestion_id}/source",
            content=body,
            headers=_headers(user_token),
        )
        assert response.status_code == expected_status
        assert response.headers["x-ingestion-error-code"] == expected_code

        with Session(test_engine) as db:
            ingestion = db.get(Ingestion, UUID(ingestion_id))
            assert ingestion.status == IngestionStatus.FAILED
            assert ingestion.error_code == expected_code


def test_bad_files_and_dangerous_names_are_refused(client, user_token):
    dangerous = _create_ingestion(
        client,
        user_token,
        filename="../private.txt",
    )
    unsupported = _create_ingestion(
        client,
        user_token,
        filename="payload.exe",
    )

    assert dangerous.status_code == 422
    assert unsupported.status_code == 415

    created = _create_ingestion(
        client,
        user_token,
        filename="broken.json",
    )
    response = client.put(
        f"/api/v1/ingestions/{created.json()['ingestion_id']}/source",
        content=b"{broken",
        headers=_headers(user_token),
    )

    assert response.status_code == 422
    assert response.headers["x-ingestion-error-code"] == "invalid_content"


def test_duplicate_names_never_overwrite_an_original(client, user_token):
    first = _create_ingestion(client, user_token).json()["ingestion_id"]
    second = _create_ingestion(client, user_token).json()["ingestion_id"]

    for ingestion_id, content in ((first, b"first"), (second, b"second")):
        response = client.put(
            f"/api/v1/ingestions/{ingestion_id}/source",
            content=content,
            headers=_headers(user_token),
        )
        assert response.status_code == 200

    first_source = client.get(
        f"/api/v1/ingestions/{first}/source",
        headers=_headers(user_token),
    )
    second_source = client.get(
        f"/api/v1/ingestions/{second}/source",
        headers=_headers(user_token),
    )

    assert first_source.content == b"first"
    assert second_source.content == b"second"


def test_ingestion_listing_and_download_are_isolated_between_users(
    client,
    account,
    user_token,
    test_engine,
):
    created = _create_ingestion(client, user_token).json()
    source_response = client.put(
        f"/api/v1/ingestions/{created['ingestion_id']}/source",
        content=b"private",
        headers=_headers(user_token),
    )
    assert source_response.status_code == 200

    with Session(test_engine) as db:
        other_identity = Identity(
            identity_type=IdentityType.HUMAN,
            display_name="Other identity",
        )
        db.add(other_identity)
        db.flush()
        other_user = User(identity_id=other_identity.identity_id)
        db.add(other_user)
        db.flush()
        CredentialService(db).create_username_password_credential(
            identity_id=other_identity.identity_id,
            username="other-ingestion-user",
            password=USER_PASSWORD,
            owner_type=CredentialOwnerType.USER,
            user_id=other_user.user_id,
        )
        db.commit()

    other_token = client.post(
        "/api/v1/auth/login",
        json={"username": "other-ingestion-user", "password": USER_PASSWORD},
    ).json()["access_token"]
    hidden = client.get(
        f"/api/v1/ingestions/{created['ingestion_id']}",
        headers=_headers(other_token),
    )
    hidden_source = client.get(
        f"/api/v1/ingestions/{created['ingestion_id']}/source",
        headers=_headers(other_token),
    )
    listing = client.get("/api/v1/ingestions", headers=_headers(other_token))

    assert hidden.status_code == 404
    assert hidden_source.status_code == 404
    assert listing.json() == []


def test_same_user_cannot_receive_an_ingestion_twice(client, user_token):
    created = _create_ingestion(client, user_token).json()
    path = f"/api/v1/ingestions/{created['ingestion_id']}/source"

    first = client.put(path, content=b"first", headers=_headers(user_token))
    duplicate = client.put(path, content=b"replacement", headers=_headers(user_token))

    assert first.status_code == 200
    assert duplicate.status_code == 409


def test_interrupted_transfer_is_recorded_as_failed(
    client,
    account,
    user_token,
    test_engine,
):
    created = _create_ingestion(client, user_token).json()

    async def interrupted_chunks():
        yield b"partial"
        raise ClientDisconnect()

    with Session(test_engine) as db:
        authenticated_user = get_authenticated_user(
            HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials=user_token,
            ),
            db,
        )
        service = IngestionService(db)
        with pytest.raises(IngestionReceiveError) as error:
            asyncio.run(
                service.receive_stream(
                    ingestion_id=UUID(created["ingestion_id"]),
                    authenticated_user=authenticated_user,
                    chunks=interrupted_chunks(),
                )
            )

        assert error.value.code == "transfer_interrupted"
        ingestion = db.get(Ingestion, UUID(created["ingestion_id"]))
        assert ingestion.status == IngestionStatus.FAILED
        assert ingestion.error_code == "transfer_interrupted"


def test_cleanup_marks_stale_metadata_without_deleting_received_sources(
    client,
    user_token,
    test_engine,
    monkeypatch,
):
    monkeypatch.setattr(settings, "INGESTION_ABANDONED_FAILED_TTL_SECONDS", 60)
    abandoned = _create_ingestion(client, user_token).json()
    received = _create_ingestion(client, user_token).json()
    response = client.put(
        f"/api/v1/ingestions/{received['ingestion_id']}/source",
        content=b"keep original",
        headers=_headers(user_token),
    )
    assert response.status_code == 200

    with Session(test_engine) as db:
        old_time = datetime.now(timezone.utc) - timedelta(minutes=2)
        db.get(Ingestion, UUID(abandoned["ingestion_id"])).updated_at = old_time
        db.commit()
        service = IngestionService(db)
        assert service.mark_abandoned_ingestions() == 1

        abandoned_row = db.get(Ingestion, UUID(abandoned["ingestion_id"]))
        received_row = db.get(Ingestion, UUID(received["ingestion_id"]))
        assert abandoned_row.status == IngestionStatus.FAILED
        assert abandoned_row.error_code == "abandoned_transfer"
        assert received_row.status == IngestionStatus.RECEIVED
        original_path = (
            Path(settings.INGESTION_TEMP_STORAGE_PATH) / received_row.storage_path
        )
        assert original_path.read_bytes() == b"keep original"
