"""Pydantic models for representing species extracted by `challenger-workflows`.
"""
from typing import List

from pydantic import BaseModel

from .pagination import PaginationBase


class SpeciesCommonNamesBase(BaseModel):
    id: str
    language: str
    name: str
    species_id: str


class SpeciesCommonNamesCreate(SpeciesCommonNamesBase):
    pass


class SpeciesCommonNamesUpdate(SpeciesCommonNamesBase):
    pass


class SpeciesCommonNamesInDB(SpeciesCommonNamesBase):
    class Config:
        orm_mode = True


class SpeciesCommonNames(SpeciesCommonNamesInDB):
    pass


class SpeciesCommonNamesPagination(PaginationBase):
    results: List[SpeciesCommonNames]
