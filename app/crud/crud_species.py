from app.crud.base import CRUDBase
from app.models import Species
from app.schemas import SpeciesCreate, SpeciesUpdate


class CRUDSpecies(CRUDBase[Species, SpeciesCreate, SpeciesUpdate]):
    pass


species = CRUDSpecies(Species)
