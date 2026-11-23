from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.auth.authentication import (
    AccountDisabledError,
    AuthenticationService,
    InvalidCredentialsError,
)
from app.modules.auth.registration import RegistrationService
from app.modules.credentials.services import UsernameAlreadyExistsError
from app.modules.auth.schemas import (
    LoginRequest,
    LoginResponse,
    RegistrationRequest,
    RegistrationResponse,
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: RegistrationRequest,
    db: Session = Depends(get_db),
) -> RegistrationResponse:
    service = RegistrationService(db)

    try:
        identity, credential = service.register(
            display_name=payload.display_name,
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

    return RegistrationResponse(
        identity_id=identity.identity_id,
        identity_type=identity.identity_type,
        display_name=identity.display_name,
        username=credential.username,
        status=identity.status,
        created_at=identity.created_at,
        updated_at=identity.updated_at,
    )


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> LoginResponse:
    service = AuthenticationService(db)

    try:
        access_token = service.authenticate(
            username=payload.username,
            password=payload.password,
        )
    except (InvalidCredentialsError, AccountDisabledError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides ou compte désactivé.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return LoginResponse(
        access_token=access_token,
        expires_in=service.token_lifetime_seconds,
    )
