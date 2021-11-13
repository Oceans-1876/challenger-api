from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Query, Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD)."""

    def __init__(self, model: Type[ModelType]):
        """

        Parameters
        ----------
        model : BaseModel
                A SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get a database record by id.

        Parameters
        ----------
        db : Session
            The database session.
        id : Any
            The object id to fetch from the database.

        Returns
        -------
        Optional[ModelType]
            An instance of the SQLAlchemy for the fetched object, if it exists.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def order_by(self, query: Query, *, order_by: Optional[List[str]] = None) -> Query:
        """Order the query by the given list of columns.

        Parameters
        ----------
        query : Query
        order_by : Optional[List[str]]
            List of column names to order by. If a column name is prefixed with '-',
            order it in descending order.

        Returns
        -------
        Query
            The ordered query.
        """
        order_by_args = []
        if order_by:
            for column in order_by:
                if column.startswith("-"):
                    column_name = column[1:]
                    order_func = desc
                else:
                    column_name = column
                    order_func = asc

                for entity in query.column_descriptions:
                    if hasattr(entity["type"], column_name):
                        # TODO: test this for join queries where the models/entities
                        #       have columns with the same name.
                        #       The query probably fails or won't work, which means we
                        #       we have to construct column names differently.
                        order_by_args.append(
                            order_func(getattr(entity["type"], column_name))
                        )
                        break

        return query.order_by(*order_by_args)

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[List[str]] = None,
    ) -> List[ModelType]:
        """Get multiple records from the database.

        Parameters
        ----------
        db : Session
            The database session.
        skip: int
            The offset to start fetching records from.
        limit: int
            The number of records to return.
        order_by: Optional[List[str]]
            List of column names to order by. If a column name is prefixed with '-',
            order it in descending order.

        Returns
        -------
        List[ModelType]
            A list of SQLAlchemy model instances from the query.
        """
        query = self.order_by(db.query(self.model), order_by=order_by)
        return query.offset(skip).limit(limit).all()

    def get_all(
        self, db: Session, *, order_by: Optional[List[str]] = None
    ) -> List[ModelType]:
        """Get all records from the database.

        Parameters
        ----------
        db : Session
            The database session.
        order_by: Optional[List[str]]
            List of column names to order by. If a column name is prefixed with '-',
            order it in descending order.

        Returns
        -------
        List[ModelType]
            A list of SQLAlchemy model instances from the query.
        """
        query = self.order_by(db.query(self.model), order_by=order_by)
        return query.all()

    def search(
        self,
        db: Session,
        *,
        search_column: str,
        search_term: str,
        order_by: Optional[List[str]] = None,
        limit: int = 0,
    ) -> List[ModelType]:
        """search all the records from the database based on the search column,
        search term then order the results by particular column and then return
        the first limited value results.

        Parameters
        ----------
        db : Session
            The database session.
        search_column : str
            This string specifies which columns to search the search_term for.
        search_term : str
            The string to use to search for in the search_column either startswith
            or endswith or a fuzzy search.
        order_by : Optional[List[str]], optional
            List of column names to order by. If a column name is prefixed with '-',
            order it in descending order.
        limit : int, optional
            This value controls the number of results returned, by default 0.

        Returns
        -------
        List[ModelType]
            A list of SQLAlchemy model instances from the query.
        """
        if hasattr(self.model, search_column):
            # Keeping this as a comment so as to get back to the previous exact match
            # system for stable response purposes.

            # query = db.query(self.model).filter(
            #     getattr(self.model, search_column).contains(search_term)
            # )
            # SIMILARITY function will work only if the extension is enabled.
            # only works with string data
            similarity_func = func.similarity(
                getattr(self.model, search_column), search_term
            )
            query = (db.query(self.model).where(similarity_func > 0.1)).order_by(
                similarity_func.desc()
            )
        else:
            raise HTTPException(
                status_code=400, detail=f"{search_column} is not a valid column."
            )

        ordered_query = self.order_by(query, order_by=order_by)

        if limit > 0:
            return ordered_query.limit(limit).all()
        return ordered_query.all()

    def create(
        self, db: Session, *, obj_in: Union[CreateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Create a new record in the database.

        Parameters
        ----------
        db : Session
            The database session.
        obj_in : CreateSchemaType
            A Pydantic model that its attributes are used
            to create a new record in the attributes.

        Returns
        -------
        ModelType
            An instance of the SQLAlchemy model for the newly created records.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """Update an existing record in the database.

        Parameters
        ----------
        db : Session
            The database session.
        db_obj : ModelType
            The database object to update.
        obj_in : Union[UpdateSchemaType, Dict[str, Any]]
            Either a Pydantic model or a dictionary of
            new values for the database object to update from.

        Returns
        -------
        ModelType
            The updated database object.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        """Delete the database object for the given id.

        Parameters
        ----------
        db : Session
            The database session.
        id : Any
            The object id in the database to delete.

        Returns
        -------
        Optional[ModelType]
            The deleted object, if it existed in the database.
        """
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
            return obj
        return None
