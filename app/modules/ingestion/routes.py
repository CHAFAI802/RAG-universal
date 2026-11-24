from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.ingestion.dependencies import (
    AuthenticatedUser,
    get_authenticated_user,
)
from app.modules.ingestion.file_validation import (
    FilenameRejectedError,
    UnsupportedExtensionError,
)
from app.modules.ingestion.folder_client import FOLDER_CLIENT_HTML
from app.modules.ingestion.models import Ingestion
from app.modules.ingestion.schemas import (
    CreateIngestionRequest,
    IngestionResponse,
)
from app.modules.ingestion.services import (
    IngestionConflictError,
    IngestionNotFoundError,
    IngestionReceiveError,
    IngestionService,
)
from app.modules.ingestion.storage import StoragePathError


router = APIRouter(
    prefix="/api/v1/ingestions",
    tags=["Ingestions"],
)


def _response(ingestion: Ingestion) -> IngestionResponse:
    return IngestionResponse(
        ingestion_id=ingestion.ingestion_id,
        identity_id=ingestion.identity_id,
        user_id=ingestion.user_id,
        source_type=ingestion.source_type,
        source_identifier=ingestion.source_identifier,
        document_name=ingestion.document_name,
        content_type=ingestion.content_type,
        size_bytes=ingestion.size_bytes,
        checksum_sha256=ingestion.checksum_sha256,
        status=ingestion.status.value,
        temporary_location=ingestion.storage_path,
        error_code=ingestion.error_code,
        error_message=ingestion.error_message,
        received_at=ingestion.received_at,
        created_at=ingestion.created_at,
        updated_at=ingestion.updated_at,
    )


def _raise_receive_error(exc: IngestionReceiveError) -> None:
    raise HTTPException(
        status_code=exc.status_code,
        detail=exc.message,
        headers={
            "X-Ingestion-ID": str(exc.ingestion_id),
            "X-Ingestion-Error-Code": exc.code,
        },
    ) from exc


def _create_ingestion(
    service: IngestionService,
    payload: CreateIngestionRequest,
    authenticated_user: AuthenticatedUser,
) -> Ingestion:
    try:
        return service.create_ingestion(
            authenticated_user=authenticated_user,
            document_name=payload.document_name,
            source_type=payload.source_type,
            source_identifier=payload.source_identifier,
        )
    except UnsupportedExtensionError as exc:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=str(exc),
        ) from exc
    except (FilenameRejectedError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc


@router.get(
    "/folder-client",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def folder_client() -> HTMLResponse:
    return HTMLResponse(
        FOLDER_CLIENT_HTML,
        headers={
            "Content-Security-Policy": (
                "default-src 'none'; script-src 'unsafe-inline'; "
                "style-src 'unsafe-inline'; connect-src 'self'; "
                "base-uri 'none'; frame-ancestors 'none'"
            ),
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "no-referrer",
        },
    )


@router.post(
    "",
    response_model=IngestionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ingestion(
    payload: CreateIngestionRequest,
    authenticated_user: AuthenticatedUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> IngestionResponse:
    ingestion = _create_ingestion(
        IngestionService(db),
        payload,
        authenticated_user,
    )
    return _response(ingestion)


@router.post(
    "/text",
    response_model=IngestionResponse,
    status_code=status.HTTP_201_CREATED,
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "text/plain": {
                    "schema": {"type": "string", "format": "binary"}
                }
            },
        }
    },
)
async def ingest_text(
    request: Request,
    document_name: str = Query(default="text.txt", min_length=1, max_length=255),
    authenticated_user: AuthenticatedUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> IngestionResponse:
    service = IngestionService(db)
    ingestion = _create_ingestion(
        service,
        CreateIngestionRequest(
            document_name=document_name,
            source_type="TEXT",
        ),
        authenticated_user,
    )

    try:
        received = await service.receive_stream(
            ingestion_id=ingestion.ingestion_id,
            authenticated_user=authenticated_user,
            chunks=request.stream(),
        )
    except IngestionReceiveError as exc:
        _raise_receive_error(exc)

    return _response(received)


@router.put(
    "/{ingestion_id}/source",
    response_model=IngestionResponse,
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/octet-stream": {
                    "schema": {"type": "string", "format": "binary"}
                }
            },
        }
    },
)
async def receive_source(
    ingestion_id: UUID,
    request: Request,
    authenticated_user: AuthenticatedUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> IngestionResponse:
    service = IngestionService(db)
    try:
        ingestion = await service.receive_stream(
            ingestion_id=ingestion_id,
            authenticated_user=authenticated_user,
            chunks=request.stream(),
        )
    except IngestionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingestion introuvable.",
        ) from exc
    except IngestionConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="L'état de l'ingestion n'autorise pas ce transfert.",
        ) from exc
    except IngestionReceiveError as exc:
        _raise_receive_error(exc)

    return _response(ingestion)


@router.get(
    "",
    response_model=list[IngestionResponse],
)
def list_ingestions(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    authenticated_user: AuthenticatedUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> list[IngestionResponse]:
    service = IngestionService(db)
    return [
        _response(ingestion)
        for ingestion in service.list_owned_ingestions(
            authenticated_user=authenticated_user,
            limit=limit,
            offset=offset,
        )
    ]


@router.get(
    "/{ingestion_id}/source",
    response_class=FileResponse,
    include_in_schema=False,
)
def get_original_source(
    ingestion_id: UUID,
    authenticated_user: AuthenticatedUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> FileResponse:
    service = IngestionService(db)
    try:
        ingestion = service.get_owned_ingestion(
            ingestion_id=ingestion_id,
            authenticated_user=authenticated_user,
        )
        path = service.get_source_path(ingestion=ingestion)
    except (IngestionNotFoundError, IngestionConflictError, StoragePathError) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source introuvable.",
        ) from exc

    return FileResponse(
        path=Path(path),
        filename=ingestion.document_name,
        media_type=ingestion.content_type or "application/octet-stream",
    )


@router.get(
    "/{ingestion_id}",
    response_model=IngestionResponse,
)
def get_ingestion(
    ingestion_id: UUID,
    authenticated_user: AuthenticatedUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> IngestionResponse:
    try:
        ingestion = IngestionService(db).get_owned_ingestion(
            ingestion_id=ingestion_id,
            authenticated_user=authenticated_user,
        )
    except IngestionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingestion introuvable.",
        ) from exc

    return _response(ingestion)
