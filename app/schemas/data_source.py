"""Pydantic models for representing data sources used by
[Global Names](https://verifier.globalnames.org/data_sources).
"""
from app.schemas.pagination import PaginationBase
from datetime import date  # noqa
from typing import Optional, List

from pydantic import BaseModel


class DataSourceBase(BaseModel):
    id: int
    title: str


class DataSourceSummaryInDB(DataSourceBase):
    class Config:
        orm_mode = True


class DataSourceSummary(DataSourceSummaryInDB):
    pass


class DataSourceSummaryPagination(PaginationBase):
    results: List[DataSourceSummary]


class DataSourceDetailsBase(DataSourceBase):
    title_short: str
    description: Optional[str]
    curation: str
    record_count: Optional[int]
    updated_at: date
    is_out_link_ready: bool
    home_url: Optional[str]
    url_template: Optional[str]


class DataSourceCreate(DataSourceDetailsBase):
    pass


class DataSourceUpdate(DataSourceDetailsBase):
    pass


class DataSourceDetailsInDB(DataSourceDetailsBase):
    class Config:
        orm_mode = True


class DataSourceDetails(DataSourceDetailsInDB):
    pass
