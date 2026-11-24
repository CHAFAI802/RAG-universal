import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree


DEFAULT_ALLOWED_EXTENSIONS = frozenset(
    {
        "pdf",
        "docx",
        "txt",
        "csv",
        "json",
        "md",
        "html",
        "htm",
        "xml",
        "rtf",
        "odt",
    }
)

TEXT_EXTENSIONS = frozenset({"txt", "csv", "json", "md", "html", "htm", "xml"})

CONTENT_TYPES_BY_EXTENSION = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "odt": "application/vnd.oasis.opendocument.text",
    "txt": "text/plain",
    "csv": "text/csv",
    "json": "application/json",
    "md": "text/markdown",
    "html": "text/html",
    "htm": "text/html",
    "xml": "application/xml",
    "rtf": "application/rtf",
}

# Noms réservés Windows : refusés même sur un serveur POSIX afin qu'une
# future utilisation locale du nom ne crée pas de comportement ambigu.
_WINDOWS_RESERVED_NAMES = frozenset(
    {"con", "prn", "aux", "nul"}
    | {f"com{index}" for index in range(1, 10)}
    | {f"lpt{index}" for index in range(1, 10)}
)

_FORBIDDEN_FILENAME_CHARACTERS = frozenset('<>:"|?*')


class FilenameRejectedError(ValueError):
    """Le nom de fichier est absent, ambigu ou dangereux."""


class UnsupportedExtensionError(ValueError):
    """L'extension n'appartient pas à la liste configurée."""


class ContentValidationError(ValueError):
    """Le contenu ne correspond pas au format attendu."""


def get_extension(filename: str) -> str:
    name = filename.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    if "." not in name:
        return ""
    return name.rsplit(".", 1)[-1].lower()


def sanitize_filename(
    filename: str,
    *,
    allowed_extensions: frozenset[str] = DEFAULT_ALLOWED_EXTENSIONS,
) -> str:
    """Retourne un nom de fichier sûr, ou refuse la réception.

    Le nom fourni par le client n'est jamais utilisé comme chemin : seuls
    ses composants contrôlés sont conservés pour l'affichage et le stockage.
    """

    if not isinstance(filename, str):
        raise FilenameRejectedError("Le nom du document est obligatoire.")

    name = filename.strip()

    if not name:
        raise FilenameRejectedError("Le nom du document est obligatoire.")

    if len(name.encode("utf-8")) > 255:
        raise FilenameRejectedError(
            "Le nom du document ne peut pas dépasser 255 octets."
        )

    if name in {".", ".."} or name.startswith("."):
        raise FilenameRejectedError("Le nom du document est interdit.")

    if "/" in name or "\\" in name:
        raise FilenameRejectedError(
            "Le nom du document ne peut pas contenir de chemin."
        )

    if ".." in name:
        raise FilenameRejectedError(
            "Le nom du document ne peut pas contenir de traversée de répertoire."
        )

    if name.endswith(".") or name.endswith(" "):
        raise FilenameRejectedError(
            "Le nom du document ne peut pas se terminer par un point ou un espace."
        )

    for character in name:
        if ord(character) < 32 or ord(character) == 127:
            raise FilenameRejectedError(
                "Le nom du document contient des caractères de contrôle."
            )
        if character in _FORBIDDEN_FILENAME_CHARACTERS:
            raise FilenameRejectedError(
                "Le nom du document contient des caractères interdits."
            )

    stem = name.rsplit(".", 1)[0].strip().lower()
    if stem in _WINDOWS_RESERVED_NAMES:
        raise FilenameRejectedError("Le nom du document est réservé.")

    extension = get_extension(name)

    if not extension:
        raise UnsupportedExtensionError(
            "Le document doit posséder une extension explicite."
        )

    if extension not in allowed_extensions:
        raise UnsupportedExtensionError(
            f"L'extension .{extension} n'est pas prise en charge."
        )

    return name


def allowed_extensions_from_config(value: str) -> frozenset[str]:
    extensions = {
        item.strip().lower().lstrip(".")
        for item in value.split(",")
        if item.strip()
    }
    return frozenset(extensions) if extensions else DEFAULT_ALLOWED_EXTENSIONS


def detect_content_type(*, filename: str, head: bytes) -> str:
    """Détermine le type MIME à partir de l'extension et des octets réels."""

    extension = get_extension(filename)
    content_type = CONTENT_TYPES_BY_EXTENSION.get(
        extension,
        "application/octet-stream",
    )

    if extension == "pdf":
        if not head.startswith(b"%PDF-"):
            raise ContentValidationError(
                "Le contenu ne correspond pas à un fichier PDF."
            )
    elif extension in {"docx", "odt"}:
        if not head.startswith(b"PK\x03\x04"):
            raise ContentValidationError(
                "Le contenu ne correspond pas à un document OOXML/ODF."
            )
    elif extension == "rtf":
        if not head.lstrip().startswith(b"{\\rtf"):
            raise ContentValidationError(
                "Le contenu ne correspond pas à un fichier RTF."
            )
    elif extension in TEXT_EXTENSIONS:
        if b"\x00" in head:
            raise ContentValidationError(
                "Le contenu texte contient des octets binaires."
            )

    return content_type


def validate_saved_content(
    *,
    path: Path,
    filename: str,
    content_type: str,
) -> None:
    """Valide le contenu complet après réception, sans faire confiance au client."""

    extension = get_extension(filename)

    if extension in TEXT_EXTENSIONS:
        try:
            content = path.read_bytes().decode("utf-8-sig")
        except (UnicodeDecodeError, OSError) as exc:
            raise ContentValidationError(
                "Le contenu texte doit être encodé en UTF-8 valide."
            ) from exc

        if extension == "json":
            try:
                json.loads(content)
            except json.JSONDecodeError as exc:
                raise ContentValidationError(
                    "Le contenu JSON est malformé."
                ) from exc
        elif extension == "xml":
            try:
                ElementTree.fromstring(content)
            except ElementTree.ParseError as exc:
                raise ContentValidationError(
                    "Le contenu XML est malformé."
                ) from exc

    if extension in {"docx", "odt"}:
        try:
            with zipfile.ZipFile(path) as archive:
                names = set(archive.namelist())
        except (OSError, zipfile.BadZipFile) as exc:
            raise ContentValidationError(
                "L'archive du document est malformée."
            ) from exc

        required_members = (
            {"[Content_Types].xml", "word/document.xml"}
            if extension == "docx"
            else {"mimetype", "content.xml"}
        )
        if not required_members.issubset(names):
            raise ContentValidationError(
                "L'archive ne contient pas la structure attendue."
            )

    if extension == "pdf":
        with path.open("rb") as handle:
            if not handle.read(5).startswith(b"%PDF-"):
                raise ContentValidationError(
                    "Le contenu ne correspond pas à un fichier PDF."
                )
            handle.seek(max(0, path.stat().st_size - 1024))
            if b"%%EOF" not in handle.read():
                raise ContentValidationError(
                    "Le fichier PDF semble incomplet."
                )

    if content_type == "application/octet-stream" and path.stat().st_size == 0:
        raise ContentValidationError("Le document est vide.")


def is_safe_component(value: str) -> bool:
    """Vérifie qu'une valeur ne peut pas introduire de chemin arbitraire."""

    return bool(re.fullmatch(r"[A-Za-z0-9_-]{1,128}", value))
