from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.routes.cats import router as cats_router
from app.api.routes.missions import router as missions_router

app = FastAPI(title="Spy Cat Agency API")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(cats_router)
app.include_router(missions_router)

@app.get("/health")
def health():
    return {"status": "ok"}
