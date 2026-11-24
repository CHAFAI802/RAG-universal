from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.modules.auth.routes import router as auth_router
from app.modules.identity.routes import router as identity_router
from app.modules.ingestion.routes import router as ingestion_router
from app.modules.users.routes import router as users_router


app = FastAPI(
    title="RAG Universal API",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(identity_router)
app.include_router(users_router)
app.include_router(ingestion_router)


@app.exception_handler(RequestValidationError)
async def handle_validation_error(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    if request.url.path in {"/api/v1/auth/login", "/api/v1/users"}:
        sanitized_errors = [
            {key: value for key, value in error.items() if key != "input"}
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={"detail": jsonable_encoder(sanitized_errors)},
        )

    return await request_validation_exception_handler(request, exc)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
