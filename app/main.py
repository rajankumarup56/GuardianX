from fastapi import FastAPI

from app.api.routes.health import router as health_router

app = FastAPI(
    title="GuardianX",
    version="0.1.0",
    description=(
        "Defensive cybersecurity, privacy and safety "
        "layer for connected cyber-physical systems."
    ),
)

app.include_router(health_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "product": "GuardianX",
        "status": "running",
        "version": "0.1.0",
    }