from app.core.config import settings
from app.core.database import SessionLocal
from app.modules.ingestion.file_validation import allowed_extensions_from_config
from app.modules.ingestion.services import IngestionService
from app.modules.ingestion.storage import TemporaryStorage


def main() -> None:
    storage = TemporaryStorage(
        settings.INGESTION_TEMP_STORAGE_PATH,
        max_file_size_bytes=settings.INGESTION_MAX_FILE_SIZE_BYTES,
        allowed_extensions=allowed_extensions_from_config(
            settings.INGESTION_ALLOWED_EXTENSIONS
        ),
    )
    removed = storage.cleanup_abandoned_parts(
        max_age_seconds=settings.INGESTION_ABANDONED_ORPHAN_TTL_SECONDS
    )
    with SessionLocal() as session:
        failed = IngestionService(session).mark_abandoned_ingestions()

    print(
        f"Removed {removed} stale partial transfer(s); "
        f"marked {failed} abandoned ingestion(s) as failed."
    )


if __name__ == "__main__":
    main()
