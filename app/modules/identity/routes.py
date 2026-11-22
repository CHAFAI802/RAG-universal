from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.identity.schemas import HumanIdentityCreate, IdentityResponse
from app.modules.identity.services import IdentityService


router = APIRouter(
    prefix="/api/v1/identities",
    tags=["Identities"],
)


@router.post(
    "/human",
    response_model=IdentityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_human_identity(
    payload: HumanIdentityCreate,
    db: Session = Depends(get_db),
) -> IdentityResponse:
    service = IdentityService(db)

    try:
        identity = service.create_human_identity(
            display_name=payload.display_name,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return IdentityResponse.model_validate(identity)
