from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.models import stations_species_table

router = APIRouter()


@router.get("/", response_model=List[schemas.StationSummary])
def read_stations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve stations."""
    stations = crud.station.get_multi(db, skip=skip, limit=limit, order_by=order_by)
    return stations


@router.get("/all/", response_model=List[schemas.StationSummary])
def read_all_stations(
    db: Session = Depends(deps.get_db),
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve all stations."""
    stations = crud.station.get_all(db, order_by=order_by)
    return stations


@router.post("/search/", response_model=List[schemas.StationSummary])
def read_stations_by_search(
    expressions: Union[schemas.Expression, schemas.ExpressionGroup],
    db: Session = Depends(deps.get_db),
    limit: int = 0,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieves the stations based on the given search expressions."""
    stations = crud.station.search(
        db,
        expressions=expressions,
        relations=[stations_species_table],
        order_by=order_by,
        limit=limit,
    )
    return stations


@router.get("/{station_id}", response_model=schemas.StationDetails)
def read_station_by_id(station_id: str, db: Session = Depends(deps.get_db)) -> Any:
    """Get a specific station by id."""
    station = crud.station.get(db, id=station_id)
    if not station:
        raise HTTPException(status_code=404, detail=f"Station not found: ${station_id}")
    return station
