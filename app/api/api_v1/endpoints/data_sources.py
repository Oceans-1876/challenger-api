from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.DataSourceSummaryPagination)
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
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Get a data source by id."""
    data_source = crud.data_source.get(db, id=data_source_id)
    if not data_source:
        raise HTTPException(
            status_code=404, detail=f"Data source not found: ${data_source_id}"
        )
    return data_source


@router.get("/{data_source_id}/species", response_model=List[schemas.SpeciesSummary])
def read_data_source_species(
    data_source_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get all the species for the given data source id."""
    species = crud.data_source.get_species(db, id=data_source_id)
    return species
