from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models import User
from app.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """get_by_email function fetches a User from the
            Database based on their email.

        Parameters
        ----------
        db : Session
            The database session.
        email : str
            email of the user whose record is to be fetched.

        Returns
        -------
        Optional[User]
            User instance or None is returned.
        """
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:  # type: ignore[override] # noqa E501
        """create function creates a user from incoming object.

        Parameters
        ----------
        db : Session
            The database session.
        obj_in : UserCreate
            Predefined User creation schema object containing
            data to be added to the database.

        Returns
        -------
        User
            The created instance of User.
        """
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """update the User password.

        Parameters
        ----------
        db : Session
            The database session.
        db_obj : User
             The database object User to update.
        obj_in : Union[UserUpdate, Dict[str, Any]]
            Either a UserUpdate schema object or a Dictionary of
            new values for the existing object to update from.

        Returns
        -------
        User
            The updated user object.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """authenticate

        Parameters
        ----------
        db : Session
            The database session.
        email : str
            User entered email
        password : str
            User entered password

        Returns
        -------
        Optional[User]
            None if authentication fails else, User instance.
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """is_active returns active status of the user.

        Parameters
        ----------
        user : User
            An instance of User class

        Returns
        -------
        bool
            Attribute value.
        """
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """is_superuser return superuser status of a user.

        Parameters
        ----------
        user : User
            An instance of User Class

        Returns
        -------
        bool
            Attribute value.
        """
        return user.is_superuser


user = CRUDUser(User)
