"""Pydantic models for representing data sources used by
[Global Names](https://verifier.globalnames.org/data_sources).
"""
from typing import List

from pydantic import BaseModel

from app.schemas.species import SpeciesSummary


class DataSourceBase(BaseModel):
    id: int
    title: str


class DataSourceSummaryInDB(DataSourceBase):
    class Config:
        orm_mode = True


class DataSourceSummary(DataSourceSummaryInDB):
    pass


class DataSourceCreate(DataSourceBase):
    pass


class DataSourceUpdate(DataSourceBase):
    pass


class DataSourceDetailsInDB(DataSourceBase):
    species: List[SpeciesSummary]

    class Config:
        orm_mode = True


class DataSourceDetails(DataSourceDetailsInDB):
    pass