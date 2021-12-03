from typing import Optional
from pydantic import BaseModel


class PaginationBase(BaseModel):
    count: int
    first_page: str
    last_page: str
    previous_page: Optional[str]
    next_page: Optional[str]
