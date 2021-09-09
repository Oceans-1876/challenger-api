from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import get_settings
from app.utils.email import send_new_account_email

settings = get_settings()

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """read_users: Retrieve users.

    Parameters
    ----------
    db : Session
        The database session, by default Depends(deps.get_db)
    skip : int, optional
        The offset to start fetching records from, by default 0
    limit : int, optional
        The number of records to return, by default 100
    current_user : models.User, optional
        Instance of User having SuperUser privileges,
        by default Depends(deps.get_current_active_superuser)

    Returns
    -------
    Any
        List of Users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """create_user: Create new user.

    Parameters
    ----------
    user_in : schemas.UserCreate
        Incoming user data which is to be added to the database.
    db : Session
        The database session, by default Depends(deps.get_db)
    current_user : models.User, optional
         Instance of User having SuperUser privileges,
         by default Depends(deps.get_current_active_superuser)

    Returns
    -------
    Any
        Instance of the created User.

    Raises
    ------
    HTTPException
        Raised when the user tries to create account with
        existing email in the database.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """update_user_me: Update own user.

    Parameters
    ----------
    db : Session
        The database session, by default Depends(deps.get_db)
    password : str, optional
        Password to be updated by the user, by default Body(None)
    full_name : str, optional
        Full name to be updated by the user, by default Body(None)
    email : EmailStr, optional
        Email to be updated by the user, by default Body(None)
    current_user : models.User, optional
        An instance of User who is an active user,
        by default Depends(deps.get_current_active_user)

    Returns
    -------
    Any
        Updated instance of the User.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """read_user_me: Get current user.

    Parameters
    ----------
    db : Session, optional
        The database session, by default Depends(deps.get_db)
    current_user : models.User, optional
        An instance of User who is an active user,
        by default Depends(deps.get_current_active_user)

    Returns
    -------
    Any
        Instance of the User.
    """
    return current_user


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """create_user_open: Create new user without the need to be logged in.

    Parameters
    ----------
    db : Session
        The database session, by default Depends(deps.get_db)
    password : str, optional
        Password of the open user, by default Body(...)
    email : EmailStr, optional
        Email of the open user, by default Body(...)
    full_name : str, optional
        Full name of the user, by default Body(None)

    Returns
    -------
    Any
        Instance of the created User.

    Raises
    ------
    HTTPException
        Raised if open user registeration is not allowed on
        the server or if the username is already in the system.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """read_user_by_id: Get a specific user by id.

    Parameters
    ----------
    user_id : int
        Primary key of the User to be fetched.
    current_user : models.User, optional
        An instance of User who is an active user,
        by default Depends(deps.get_current_active_user)
    db : Session, optional
        The database session, by default Depends(deps.get_db)

    Returns
    -------
    Any
        Instance of the fetched User if found.

    Raises
    ------
    HTTPException
        Raised when a superuser has not initiated the request.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """update_user: Update a user.

    Parameters
    ----------
    user_id : int
        Primary key of the User to be updated.
    user_in : schemas.UserUpdate
        Schema for the user data to be updated.
    db : Session, optional
        The database session, by default Depends(deps.get_db)
    current_user : models.User, optional
        Instance of the User having SuperUser privileges,
        by default Depends(deps.get_current_active_superuser)

    Returns
    -------
    Any
        Instance of the updated User.

    Raises
    ------
    HTTPException
        Raised when the User isn't found.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
