import argparse
import csv
import json
import logging
from datetime import datetime
from functools import reduce
from typing import Dict, List

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
    def __init__(self, test_mode: bool) -> None:
        self.db = SessionLocal()
        self.data_sources: Dict[int, models.DataSource] = {}

        species_path = (
            PROJECT_ROOT
            / "data"
            / ("Oceans1876" if not test_mode else "Oceans1876_test")
            / "species.json"
        )

        species_extra_path = (
            PROJECT_ROOT / "data" / "Oceans1876" / "index_species_verified_extra.json"
        )

        stations_path = (
            PROJECT_ROOT
            / "data"
            / ("Oceans1876" if not test_mode else "Oceans1876_test")
            / "stations.json"
        )

        data_sources_path = PROJECT_ROOT / "data" / "Oceans1876" / "data_sources.json"

        hathitrust_path = PROJECT_ROOT / "data" / "HathiTrust" / "sections.csv"

        with open(species_path, "r") as f:
            self.species = json.load(f)["species"]
        with open(species_extra_path, "r") as f:
            self.species_extra = json.load(f)["species"]
        with open(stations_path, "r") as f:
            self.stations = json.load(f)
        with open(data_sources_path, "r") as f:
            self.data_sources_dict = json.load(f)
        with open(hathitrust_path, "r") as f:
            self.hathitrust_urls: Dict[str, str] = reduce(
                lambda all_urls, section_props: all_urls.update(
                    {section_props["Section"]: section_props["Url"]}
                )
                or all_urls,
                csv.DictReader(f),
                {},
            )

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

    def import_data_sources(self) -> None:
        logger.info("Importing data sources")

        for data_source_data in self.data_sources_dict.values():
            logger.info(f"Importing Data Source: {data_source_data['title']}")

            obj_in = {
                "id": data_source_data["id"],
                "title": data_source_data["title"],
                "title_short": data_source_data["title_short"],
                "description": data_source_data.get("description"),
                "curation": data_source_data["curation"],
                "record_count": data_source_data.get("record_count"),
                "updated_at": data_source_data["updated_at"],
                "is_out_link_ready": data_source_data["is_outlink_ready"],
                "home_url": data_source_data.get("home_url"),
                "url_template": data_source_data.get("urls", {}).get("web"),
            }

            data_source = crud.data_source.get(self.db, data_source_data["id"])
            if data_source:
                data_source = crud.data_source.update(
                    self.db,
                    obj_in=schemas.DataSourceUpdate(**obj_in),
                    db_obj=data_source,
                )
            else:
                data_source = crud.data_source.create(
                    self.db, obj_in=schemas.DataSourceCreate(**obj_in)
                )
            self.data_sources[data_source.id] = data_source

    def import_species(self) -> None:
        logger.info("Importing species")

        for record_id, sp in self.species.items():
            logger.info(f"Importing species: {sp['name']} ({record_id})")
            sp_data = sp.get("bestResult")
            if not sp_data:
                continue
            data_source = self.data_sources[sp_data["dataSourceId"]]
            records = self.species_extra.get(record_id, {}).get("records", [])
            synonyms = self.species_extra.get(record_id, {}).get("synonyms", [])
            common_names = self.species_extra.get(record_id, {}).get("common_names", [])

            obj_in = {
                "id": sp["id"],
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

            species = crud.species.get(self.db, sp["id"])
            if species:
                inserted_sp = crud.species.update(
                    self.db, obj_in=schemas.SpeciesUpdate(**obj_in), db_obj=species
                )
            else:
                inserted_sp = crud.species.create(
                    self.db, obj_in=schemas.SpeciesCreate(**obj_in)
                )

            for record in records:

                sp_extra_in = {
                    "id": str(record["id"]),
                    "scientific_name": f"{record['scientificname']} {record['authority']}",
                    "status": True if record["status"] == "accepted" else False,
                    "unaccepted_reason": record["unacceptreason"],
                    "valid_name": f"{record['valid_name']} {record['valid_authority']}",
                    "lsid": record["lsid"],
                    "isBrackish": record["isBrackish"]
                    if record["isBrackish"] is not None
                    else False,
                    "isExtinct": record["isExtinct"]
                    if record["isExtinct"] is not None
                    else False,
                    "isFreshwater": record["isFreshwater"]
                    if record["isFreshwater"] is not None
                    else False,
                    "isMarine": record["isMarine"]
                    if record["isMarine"] is not None
                    else False,
                    "isTerrestrial": record["isTerrestrial"]
                    if record["isTerrestrial"] is not None
                    else False,
                    "species_id": inserted_sp.id,
                }

                species_ex = crud.species_extra.get(self.db, str(record["id"]))
                if species_ex:
                    crud.species_extra.update(
                        self.db,
                        obj_in=schemas.SpeciesExtraUpdate(**sp_extra_in),
                        db_obj=species_ex,
                    )
                else:
                    crud.species_extra.create(
                        self.db, obj_in=schemas.SpeciesExtraCreate(**sp_extra_in)
                    )

            for syn in synonyms:
                sp_syn_in = {
                    "id": str(syn["id"]),
                    "scientific_name": f"{syn['scientificname']} {syn['authority']}",
                    "outlink": syn["url"],
                    "species_id": inserted_sp.id,
                }

                species_syn = crud.species_synonyms.get(self.db, str(syn["id"]))
                if species_syn:
                    crud.species_synonyms.update(
                        self.db,
                        obj_in=schemas.SpeciesSynonymsUpdate(**sp_syn_in),
                        db_obj=species_syn,
                    )
                else:
                    crud.species_synonyms.create(
                        self.db, obj_in=schemas.SpeciesSynonymsCreate(**sp_syn_in)
                    )

            for comm_name in common_names:
                sp_comm_name_in = {
                    "id": sp["id"],
                    "language": comm_name["language"],
                    "name": comm_name["vernacular"],
                    "species_id": inserted_sp.id,
                }

                species_comm_name = crud.species_common_names.get(self.db, sp["id"])
                if species_comm_name:
                    crud.species_common_names.update(
                        self.db,
                        obj_in=schemas.SpeciesCommonNamesUpdate(**sp_comm_name_in),
                        db_obj=species_comm_name,
                    )
                else:
                    crud.species_common_names.create(
                        self.db,
                        obj_in=schemas.SpeciesCommonNamesCreate(**sp_comm_name_in),
                    )

    def get_hathitrust_url(self, ranges: List[List[str]]) -> List[str]:
        urls = []
        for section_name, pages in ranges:
            first_page = int(pages.split("-")[0]) - 1
            urls.append(
                f"{self.hathitrust_urls[section_name]}?urlappend=%3Bseq={first_page}"
            )
        return urls

    def import_stations(self) -> None:
        logger.info("Importing stations")

        # First remove all stations species relations
        models.stations_species_table.delete()

        for idx, station_data in enumerate(self.stations, start=1):
            logger.info(f"Importing Station {station_data['Station']}")

            longitude = station_data["Decimal Longitude"]
            latitude = station_data["Decimal Latitude"]
            coordinates = f"POINT ({longitude} {latitude})"

            obj_in = {
                "name": station_data["Station"],
                "order": idx,
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
                "bottom_water_temp_c": station_data.get("Bottom water temperature (C)"),
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
                "hathitrust_urls": self.get_hathitrust_url(
                    station_data["HathiTrust"]["Range"]
                ),
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
                        self.db, self.species[sp["recordId"]]["id"]
                    )
                    if species:
                        station.species.append(species)


if __name__ == "__main__":
    logger.info("Creating initial data")
    data = Data(test_mode=args.testing)
    data.create_all()
    logger.info("Initial data created")
