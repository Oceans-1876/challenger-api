from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models import Species


class SpeciesCommonNames(Base):
    __tablename__ = "species_common_names"

    id: str = Column(String(length=300), primary_key=True, index=True)
    language: str = Column(String(length=300), nullable=False)
    name: str = Column(String(length=300), nullable=False)

    species_id: str = Column(String, ForeignKey("species.id"), nullable=False)

    species: "Species" = relationship("Species", back_populates="species_common_names")
