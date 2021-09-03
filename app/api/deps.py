from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import get_settings
from app.db.session import SessionLocal

settings = get_settings()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    """get_current_user fetches the currently logged in user by using the generated token for the particular user.

    Parameters
    ----------
    db : Session
        The database session, by default Depends(get_db)
    token : str
        The token is extracted form the users system local storage by the OAuth2PasswordBearer function,
        by default Depends(reusable_oauth2)

    Returns
    -------
    models.User
        If the User is found in the database then it is returned, otherwise, en exception is raised.

    Raises
    ------
    HTTPException
        Raised when Invalid credentials are provided and the jwt can't decode the token.
    HTTPException
        Rasied when the extracted information of the user from the token cannot fetch a valid user from the database.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """get_current_active_user

    Parameters
    ----------
    current_user : models.User
        Current User from the database, by default Depends(get_current_user)

    Returns
    -------
    models.User
        Active User is returned upon validation.

    Raises
    ------
    HTTPException
        Raised when the User found, isn't active.
    """
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """get_current_active_superuser

    Parameters
    ----------
    current_user : models.User
        Current User from the database, by default Depends(get_current_user)

    Returns
    -------
    models.User
        Active SuperUser is returned upon validation.

    Raises
    ------
    HTTPException
        Raised when the User found, isn't an active SuperUser.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
