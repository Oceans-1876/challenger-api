from app.crud.base import CRUDBase
from app.models import Station
from app.schemas import StationCreate, StationUpdate


class CRUDStation(CRUDBase[Station, StationCreate, StationUpdate]):
    pass


station = CRUDStation(Station)
