from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.SpeciesSummary])
def read_species(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve species."""
    species = crud.species.get_multi(db, skip=skip, limit=limit, order_by=order_by)
    return species


@router.get("/all/", response_model=List[schemas.SpeciesSummary])
def read_all_species(
    db: Session = Depends(deps.get_db), order_by: Optional[List[str]] = Query(None)
) -> Any:
    """Retrieve all species."""
    species = crud.species.get_all(db, order_by=order_by)
    return species


@router.get("/search/", response_model=List[schemas.SpeciesSummary])
def read_species_by_search(
    search_term: str,
    search_column: str,
    db: Session = Depends(deps.get_db),
    limit: int = 0,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieves the species based on the
    requested search params.
    """
    species = crud.species.search(
        db,
        search_column=search_column,
        search_term=search_term,
        order_by=order_by,
        limit=limit,
    )
    return species


@router.get("/{species_id}", response_model=schemas.SpeciesDetails)
def read_species_by_id(
    species_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get a specific species by id."""
    species = crud.species.get(db, id=species_id)
    if not species:
        raise HTTPException(status_code=404, detail=f"Species not found: ${species_id}")
    return species
