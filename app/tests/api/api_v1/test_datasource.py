from typing import Dict
from fastapi.testclient import TestClient
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import get_settings

import requests

settings = get_settings()

from fastapi import FastAPI, Request


# def test_read_datasource(client: TestClient, db: Session) -> None:
#     # data = {"email": username, "password": password}
#     r = client.get(f"{settings.API_V1_STR}/data_source/")
#     assert 200 <= r.status_code < 300
#     # created_user = r.json()
#     data_sources = crud.species.get_multi(db)
#     assert data_sources

# def test_read_datasource_by_id(client: TestClient, data_source_id: str, db: Session) -> None:
#     # data = {"email": username, "password": password}
#     r = client.get(f"{settings.API_V1_STR}/{data_source_id}")
#     assert 200 <= r.status_code < 300
#     # created_user = r.json()
#     data_source = crud.species.get_multi(db)
#     assert data_source
