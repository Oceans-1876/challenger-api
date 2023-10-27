from typing import List

from app.models import Species


def binomial_only(species: List[Species]) -> List[Species]:
    """
    TODO: This is a temporary fix. In the future, we could consider filtering out genera
    when loading data into the database or as part of the OCR workflow.
    """
    # Unlike `current_name`, `current_canonical_full_name` doesn't include
    # author(s) and year of publication, so for a genus, there won't be any spaces.
    return [
        sp
        for sp in species
        if sp.current_canonical_simple_name and " " in sp.current_canonical_simple_name
    ]
