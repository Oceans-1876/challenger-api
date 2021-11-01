"""Pydantic models for representing species extracted by `challenger-workflows`.
"""
from typing import Optional

from pydantic import BaseModel


class SpeciesBase(BaseModel):
    id: str
    matched_canonical_full_name: Optional[str] = None


class SpeciesSummaryInDB(SpeciesBase):
    class Config:
        orm_mode = True


class SpeciesSummary(SpeciesSummaryInDB):
    pass


class SpeciesDetailsBase(SpeciesBase):
    matched_name: str
    matched_canonical_simple_name: Optional[str] = None
    common_name: Optional[str] = None
    classification_path: Optional[str]
    classification_ranks: Optional[str]
    classification_ids: Optional[str]
    data_source_id: int


class SpeciesCreate(SpeciesDetailsBase):
    pass


class SpeciesUpdate(SpeciesDetailsBase):
    pass


class SpeciesDetailsInDB(SpeciesDetailsBase):
    class Config:
        orm_mode = True


class SpeciesDetails(SpeciesDetailsInDB):
    pass
