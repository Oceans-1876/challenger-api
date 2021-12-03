"""Pydantic models for representing species extracted by `challenger-workflows`.
"""
from typing import Optional, List

from pydantic import BaseModel
from app.schemas import PaginationBase


class SpeciesBase(BaseModel):
    id: str
    record_id: str
    matched_canonical_full_name: Optional[str] = None


class SpeciesSummaryInDB(SpeciesBase):
    class Config:
        orm_mode = True


class SpeciesSummary(SpeciesSummaryInDB):
    pass


class SpeciesSummaryPagination(PaginationBase):
    results: List[SpeciesSummary]


class SpeciesDetailsBase(SpeciesBase):
    current_record_id: str
    matched_name: str
    matched_canonical_simple_name: Optional[str] = None
    current_name: Optional[str] = None
    current_canonical_simple_name: Optional[str] = None
    current_canonical_full_name: Optional[str] = None
    common_name: Optional[str] = None
    classification_path: Optional[str]
    classification_ranks: Optional[str]
    classification_ids: Optional[str]
    outlink: Optional[str]
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
