from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator


class Operator(str, Enum):
    eq = "eq"  # ==
    ne = "ne"  # !=
    gt = "gt"  # >
    gte = "ge"  # >=
    lt = "lt"  # <
    lte = "le"  # <=
    contains = "contains"  # if iterable contains the given value (not tested)
    # TODO add more operators


class Join(str, Enum):
    AND = "AND"
    OR = "OR"


class Expression(BaseModel):
    column_name: str
    search_term: str
    operator: Operator
    fuzzy: bool = False
    min_string_similarity: Optional[float] = Field(default=0.1)

    def uses_column(self, name: str) -> bool:
        return self.column_name == name


class ExpressionGroup(BaseModel):
    join: Optional[Join]
    expressions: List[Union[Expression, "ExpressionGroup"]] = Field(min_items=1)

    @validator("expressions")
    def expressions_validator(
        cls,
        v: List[Union[Expression, "ExpressionGroup"]],
        values: Dict[str, Any],
    ) -> List[Union[Expression, "ExpressionGroup"]]:
        join = values.get("join")
        expressions_length = len(v)
        if not join and expressions_length > 1:
            raise ValueError("a join operator is needed for multiple expression")
        if join and expressions_length == 1:
            raise ValueError("a join operator is not needed for one expression")
        return v

    def uses_column(self, name: str) -> bool:
        for expression in self.expressions:
            if expression.uses_column(name):
                return True
        return False


ExpressionGroup.update_forward_refs()
