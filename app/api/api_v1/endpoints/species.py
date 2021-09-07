from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Species])
def read_species(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100
) -> Any:
    """Retrieve species."""
    species = crud.species.get_multi(db, skip=skip, limit=limit)
    return species


@router.get("/{species_id}", response_model=schemas.Species)
def read_species_by_id(
    species_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get a specific species by id."""
    species = crud.species.get(db, id=species_id)
    return species
