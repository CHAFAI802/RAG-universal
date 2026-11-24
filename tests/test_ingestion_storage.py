import io
import os
import stat
import time
from uuid import uuid4

import pytest

from app.modules.ingestion.file_validation import (
    ContentValidationError,
    FilenameRejectedError,
    UnsupportedExtensionError,
)
from app.modules.ingestion.storage import (
    EmptyFileError,
    FileTooLargeError,
    StoragePathError,
    TemporaryStorage,
)


@pytest.fixture
def storage(tmp_path):
    return TemporaryStorage(
        tmp_path / "temporary",
        max_file_size_bytes=32,
        allowed_extensions=frozenset({"txt", "json", "pdf"}),
    )


def _owner_ids():
    return uuid4(), uuid4(), uuid4()


def test_storage_keeps_original_with_private_permissions(storage):
    identity_id, user_id, ingestion_id = _owner_ids()
    original = b"original content"

    stored = storage.save_stream(
        identity_id=identity_id,
        user_id=user_id,
        ingestion_id=ingestion_id,
        filename="source.txt",
        stream=io.BytesIO(original),
    )

    assert stored.absolute_path.read_bytes() == original
    assert stat.S_IMODE(storage.root.stat().st_mode) == 0o700
    assert stat.S_IMODE(stored.absolute_path.stat().st_mode) == 0o600


def test_storage_never_overwrites_same_ingestion_filename(storage):
    identity_id, user_id, ingestion_id = _owner_ids()
    first = storage.save_stream(
        identity_id=identity_id,
        user_id=user_id,
        ingestion_id=ingestion_id,
        filename="same.txt",
        stream=io.BytesIO(b"first"),
    )

    with pytest.raises(StoragePathError):
        storage.save_stream(
            identity_id=identity_id,
            user_id=user_id,
            ingestion_id=ingestion_id,
            filename="same.txt",
            stream=io.BytesIO(b"replacement"),
        )

    assert first.absolute_path.read_bytes() == b"first"


@pytest.mark.parametrize(
    ("filename", "content", "error"),
    [
        ("../outside.txt", b"hello", FilenameRejectedError),
        ("empty.txt", b"", EmptyFileError),
        ("large.txt", b"x" * 33, FileTooLargeError),
        ("bad.exe", b"hello", UnsupportedExtensionError),
        ("bad.json", b"{bad", ContentValidationError),
        ("bad.pdf", b"%PDF-1.7\n", ContentValidationError),
    ],
)
def test_storage_rejects_unsafe_or_invalid_sources(
    storage,
    filename,
    content,
    error,
):
    identity_id, user_id, ingestion_id = _owner_ids()

    with pytest.raises(error):
        storage.save_stream(
            identity_id=identity_id,
            user_id=user_id,
            ingestion_id=ingestion_id,
            filename=filename,
            stream=io.BytesIO(content),
        )


def test_storage_resolver_rejects_traversal_and_symlinks(storage, tmp_path):
    with pytest.raises(StoragePathError):
        storage.resolve_relative_path("../outside")

    identity_id, user_id, ingestion_id = _owner_ids()
    owner_directory = storage.ingestion_directory(
        identity_id=identity_id,
        user_id=user_id,
        ingestion_id=ingestion_id,
    )
    owner_directory.mkdir(parents=True)
    target = tmp_path / "outside.txt"
    target.write_text("outside", encoding="utf-8")
    link = owner_directory / "link.txt"

    try:
        link.symlink_to(target)
    except (NotImplementedError, OSError):
        pytest.skip("Symlinks are unavailable on this filesystem.")

    with pytest.raises(StoragePathError):
        storage.resolve_relative_path(link.relative_to(storage.root).as_posix())


def test_cleanup_removes_only_stale_partial_transfers(storage):
    identity_id, user_id, ingestion_id = _owner_ids()
    stored = storage.save_stream(
        identity_id=identity_id,
        user_id=user_id,
        ingestion_id=ingestion_id,
        filename="keep.txt",
        stream=io.BytesIO(b"received original"),
    )
    directory = stored.absolute_path.parent
    partial = directory / ".interrupted.part-deadbeef"
    partial.write_bytes(b"partial")
    old_time = time.time() - 3600
    os.utime(partial, (old_time, old_time))

    removed = storage.cleanup_abandoned_parts(max_age_seconds=60)

    assert removed == 1
    assert not partial.exists()
    assert stored.absolute_path.read_bytes() == b"received original"
