from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Station])
def read_stations(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100
) -> Any:
    """Retrieve stations."""
    stations = crud.station.get_multi(db, skip=skip, limit=limit)
    return stations


@router.get("/{station_id}", response_model=schemas.Station)
def read_station_by_id(
    station_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get a specific station by id."""
    station = crud.station.get(db, id=station_id)
    return station
