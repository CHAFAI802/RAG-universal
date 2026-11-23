from fastapi import FastAPI

from app.modules.auth.routes import router as auth_router
from app.modules.identity.routes import router as identity_router


app = FastAPI(
    title="RAG Universal API",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(identity_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
