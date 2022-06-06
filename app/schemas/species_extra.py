"""Pydantic models for representing species extracted by `challenger-workflows`.
"""
from typing import List, Optional

from pydantic import BaseModel

from app.schemas import PaginationBase


class SpeciesExtraBase(BaseModel):
    id: str
    scientific_name: Optional[str]
    status: bool


class SpeciesExtraSummaryInDB(SpeciesExtraBase):
    class Config:
        orm_mode = True


class SpeciesExtraSummary(SpeciesExtraSummaryInDB):
    pass


class SpeciesExtraSummaryPagination(PaginationBase):
    results: List[SpeciesExtraSummary]


class SpeciesExtraDetailsBase(SpeciesExtraBase):
    unaccepted_reason: Optional[str]
    valid_name: Optional[str]
    lsid: Optional[str]
    isBrackish: bool
    isExtinct: bool
    isFreshwater: bool
    isMarine: bool
    isTerrestrial: bool

    species_id: str


class SpeciesExtraCreate(SpeciesExtraDetailsBase):
    pass


class SpeciesExtraUpdate(SpeciesExtraDetailsBase):
    pass


class SpeciesExtraDetailsInDB(SpeciesExtraDetailsBase):
    class Config:
        orm_mode = True


class SpeciesExtraDetails(SpeciesExtraDetailsInDB):
    pass
