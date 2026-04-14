from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import auth, franchise, profile

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(franchise.router, prefix="/api/v1/franchise", tags=["Franchise"])
app.include_router(profile.router, prefix="/api/v1/profile", tags=["Profile"])