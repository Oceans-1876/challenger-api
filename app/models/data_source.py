from typing import TYPE_CHECKING, List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models import Species


class DataSource(Base):
    """The data source used by Global Names"""

    __tablename__ = "data_sources"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(150), nullable=False, index=True)

    species: List["Species"] = relationship(
        "Species", back_populates="data_source", cascade="all, delete"
    )
