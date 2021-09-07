"""Pydantic models for representing GeoJSON objects.
"""
from typing import List

from pydantic import BaseModel, Field


class Point(BaseModel):
    type: str = "Point"
    coordinates: List[float] = Field(min_items=2, max_items=2)
