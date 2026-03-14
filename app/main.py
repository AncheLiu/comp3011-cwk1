from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.custom_builds import router as custom_builds_router
from app.api.routes.heroes import router as heroes_router
from app.api.routes.saved_reports import router as saved_reports_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models import CustomBuild, Hero, Match, MatchParticipant, SavedReport  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.app_name,
    description="A data-driven API for Deadlock analytics and build management.",
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(heroes_router)
app.include_router(custom_builds_router)
app.include_router(saved_reports_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Deadlock Meta Intelligence API"}
