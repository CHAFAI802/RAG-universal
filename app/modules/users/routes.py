from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.auth.dependencies import get_identity_admin
from app.modules.credentials.services import UsernameAlreadyExistsError
from app.modules.identity.models import Identity
from app.modules.users.schemas import UserCreateRequest, UserResponse
from app.modules.users.services import UserService


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    payload: UserCreateRequest,
    admin_identity: Identity = Depends(get_identity_admin),
    db: Session = Depends(get_db),
) -> UserResponse:
    service = UserService(db)

    try:
        user, credential = service.create_user(
            identity_id=admin_identity.identity_id,
            username=payload.username,
            password=payload.password,
        )

    except UsernameAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce username est déjà utilisé.",
        ) from exc

    return UserResponse(
        user_id=user.user_id,
        identity_id=user.identity_id,
        username=credential.username,
        status=user.status,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
