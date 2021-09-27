from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.DataSourceIDOnly])
def read_data_source(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Retrieve data sources."""
    data_sources = crud.data_source.get_multi(db, skip=skip, limit=limit)
    return data_sources


@router.get("/{data_source_id}", response_model=schemas.DataSource)
def read_data_source_by_id(
    data_source_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get a data source by id."""
    data_source = crud.data_source.get(db, id=data_source_id)
    return data_source
