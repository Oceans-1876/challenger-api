"""Pydantic models for representing data sources used by
[Global Names](https://verifier.globalnames.org/data_sources).
"""
from typing import List

from pydantic import BaseModel

from app.schemas.species import SpeciesID


class DataSourceBase(BaseModel):
    id: int
    title: str


class DataSourceCreate(DataSourceBase):
    pass


class DataSourceUpdate(DataSourceBase):
    pass


class DataSourceInDBIDOnly(DataSourceBase):
    species: List[SpeciesID]

    class Config:
        orm_mode = True


class DataSourceIDOnly(DataSourceInDBIDOnly):
    pass
