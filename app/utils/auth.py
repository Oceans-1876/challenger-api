from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

from app.core.config import get_settings

settings = get_settings()


def generate_password_reset_token(email: str) -> str:
    """generate_password_reset_token Generates the access token to reset/recover the password.

    Parameters
    ----------
    email : str
        Email ID of the User.

    Returns
    -------
    str
        Encoded JWT Token.
    """
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """verify_password_reset_token Check whether the token is authentic or not.

    Parameters
    ----------
    token : str
        Password reset/recover token.

    Returns
    -------
    Optional[str]
        Email ID in the token or None.
    """
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None
