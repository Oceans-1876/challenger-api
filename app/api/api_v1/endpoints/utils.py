from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps
from app.utils.email import send_test_email

router = APIRouter()


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """test_email: Sending test emails.

    Parameters
    ----------
    email_to : EmailStr
        A pydantic Model to validate Email String.
    current_user : models.User, optional
        Instance of the current superuser,
        by default Depends(deps.get_current_active_superuser)

    Returns
    -------
    Any
        Message, indicating that the test email has been sent.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
