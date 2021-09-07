"""Pydantic models for representing species extracted by `challenger-workflows`.
"""
from typing import Optional

from pydantic import BaseModel


class SpeciesBase(BaseModel):
    id: str
    matched_name: str
    matched_canonical_simple_name: Optional[str] = None
    matched_canonical_full_name: Optional[str] = None
    common_name: Optional[str] = None
    classification_path: str
    classification_ranks: str
    classification_ids: str
    data_source_id: int


class SpeciesCreate(SpeciesBase):
    pass


class SpeciesUpdate(SpeciesBase):
    pass


class SpeciesInDB(SpeciesBase):
    class Config:
        orm_mode = True


class Species(SpeciesInDB):
    pass
