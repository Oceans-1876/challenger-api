from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypedDict,
    TypeVar,
    Union,
    cast,
)

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import Column, Table, and_, asc, desc, func, or_
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.functions import _FunctionGenerator

from app.core.config import get_settings
from app.db.base_class import Base
from app.schemas import Expression, ExpressionGroup, Join

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
PaginationSchemaType = TypeVar("PaginationSchemaType", bound=BaseModel)

settings = get_settings()

page_URI = f"{settings.SERVER_HOST}{settings.API_V1_STR}" + "/{}/?skip={}&limit={}"

API_Model_mapping = {
    "DataSource": "data_source",
    "Species": "species",
    "Station": "stations",
    "User": "users",
}


class SearchExpressions(TypedDict):
    clauses: List[BinaryExpression]
    fuzzy_funcs: List[_FunctionGenerator]


class CRUDBase(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, PaginationSchemaType]
):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD)."""

    def __init__(self, model: Type[ModelType]):
        """

        Parameters
        ----------
        model : BaseModel
                A SQLAlchemy model class
        """
        self.model = model

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

    def create_search_expressions(
        self,
        expressions: Union[Expression, ExpressionGroup],
        *,
        relations: Optional[List[Union[Type[Base], Table]]] = None,
    ) -> SearchExpressions:
        """Create SQLAlchemy search expressions from the given Expression or
        ExpressionGroup.
        Return a Dict with two keys: `clauses` and `fuzzy_funcs`. The former
        can be passed to a query.filter() call, while the latter can be used to order
        the query by the fuzzy_funcs.

        Parameters
        ----------
        expressions : Union[Expression, ExpressionGroup]
            The search expressions. See the `search` method for an example.
        relations : Optional[List[Union[Type[Base], Table]]]
            The relations to use for discovering columns.

        Returns
        -------
        SearchExpressions
        """
        search_expressions = SearchExpressions(clauses=[], fuzzy_funcs=[])

        if isinstance(expressions, ExpressionGroup):
            if expressions.join == Join.AND:
                join_func = and_
            elif expressions.join == Join.OR:
                join_func = or_
            else:
                raise ValueError(f"Invalid join type: {expressions.join}")

            sub_clauses: List[BinaryExpression] = []
            for expression in expressions.expressions:
                sub_search_expressions = self.create_search_expressions(
                    expression, relations=relations
                )
                sub_clauses.append(
                    cast(BinaryExpression, and_(*sub_search_expressions["clauses"]))
                )
                search_expressions["fuzzy_funcs"].extend(
                    sub_search_expressions["fuzzy_funcs"]
                )
            search_expressions["clauses"].append(
                cast(BinaryExpression, join_func(*sub_clauses))
            )
        else:
            expression = expressions
            column: Optional[Column] = getattr(self.model, expression.column_name, None)
            if not column:
                has_column = False
                if relations:
                    for relation in relations:
                        if isinstance(relation, Table):
                            column = relation.c[expression.column_name]
                            has_column = True
                        else:
                            column = getattr(relation, expression.column_name, None)
                            if column is not None:
                                has_column = True
                        if has_column:
                            break
                if not has_column:
                    raise ValueError(f"Invalid column name: {expression.column_name}")

            if not hasattr(column, "type"):
                raise ValueError(f"Invalid column name: {expression.column_name}")

            if column.type.python_type == str and expression.fuzzy:  # type: ignore

                similarity_func = func.word_similarity(expression.search_term, column)

                search_expressions["clauses"].append(
                    cast(
                        BinaryExpression,
                        similarity_func >= expression.min_string_similarity,
                    ),
                )
                search_expressions["fuzzy_funcs"].append(
                    cast(_FunctionGenerator, similarity_func)
                )
            else:
                operator_func = getattr(column, f"__{expression.operator}__", None)
                if not operator_func:
                    raise ValueError(f"Invalid operator: {expression.operator}")

                search_expressions["clauses"].append(
                    operator_func(expression.search_term)
                )

        return search_expressions

    def search(
        self,
        db: Session,
        expressions: Union[Expression, ExpressionGroup],
        *,
        relations: Optional[List[Union[Type[Base], Table]]] = None,
        order_by: Optional[List[str]] = None,
        limit: int = 0,
    ) -> List[ModelType]:
        """Search all the records from the database using the given search expressions,
        then order the results by the columns in `order_by` and return
        the first limited results.

        Here is an example of expressions for the Station model:
        {
          "join": "AND",
          "expressions": [
            {
              "column_name": "fao_area",
              "search_term": "27",
              "operator": "eq"
            },
            {
              "join": "OR",
              "expressions": [
                {
                  "column_name": "species_id",
                  "search_term": "b92a3b6f-8816-5c29-ba10-83bc78eab8ae",
                  "operator": "eq"
                },
                {
                  "column_name": "species_id",
                  "search_term": "a57a7c8b-1b3b-57f9-8101-f456834d18ea",
                  "operator": "eq"
                }
              ]
            }
          ]
        }
        This example searches for all stations that are in the FAO area 27 and
        have at least one of the species given by their IDs.
        This requires `app.models.stations.stations_species_table` to be passed as
        a relation to provide `species_id`, otherwise it will raise an error.

        Parameters
        ----------
        db : Session
            The database session.
        expressions : Union[Expression, ExpressionGroup]
            The search expressions.
        relations : Optional[List[Union[Type[Base], Table]]]
            The relations to be joined in the search.
        order_by : Optional[List[str]]
            List of column names to order by. If a column name is prefixed with '-',
            order it in descending order.
        limit : int, optional
            This value controls the number of results returned, by default 0.

        Returns
        -------
        List[ModelType]
            A list of SQLAlchemy model instances from the query.
        """
        try:
            search_expressions = self.create_search_expressions(
                expressions, relations=relations
            )
        except ValueError as e:
            raise HTTPException(
                status_code=400, detail=f"Error with search expressions: {e}"
            )

        query = db.query(self.model)

        if relations:
            for relation in relations:
                query = query.join(relation, isouter=True)

        query = query.filter(*search_expressions["clauses"]).order_by(
            *map(lambda f: f.desc(), search_expressions["fuzzy_funcs"])
            # *map(lambda f: f.asc(), search_expressions["fuzzy_funcs"])
        )

        ordered_query = self.order_by(query, order_by=order_by)

        if limit > 0:
            return ordered_query.limit(limit).all()
        return ordered_query.all()

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

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[List[str]] = None,
    ) -> PaginationSchemaType:
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
        data_from_db = query.offset(skip).limit(limit).all()
        count = query.count()
        data = {
            "count": count,
            "first_page": page_URI.format(
                API_Model_mapping[self.model.__name__], 0, limit
            ),
            "last_page": page_URI.format(
                API_Model_mapping[self.model.__name__], max(0, count - limit), limit
            ),
            "previous_page": (
                None
                if (skip - limit) < 0
                else page_URI.format(
                    API_Model_mapping[self.model.__name__], (skip - limit), limit
                )
            ),
            "next_page": (
                None
                if skip >= (count - limit)
                else page_URI.format(
                    API_Model_mapping[self.model.__name__], (skip + limit), limit
                )
            ),
            "results": data_from_db,
        }
        return cast(PaginationSchemaType, data)

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
