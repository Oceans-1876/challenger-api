from typing import Dict
from fastapi.testclient import TestClient
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import get_settings

import requests

settings = get_settings()

from fastapi import FastAPI, Request


def test_read_stations(client: TestClient, db: Session) -> None:
    # data = {"email": username, "password": password}
    r = client.get(f"{settings.API_V1_STR}/stations/")
    assert 200 <= r.status_code < 300
    # created_user = r.json()
    stations = crud.species.get_multi(db)
    assert stations

def test_read_station_by_id(client: TestClient, station_id: str, db: Session) -> None:
    # data = {"email": username, "password": password}
    r = client.get(f"{settings.API_V1_STR}/{station_id}")
    assert 200 <= r.status_code < 300
    # created_user = r.json()
    station = crud.species.get_multi(db)
    assert station