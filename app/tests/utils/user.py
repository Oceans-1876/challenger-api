from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import get_settings
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string

settings = get_settings()


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    """user_authentication_headers This function returns the Authorization token as headers.

    Parameters
    ----------
    client : TestClient
        A TestClient instance to emulate as a client.
    email : str
        Email ID of the User whose token is to be obtained.
    password : str
        Password of the User whose token is to be obtained.

    Returns
    -------
    Dict[str, str]
        Header containing authentication parameter is returned.
    """
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    """create_random_user This function inserts a random user in the database.

    Parameters
    ----------
    db : Session
        The database session.

    Returns
    -------
    User
        Returns the created User instance.
    """
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db=db, obj_in=user_in)
    return user


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """authentication_token_from_email Return a valid token for the user with given email.
    If the user doesn't exist it is created first.

    Parameters
    ----------
    client : TestClient
        A TestClient instance to emulate as a client.
    email : str

    db : Session
        The database session.

    Returns
    -------
    Dict[str, str]
        Authentication header is returned.
    """
    password = random_lower_string()
    user = crud.user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreate(username=email, email=email, password=password)
        user = crud.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = crud.user.update(db, db_obj=user, obj_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
