from app.crud.base import CRUDBase
from app.models import SpeciesSynonyms
from app.schemas import (
    SpeciesSynonymsCreate,
    SpeciesSynonymsPagination,
    SpeciesSynonymsUpdate,
)


class CRUDSpeciesSynonyms(
    CRUDBase[
        SpeciesSynonyms,
        SpeciesSynonymsCreate,
        SpeciesSynonymsUpdate,
        SpeciesSynonymsPagination,
    ]
):
    pass


species_synonyms = CRUDSpeciesSynonyms(SpeciesSynonyms)
