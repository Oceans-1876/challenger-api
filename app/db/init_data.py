import argparse
import json
import logging
from datetime import datetime
from typing import Dict, Optional

from app import crud, models, schemas
from app.core.config import PROJECT_ROOT, get_settings
from app.db import base  # noqa: F401
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Data Import")

settings = get_settings()

parser = argparse.ArgumentParser()
parser.add_argument("--testing", type=bool, default=False)
args = parser.parse_args()


class Data:
    def __init__(self, test_mode) -> None:
        self.db = SessionLocal()
        self.data_sources: Dict[str, models.DataSource] = {}

        self.species_path = (
            PROJECT_ROOT
            / "data"
            / ("Oceans1876" if not test_mode else "Oceans1876_subset")
            / "species.json"
        )

        self.stations_path = (
            PROJECT_ROOT
            / "data"
            / ("Oceans1876" if not test_mode else "Oceans1876_subset")
            / "stations.json"
        )

        self.datasources_path = (
            PROJECT_ROOT / "data" / "Oceans1876" / "data_sources.json"
        )

        with open(self.species_path, "r") as f:
            self.species = json.load(f)["species"]
        with open(self.stations_path, "r") as f:
            self.stations = json.load(f)
        with open(self.datasources_path, "r") as f:
            self.data_sources_list = json.load(f)

    def create_all(self) -> None:
        self.create_superuser()
        self.import_data_sources()
        self.import_species()
        self.import_stations()

    def create_superuser(self) -> None:
        logger.info("Creating superuser")
        user = crud.user.get_by_email(self.db, email=settings.FIRST_SUPERUSER)

        if not user:
            user_in = schemas.UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            crud.user.create(self.db, obj_in=user_in)
            logger.info(f"Superuser created: {settings.FIRST_SUPERUSER}")
        else:
            logger.info(f"Superuser already exists: {settings.FIRST_SUPERUSER}")

    def get_data_source(
        self,
        data_source_id: int
        # , data_source_name: str
    ) -> Optional[models.DataSource]:
        data_source = crud.data_source.get(self.db, data_source_id)
        if data_source:
            return data_source
        return None
        # logger.info(f"Creating data source: {data_source_name}")
        # return crud.data_source.create(
        #     self.db,
        #     obj_in=schemas.DataSourceCreate(
        #         **{"id": data_source_id, "title": data_source_name}
        #     ),
        # )

    def import_data_sources(self) -> None:
        logger.info("Importing data sources")

        for data_source in self.data_sources_list:
            logger.info(f"Importing Data Soruce: {data_source['title']}")

            obj_in = {
                "id": data_source["id"],
                "title": data_source["title"],
                "title_short": data_source["titleShort"],
                "description": data_source.get("description"),
                "curation": data_source["curation"],
                "record_count": data_source.get("recordCount"),
                "updated_at": data_source["updatedAt"],
                "is_out_link_ready": data_source["isOutlinkReady"],
                "home_url": data_source.get("homeURL"),
                "url_template": data_source.get("URL_template"),
            }

            data = self.get_data_source(data_source["id"])
            if not data:
                crud.data_source.create(
                    self.db, obj_in=schemas.DataSourceCreate(**obj_in)
                )
            else:
                crud.data_source.update(
                    self.db, obj_in=schemas.DataSourceUpdate(**obj_in), db_obj=data
                )

    def import_species(self) -> None:
        logger.info("Importing species")

        for record_id, sp in self.species.items():
            logger.info(f"Importing species: {sp['input']} ({record_id})")
            sp_data = sp.get("bestResult")
            if not sp_data:
                continue
            data_source = self.data_sources.setdefault(
                sp_data["dataSourceId"],
                self.get_data_source(sp_data["dataSourceId"]),
            )

            obj_in = {
                "id": sp["inputId"],
                "record_id": sp_data["recordId"],
                "current_record_id": sp_data["currentRecordId"],
                "matched_name": sp_data["matchedName"],
                "matched_canonical_simple_name": sp_data.get("matchedCanonicalSimple"),
                "matched_canonical_full_name": sp_data.get("matchedCanonicalFull"),
                "current_name": sp_data.get("currentName"),
                "current_canonical_simple_name": sp_data.get("currentCanonicalSimple"),
                "current_canonical_full_name": sp_data.get("currentCanonicalFull"),
                "common_name": "",
                "classification_path": sp_data.get("classificationPath"),
                "classification_ranks": sp_data.get("classificationRanks"),
                "classification_ids": sp_data.get("classificationIds"),
                "outlink": sp_data.get("outlink"),
                "data_source_id": data_source.id,
            }

            species = crud.species.get(self.db, sp["inputId"])
            if species:
                crud.species.update(
                    self.db, obj_in=schemas.SpeciesUpdate(**obj_in), db_obj=species
                )
            else:
                crud.species.create(self.db, obj_in=schemas.SpeciesCreate(**obj_in))

    def import_stations(self) -> None:
        logger.info("Importing stations")

        # First remove all stations species relations
        models.stations_species_table.delete()

        for station_data in self.stations:
            logger.info(f"Importing Station {station_data['Station']}")

            longitude = station_data["Decimal Longitude"]
            latitude = station_data["Decimal Latitude"]
            coordinates = f"POINT ({longitude} {latitude})"

            obj_in = {
                "name": station_data["Station"],
                "sediment_sample": station_data.get("Sediment sample"),
                "coordinates": coordinates,
                "location": station_data["Location"],
                "water_body": station_data["Water body"],
                "sea_area": station_data.get("Sea Area"),
                "place": station_data.get("Place"),
                "date": datetime.strptime(station_data["Date"], "%d/%m/%Y"),
                "fao_area": station_data["FAOarea"],
                "gear": station_data.get("Gear"),
                "depth_fathoms": station_data.get("Depth (fathoms)"),
                "bottom_water_temp_c": station_data.get(
                    "Bottom water temperature (C) "
                ),
                "bottom_water_depth_fathoms": station_data.get(
                    "Bottom water depth D (fathoms)"
                ),
                "specific_gravity_at_bottom": station_data.get(
                    "Specific Gravity at bottom"
                ),
                "surface_temp_c": station_data.get("Surface temp (C)"),
                "specific_gravity_at_surface": station_data.get(
                    "Specific Gravity at surface"
                ),
                "water_temp_c_at_depth_fathoms": station_data["Temp (F) at Fathoms"],
                "text": station_data["HathiTrust"]["Text"],
            }

            station = crud.station.get(self.db, station_data["Station"])
            if station:
                station = crud.station.update(self.db, obj_in=obj_in, db_obj=station)
            else:
                station = crud.station.create(self.db, obj_in=obj_in)

            station_species = set()
            for sp in station_data["Species"]:
                if sp.get("recordId") and sp["recordId"] not in station_species:
                    station_species.add(sp["recordId"])
                    species = crud.species.get(
                        self.db, self.species[sp["recordId"]]["inputId"]
                    )
                    if species:
                        station.species.append(species)


if __name__ == "__main__":
    logger.info("Creating initial data")
    data = Data(test_mode=args.testing)
    data.create_all()
    logger.info("Initial data created")
