from fastapi import APIRouter

from app.core.config import get_settings

from .endpoints import data_sources, login, species, stations, users, utils

settings = get_settings()

# Add all the API endpoints from the endpoints folder
api_router = APIRouter()
api_router.include_router(data_sources.router, prefix="/data_source", tags=["species"])
api_router.include_router(species.router, prefix="/species", tags=["species"])
api_router.include_router(stations.router, prefix="/stations", tags=["stations"])

if settings.ENABLE_AUTH:
    api_router.include_router(login.router, tags=["login"])
    api_router.include_router(users.router, prefix="/users", tags=["users"])
    api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
