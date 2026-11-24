import asyncio
import logging
import re
import tempfile
from collections.abc import AsyncIterable
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
from starlette.requests import ClientDisconnect

from app.core.config import settings
from app.modules.ingestion.dependencies import AuthenticatedUser
from app.modules.ingestion.file_validation import (
    ContentValidationError,
    FilenameRejectedError,
    UnsupportedExtensionError,
    allowed_extensions_from_config,
    sanitize_filename,
)
from app.modules.ingestion.models import Ingestion, IngestionStatus
from app.modules.ingestion.storage import (
    EmptyFileError,
    FileTooLargeError,
    StoragePathError,
    StoredOriginal,
    TemporaryStorage,
)


logger = logging.getLogger(__name__)

SOURCE_TYPE_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]{0,49}$")
SPOOL_MEMORY_LIMIT_BYTES = 1024 * 1024


class IngestionNotFoundError(Exception):
    """L'ingestion n'existe pas pour l'utilisateur authentifié."""


class IngestionConflictError(Exception):
    """L'état de l'ingestion n'autorise pas une nouvelle réception."""


class IngestionReceiveError(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        ingestion_id: UUID,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.ingestion_id = ingestion_id


class IngestionService:
    def __init__(self, session: Session):
        self.session = session
        self.storage = TemporaryStorage(
            settings.INGESTION_TEMP_STORAGE_PATH,
            max_file_size_bytes=settings.INGESTION_MAX_FILE_SIZE_BYTES,
            allowed_extensions=allowed_extensions_from_config(
                settings.INGESTION_ALLOWED_EXTENSIONS
            ),
        )

    def create_ingestion(
        self,
        *,
        authenticated_user: AuthenticatedUser,
        document_name: str,
        source_type: str,
        source_identifier: str | None = None,
    ) -> Ingestion:
        normalized_source_type = source_type.strip().upper()
        if not SOURCE_TYPE_PATTERN.fullmatch(normalized_source_type):
            raise ValueError("Le type de source est invalide.")

        safe_name = sanitize_filename(
            document_name,
            allowed_extensions=self.storage.allowed_extensions,
        )
        self._validate_source_identifier(
            source_type=normalized_source_type,
            source_identifier=source_identifier,
        )

        ingestion = Ingestion(
            identity_id=authenticated_user.identity.identity_id,
            user_id=authenticated_user.user.user_id,
            source_type=normalized_source_type,
            source_identifier=source_identifier,
            document_name=safe_name,
        )
        self.session.add(ingestion)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return ingestion

    async def receive_stream(
        self,
        *,
        ingestion_id: UUID,
        authenticated_user: AuthenticatedUser,
        chunks: AsyncIterable[bytes],
    ) -> Ingestion:
        ingestion = self.get_owned_ingestion(
            ingestion_id=ingestion_id,
            authenticated_user=authenticated_user,
            lock=True,
        )
        if ingestion.status in {
            IngestionStatus.RECEIVING,
            IngestionStatus.RECEIVED,
        }:
            raise IngestionConflictError

        ingestion.status = IngestionStatus.RECEIVING
        ingestion.error_code = None
        ingestion.error_message = None
        self.session.commit()

        try:
            with tempfile.SpooledTemporaryFile(
                max_size=SPOOL_MEMORY_LIMIT_BYTES,
                mode="w+b",
            ) as spool:
                total = 0
                async for chunk in chunks:
                    if not isinstance(chunk, bytes):
                        raise OSError("Le flux de transfert est invalide.")

                    total += len(chunk)
                    if total > settings.INGESTION_MAX_FILE_SIZE_BYTES:
                        raise FileTooLargeError(
                            "Le document dépasse la taille maximale autorisée."
                        )
                    spool.write(chunk)

                if total == 0:
                    raise EmptyFileError("Le document transmis est vide.")

                spool.seek(0)
                stored = await run_in_threadpool(
                    self.storage.save_stream,
                    identity_id=ingestion.identity_id,
                    user_id=ingestion.user_id,
                    ingestion_id=ingestion.ingestion_id,
                    filename=ingestion.document_name,
                    stream=spool,
                )
        except asyncio.CancelledError:
            self._mark_failed(
                ingestion,
                code="transfer_interrupted",
                message="Le transfert du document a été interrompu.",
            )
            raise
        except FileTooLargeError as exc:
            self._mark_failed(
                ingestion,
                code="file_too_large",
                message="Le document dépasse la taille maximale autorisée.",
            )
            raise IngestionReceiveError(
                status_code=413,
                code="file_too_large",
                message="Le document dépasse la taille maximale autorisée.",
                ingestion_id=ingestion.ingestion_id,
            ) from exc
        except EmptyFileError as exc:
            self._mark_failed(
                ingestion,
                code="empty_file",
                message="Le document transmis est vide.",
            )
            raise IngestionReceiveError(
                status_code=422,
                code="empty_file",
                message="Le document transmis est vide.",
                ingestion_id=ingestion.ingestion_id,
            ) from exc
        except ContentValidationError as exc:
            self._mark_failed(
                ingestion,
                code="invalid_content",
                message="Le contenu ne correspond pas au format annoncé.",
            )
            raise IngestionReceiveError(
                status_code=422,
                code="invalid_content",
                message="Le contenu ne correspond pas au format annoncé.",
                ingestion_id=ingestion.ingestion_id,
            ) from exc
        except StoragePathError as exc:
            self._mark_failed(
                ingestion,
                code="storage_conflict",
                message="Le document ne peut pas être enregistré à cet emplacement.",
            )
            raise IngestionReceiveError(
                status_code=409,
                code="storage_conflict",
                message="Le document ne peut pas être enregistré à cet emplacement.",
                ingestion_id=ingestion.ingestion_id,
            ) from exc
        except ClientDisconnect as exc:
            self._mark_failed(
                ingestion,
                code="transfer_interrupted",
                message="Le transfert du document a été interrompu.",
            )
            raise IngestionReceiveError(
                status_code=400,
                code="transfer_interrupted",
                message="Le transfert du document a été interrompu.",
                ingestion_id=ingestion.ingestion_id,
            ) from exc
        except (FilenameRejectedError, UnsupportedExtensionError) as exc:
            self._mark_failed(
                ingestion,
                code="invalid_document",
                message="Le document ne peut pas être accepté.",
            )
            raise IngestionReceiveError(
                status_code=422,
                code="invalid_document",
                message="Le document ne peut pas être accepté.",
                ingestion_id=ingestion.ingestion_id,
            ) from exc
        except OSError as exc:
            logger.exception(
                "Ingestion %s failed during temporary storage.",
                ingestion.ingestion_id,
            )
            self._mark_failed(
                ingestion,
                code="storage_error",
                message="Une erreur empêche l'enregistrement temporaire.",
            )
            raise IngestionReceiveError(
                status_code=503,
                code="storage_error",
                message="Une erreur empêche l'enregistrement temporaire.",
                ingestion_id=ingestion.ingestion_id,
            ) from exc
        except Exception as exc:
            logger.exception(
                "Unexpected ingestion failure for %s.",
                ingestion.ingestion_id,
            )
            self._mark_failed(
                ingestion,
                code="internal_error",
                message="Une erreur empêche la réception du document.",
            )
            raise IngestionReceiveError(
                status_code=500,
                code="internal_error",
                message="Une erreur empêche la réception du document.",
                ingestion_id=ingestion.ingestion_id,
            ) from exc

        self._mark_received(ingestion, stored)
        return ingestion

    def get_owned_ingestion(
        self,
        *,
        ingestion_id: UUID,
        authenticated_user: AuthenticatedUser,
        lock: bool = False,
    ) -> Ingestion:
        statement = select(Ingestion).where(
            Ingestion.ingestion_id == ingestion_id,
            Ingestion.identity_id == authenticated_user.identity.identity_id,
            Ingestion.user_id == authenticated_user.user.user_id,
        )
        if lock:
            statement = statement.with_for_update()

        ingestion = self.session.scalar(statement)
        if ingestion is None:
            raise IngestionNotFoundError
        return ingestion

    def list_owned_ingestions(
        self,
        *,
        authenticated_user: AuthenticatedUser,
        limit: int,
        offset: int,
    ) -> list[Ingestion]:
        statement = (
            select(Ingestion)
            .where(
                Ingestion.identity_id == authenticated_user.identity.identity_id,
                Ingestion.user_id == authenticated_user.user.user_id,
            )
            .order_by(Ingestion.created_at.desc(), Ingestion.ingestion_id)
            .limit(limit)
            .offset(offset)
        )
        return list(self.session.scalars(statement).all())

    def mark_abandoned_ingestions(self) -> int:
        cutoff = datetime.now(timezone.utc) - timedelta(
            seconds=settings.INGESTION_ABANDONED_FAILED_TTL_SECONDS
        )
        abandoned = self.session.scalars(
            select(Ingestion).where(
                Ingestion.status.in_(
                    [IngestionStatus.PENDING, IngestionStatus.RECEIVING]
                ),
                Ingestion.updated_at < cutoff,
            )
        ).all()

        marked = 0
        for ingestion in abandoned:
            expected_directory = self.storage.ingestion_directory(
                identity_id=ingestion.identity_id,
                user_id=ingestion.user_id,
                ingestion_id=ingestion.ingestion_id,
            )
            expected_original = expected_directory / ingestion.document_name
            if expected_original.is_symlink() or expected_original.exists():
                logger.warning(
                    "Abandoned ingestion %s has an original requiring reconciliation.",
                    ingestion.ingestion_id,
                )
                continue

            ingestion.status = IngestionStatus.FAILED
            ingestion.error_code = "abandoned_transfer"
            ingestion.error_message = (
                "La réception incomplète a expiré. Le transfert peut être relancé."
            )
            marked += 1

        if marked:
            self.session.commit()

        return marked

    def get_source_path(
        self,
        *,
        ingestion: Ingestion,
    ) -> Path:
        if (
            ingestion.status != IngestionStatus.RECEIVED
            or ingestion.storage_path is None
        ):
            raise IngestionConflictError

        path = self.storage.resolve_relative_path(ingestion.storage_path)
        expected_directory = self.storage.ingestion_directory(
            identity_id=ingestion.identity_id,
            user_id=ingestion.user_id,
            ingestion_id=ingestion.ingestion_id,
        ).resolve()
        if path.parent != expected_directory or not path.is_file():
            raise IngestionNotFoundError

        return path

    def _mark_failed(
        self,
        ingestion: Ingestion,
        *,
        code: str,
        message: str,
    ) -> None:
        ingestion.status = IngestionStatus.FAILED
        ingestion.error_code = code
        ingestion.error_message = message
        self.session.commit()

    def _mark_received(
        self,
        ingestion: Ingestion,
        stored: StoredOriginal,
    ) -> None:
        ingestion.status = IngestionStatus.RECEIVED
        ingestion.content_type = stored.content_type
        ingestion.size_bytes = stored.size_bytes
        ingestion.checksum_sha256 = stored.checksum_sha256
        ingestion.storage_path = stored.relative_path
        ingestion.received_at = datetime.now(timezone.utc)
        ingestion.error_code = None
        ingestion.error_message = None
        self.session.commit()

    @staticmethod
    def _validate_source_identifier(
        *,
        source_type: str,
        source_identifier: str | None,
    ) -> None:
        if source_identifier is None:
            if source_type == "WEB":
                raise ValueError("Une URL HTTPS est requise pour une source WEB.")
            return

        if (
            len(source_identifier.encode("utf-8")) > 1024
            or any(
                ord(character) < 32 or ord(character) == 127
                for character in source_identifier
            )
        ):
            raise ValueError("L'identifiant de source est invalide.")

        if source_type == "WEB":
            parsed = urlsplit(source_identifier)
            if (
                parsed.scheme != "https"
                or not parsed.hostname
                or parsed.username is not None
                or parsed.password is not None
            ):
                raise ValueError("L'URL de source doit utiliser HTTPS.")
            return

        if source_type in {"LOCAL_FILE", "LOCAL_FOLDER"}:
            if (
                not source_identifier
                or "\\" in source_identifier
                or source_identifier.startswith("/")
                or any(
                    part in {"", ".", ".."}
                    for part in source_identifier.split("/")
                )
            ):
                raise ValueError("Le chemin local relatif est invalide.")
            return

        if source_identifier.startswith(("/", "\\")):
            raise ValueError("Un chemin local absolu est interdit.")

