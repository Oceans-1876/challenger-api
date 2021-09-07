from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    data_sources,
    login,
    species,
    stations,
    users,
    utils,
)

api_router = APIRouter()
api_router.include_router(data_sources.router, prefix="/data_source", tags=["species"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(species.router, prefix="/species", tags=["species"])
api_router.include_router(stations.router, prefix="/stations", tags=["stations"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
