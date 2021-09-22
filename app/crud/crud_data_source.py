from app.crud.base import CRUDBase
from app.models import DataSource
from app.schemas import DataSourceCreate, DataSourceUpdate


class CRUDDataSource(CRUDBase[DataSource, DataSourceCreate, DataSourceUpdate]):
    pass


data_source = CRUDDataSource(DataSource)
