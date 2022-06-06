"""Pydantic models for representing species extracted by `challenger-workflows`.
"""
from typing import List, Optional

from pydantic import BaseModel

from app.schemas import PaginationBase


class SpeciesSynonymsBase(BaseModel):
    id: str
    scientific_name: Optional[str]
    outlink: Optional[str]
    species_id: str


class SpeciesSynonymsCreate(SpeciesSynonymsBase):
    pass


class SpeciesSynonymsUpdate(SpeciesSynonymsBase):
    pass


class SpeciesSynonymsInDB(SpeciesSynonymsBase):
    class Config:
        orm_mode = True


class SpeciesSynonyms(SpeciesSynonymsInDB):
    pass


class SpeciesSynonymsPagination(PaginationBase):
    results: List[SpeciesSynonyms]
