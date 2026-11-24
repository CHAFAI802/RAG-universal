import hashlib
import logging
import os
import stat
import time
import uuid
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import BinaryIO

from app.modules.ingestion.file_validation import (
    ContentValidationError,
    DEFAULT_ALLOWED_EXTENSIONS,
    detect_content_type,
    sanitize_filename,
    validate_saved_content,
)


CHUNK_SIZE = 1024 * 1024
SNIFF_SIZE = 512

logger = logging.getLogger(__name__)


class TemporaryStorageError(Exception):
    """Erreur interne du stockage temporaire."""


class EmptyFileError(TemporaryStorageError):
    """Le transfert ne contient aucun octet."""


class FileTooLargeError(TemporaryStorageError):
    """Le transfert dépasse la limite configurée."""


class StoragePathError(TemporaryStorageError):
    """Le chemin demandé sort du stockage temporaire ou est ambigu."""


@dataclass(frozen=True)
class StoredOriginal:
    relative_path: str
    absolute_path: Path
    size_bytes: int
    checksum_sha256: str
    content_type: str


class TemporaryStorage:
    """Stockage temporaire des sources originales reçues.

    Organisation : <racine>/<identity_id>/<user_id>/<ingestion_id>/<nom>.
    Aucun écrasement n'est possible : chaque ingestion possède son répertoire
    et le lien final est créé de façon exclusive. La réception ne supprime
    jamais une source originale.
    """

    def __init__(
        self,
        root: str | Path,
        *,
        max_file_size_bytes: int,
        allowed_extensions: frozenset[str] = DEFAULT_ALLOWED_EXTENSIONS,
    ):
        if max_file_size_bytes <= 0:
            raise ValueError("La taille maximale doit être strictement positive.")

        self.root = Path(root).expanduser().resolve()
        self.max_file_size_bytes = max_file_size_bytes
        self.allowed_extensions = allowed_extensions
        self._ensure_root()

    def _ensure_root(self) -> None:
        self.root.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.root.chmod(0o700)

    def owner_directory(
        self,
        *,
        identity_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Path:
        directory = self.root / str(identity_id) / str(user_id)
        self._ensure_inside_root(directory)
        return directory

    def ingestion_directory(
        self,
        *,
        identity_id: uuid.UUID,
        user_id: uuid.UUID,
        ingestion_id: uuid.UUID,
    ) -> Path:
        directory = self.owner_directory(
            identity_id=identity_id,
            user_id=user_id,
        ) / str(ingestion_id)
        self._ensure_inside_root(directory)
        return directory

    def save_stream(
        self,
        *,
        identity_id: uuid.UUID,
        user_id: uuid.UUID,
        ingestion_id: uuid.UUID,
        filename: str,
        stream: BinaryIO,
    ) -> StoredOriginal:
        filename = sanitize_filename(
            filename,
            allowed_extensions=self.allowed_extensions,
        )
        directory = self.ingestion_directory(
            identity_id=identity_id,
            user_id=user_id,
            ingestion_id=ingestion_id,
        )
        self._create_private_directories(directory)

        final_path = directory / filename
        self._ensure_inside_root(final_path)

        if final_path.is_symlink() or final_path.exists():
            raise StoragePathError(
                "Un document portant ce nom existe déjà pour cette ingestion."
            )

        part_path = directory / f".{ingestion_id}.part-{uuid.uuid4().hex}"

        digest = hashlib.sha256()
        total = 0
        head = b""
        content_type = "application/octet-stream"

        try:
            with part_path.open("xb") as handle:
                part_path.chmod(0o600)

                while True:
                    chunk = stream.read(CHUNK_SIZE)

                    if not chunk:
                        break

                    if not isinstance(chunk, bytes):
                        raise TemporaryStorageError(
                            "Flux de transfert invalide."
                        )

                    total += len(chunk)

                    if total > self.max_file_size_bytes:
                        raise FileTooLargeError(
                            "Le document dépasse la taille maximale autorisée."
                        )

                    if len(head) < SNIFF_SIZE:
                        head += chunk[: SNIFF_SIZE - len(head)]
                        content_type = detect_content_type(
                            filename=filename,
                            head=head,
                        )

                    digest.update(chunk)
                    handle.write(chunk)

            if total == 0:
                raise EmptyFileError("Le document transmis est vide.")

            validate_saved_content(
                path=part_path,
                filename=filename,
                content_type=content_type,
            )

            try:
                os.link(part_path, final_path, follow_symlinks=False)
            except FileExistsError as exc:
                raise StoragePathError(
                    "Un document portant ce nom existe déjà pour cette ingestion."
                ) from exc
            try:
                part_path.unlink()
            except OSError:
                logger.exception(
                    "Completed ingestion %s left a partial hard link.",
                    ingestion_id,
                )

        except Exception:
            try:
                part_path.unlink(missing_ok=True)
            except FileNotFoundError:
                pass
            except OSError:
                logger.exception(
                    "Could not remove incomplete transfer file %s.",
                    part_path,
                )
            raise

        return StoredOriginal(
            relative_path=final_path.relative_to(self.root).as_posix(),
            absolute_path=final_path,
            size_bytes=total,
            checksum_sha256=digest.hexdigest(),
            content_type=content_type,
        )

    def resolve_relative_path(self, relative_path: str) -> Path:
        if not relative_path or "\\" in relative_path:
            raise StoragePathError("Chemin de stockage invalide.")

        candidate = PurePosixPath(relative_path)

        if candidate.is_absolute() or ".." in candidate.parts:
            raise StoragePathError("Chemin de stockage invalide.")

        path = self.root / candidate
        current = self.root
        for component in candidate.parts:
            current = current / component
            if current.is_symlink():
                raise StoragePathError("Les liens symboliques sont refusés.")

        resolved = path.resolve()
        self._ensure_inside_root(resolved)
        return resolved

    def cleanup_abandoned_parts(self, *, max_age_seconds: int) -> int:
        if max_age_seconds <= 0:
            raise ValueError("L'âge maximal doit être strictement positif.")

        cutoff_time = time.time() - max_age_seconds
        removed = 0

        def raise_walk_error(error: OSError) -> None:
            raise error

        for directory_name, subdirectories, filenames in os.walk(
            self.root,
            followlinks=False,
            onerror=raise_walk_error,
        ):
            directory = Path(directory_name)
            subdirectories[:] = [
                name
                for name in subdirectories
                if not (directory / name).is_symlink()
            ]

            for filename in filenames:
                if not filename.startswith(".") or ".part-" not in filename:
                    continue

                candidate = directory / filename
                try:
                    metadata = candidate.lstat()
                except FileNotFoundError:
                    continue

                if (
                    stat.S_ISREG(metadata.st_mode)
                    and metadata.st_mtime <= cutoff_time
                ):
                    candidate.unlink()
                    removed += 1

        return removed

    def _create_private_directories(self, directory: Path) -> None:
        relative = directory.relative_to(self.root)
        current = self.root

        for component in relative.parts:
            current = current / component
            self._ensure_inside_root(current)
            current.mkdir(mode=0o700, exist_ok=True)
            if current.is_symlink():
                raise StoragePathError("Les liens symboliques sont refusés.")
            current.chmod(0o700)

    def _ensure_inside_root(self, path: Path) -> None:
        resolved = path.resolve()

        if resolved != self.root and self.root not in resolved.parents:
            raise StoragePathError(
                "Le chemin demandé sort du stockage temporaire."
            )


__all__ = [
    "ContentValidationError",
    "EmptyFileError",
    "FileTooLargeError",
    "StoragePathError",
    "StoredOriginal",
    "TemporaryStorage",
    "TemporaryStorageError",
]
