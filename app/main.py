from fastapi import FastAPI


app = FastAPI(
    title="Deadlock Meta Intelligence API",
    description="A data-driven API for Deadlock analytics and build management.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Deadlock Meta Intelligence API"}

