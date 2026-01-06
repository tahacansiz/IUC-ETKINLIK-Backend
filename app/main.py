from fastapi import FastAPI
from app.api.v1 import auth, event_api, user_api
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="IUC Event API")

# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user_api.router, prefix="/api/v1/user_api", tags=["Users"])
app.include_router(event_api.router, prefix="/api/v1/event_api", tags=["Events"])
app.mount("/media", StaticFiles(directory="media"), name="media")