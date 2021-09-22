# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.data_source import DataSource  # noqa
from app.models.species import Species  # noqa
from app.models.station import Station  # noqa
from app.models.user import User  # noqa
