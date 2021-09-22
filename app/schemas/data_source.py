"""Pydantic models for representing data sources used by
[Global Names](https://verifier.globalnames.org/data_sources).
"""
from typing import List

from pydantic import BaseModel

from app.schemas.species import Species


class DataSourceBase(BaseModel):
    id: int
    title: str


class DataSourceCreate(DataSourceBase):
    pass


class DataSourceUpdate(DataSourceBase):
    pass


class DataSourceInDB(DataSourceBase):
    species: List[Species]

    class Config:
        orm_mode = True


class DataSource(DataSourceInDB):
    pass
