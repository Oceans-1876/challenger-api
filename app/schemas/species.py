"""Pydantic models for representing species extracted by `challenger-workflows`.
"""
from typing import List, Optional

from pydantic import BaseModel

from app.schemas import PaginationBase


# Species Synonyms
class SpeciesSynonymsBase(BaseModel):
    id: str
    scientific_name: Optional[str]
    outlink: Optional[str]
    species_id: str


class SpeciesSynonymsCreate(SpeciesSynonymsBase):
    pass


class SpeciesSynonymsUpdate(SpeciesSynonymsBase):
    pass


class SpeciesSynonymsInDB(SpeciesSynonymsBase):
    class Config:
        orm_mode = True


class SpeciesSynonyms(SpeciesSynonymsInDB):
    pass


class SpeciesSynonymsPagination(PaginationBase):
    results: List[SpeciesSynonyms]


# Species Common Names
class SpeciesCommonNamesBase(BaseModel):
    id: str
    language: str
    name: str
    species_id: str


class SpeciesCommonNamesCreate(SpeciesCommonNamesBase):
    pass


class SpeciesCommonNamesUpdate(SpeciesCommonNamesBase):
    pass


class SpeciesCommonNamesInDB(SpeciesCommonNamesBase):
    class Config:
        orm_mode = True


class SpeciesCommonNames(SpeciesCommonNamesInDB):
    pass


class SpeciesCommonNamesPagination(PaginationBase):
    results: List[SpeciesCommonNames]


# Species Extra
class SpeciesExtraBase(BaseModel):
    id: str
    scientific_name: Optional[str]
    status: bool


class SpeciesExtraSummaryInDB(SpeciesExtraBase):
    class Config:
        orm_mode = True


class SpeciesExtraSummary(SpeciesExtraSummaryInDB):
    pass


class SpeciesExtraSummaryPagination(PaginationBase):
    results: List[SpeciesExtraSummary]


class SpeciesExtraDetailsBase(SpeciesExtraBase):
    unaccepted_reason: Optional[str]
    valid_name: Optional[str]
    lsid: Optional[str]
    isBrackish: bool
    isExtinct: bool
    isFreshwater: bool
    isMarine: bool
    isTerrestrial: bool

    species_id: str


class SpeciesExtraCreate(SpeciesExtraDetailsBase):
    pass


class SpeciesExtraUpdate(SpeciesExtraDetailsBase):
    pass


class SpeciesExtraDetailsInDB(SpeciesExtraDetailsBase):
    class Config:
        orm_mode = True


class SpeciesExtraDetails(SpeciesExtraDetailsInDB):
    pass


# Species
class SpeciesBase(BaseModel):
    id: str
    record_id: str
    matched_canonical_full_name: Optional[str] = None
    current_name: Optional[str]


class SpeciesSummaryInDB(SpeciesBase):
    class Config:
        orm_mode = True


class SpeciesSummary(SpeciesSummaryInDB):
    pass


class SpeciesFuzzySummary(SpeciesSummaryInDB):
    species_synonyms: List[SpeciesSynonyms]
    species_common_names: List[SpeciesCommonNames]

    class Config:
        orm_mode = True


class SpeciesSummaryPagination(PaginationBase):
    results: List[SpeciesSummary]


class SpeciesDetailsBase(SpeciesBase):
    current_record_id: str
    matched_name: str
    matched_canonical_simple_name: Optional[str] = None
    current_name: Optional[str] = None
    current_canonical_simple_name: Optional[str] = None
    current_canonical_full_name: Optional[str] = None
    common_name: Optional[str] = None
    classification_path: Optional[str]
    classification_ranks: Optional[str]
    classification_ids: Optional[str]
    outlink: Optional[str]
    data_source_id: int


class SpeciesCreate(SpeciesDetailsBase):
    pass


class SpeciesUpdate(SpeciesDetailsBase):
    pass


class SpeciesDetailsInDB(SpeciesDetailsBase):
    species_extra: List[SpeciesExtraDetails]
    species_synonyms: List[SpeciesSynonyms]
    species_common_names: List[SpeciesCommonNames]

    class Config:
        orm_mode = True


class SpeciesDetails(SpeciesDetailsInDB):
    pass
