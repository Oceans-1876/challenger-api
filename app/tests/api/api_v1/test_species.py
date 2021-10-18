from typing import Dict
from fastapi.testclient import TestClient
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import get_settings

import requests

settings = get_settings()

from fastapi import FastAPI, Request


def test_read_species(client: TestClient, db: Session) -> None:
    # data = {"email": username, "password": password}
    r = client.get(f"{settings.API_V1_STR}/species/")
    assert 200 <= r.status_code < 300
    # created_user = r.json()
    species = crud.species.get_multi(db)
    assert species


"""def test_create_user_new_email(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=username)
    assert user
    assert user.email == created_user["email"]"""
