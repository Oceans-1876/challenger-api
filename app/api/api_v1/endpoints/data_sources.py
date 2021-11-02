from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.DataSourceSummary])
def read_data_sources(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve data sources."""
    data_sources = crud.data_source.get_multi(
        db, skip=skip, limit=limit, order_by=order_by
    )
    return data_sources


@router.get("/all/", response_model=List[schemas.DataSourceSummary])
def read_all_data_sources(
    db: Session = Depends(deps.get_db),
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve all data sources."""
    data_sources = crud.data_source.get_all(db, order_by=order_by)
    return data_sources


@router.get("/{data_source_id}", response_model=schemas.DataSourceDetails)
def read_data_source_by_id(
    data_source_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get a data source by id."""
    data_source = crud.data_source.get(db, id=data_source_id)
    return data_source