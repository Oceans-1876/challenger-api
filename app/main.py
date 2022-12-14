from typing import Awaitable, Callable

import pydantic
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import Response

from app import PROJECT_ROOT
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.utils.logger import logger

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=None,
)


app.mount(
    "/fonts",
    StaticFiles(directory=PROJECT_ROOT / "fonts"),
    name="fonts",
)

allowed_origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )


async def catch_exceptions_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    Using this middleware we can return exceptions to the client as needed, while letting CORS middleware being applied.
    Otherwise, errors won't be returned for requests from clients with different origins.
    """
    origin = request.headers.get("Origin")
    error_headers = (
        {"Access-Control-Allow-Origin": origin}
        if origin and origin in allowed_origins
        else {}
    )

    try:
        return await call_next(request)
    except pydantic.ValidationError as exc:
        logger.exception(exc)
        return Response(exc.json(), status_code=500, headers=error_headers)
    except Exception as exc:
        logger.exception(exc)
        return Response("Internal server error", status_code=500, headers=error_headers)


app.middleware("http")(catch_exceptions_middleware)

app.include_router(api_router, prefix=settings.API_V1_STR)
