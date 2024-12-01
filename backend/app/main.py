import asyncio
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRoute
from sqlmodel import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

# from starlette.staticfiles import StaticFiles
from app.api.main import api_router
from app.core.config import settings
from app.core.db import close_mongo_connection, init_db, init_mongo
from app.core.exceptions import HTTPExceptionJSON
from app.profiles.exceptions import UnexpectedRelationshipState


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add exception hnadlers
@app.exception_handler(HTTPExceptionJSON)
async def http_exception_handler(
        request: Request,
        exc: HTTPExceptionJSON):
    json_data = jsonable_encoder(exc.data)
    return JSONResponse(
        status_code=exc.status_code,
        headers=exc.headers,
        content={"message": exc.detail, "code": exc.code, "error": json_data})

@app.exception_handler(UnexpectedRelationshipState)
async def unicorn_exception_handler(
        request: Request,
        exc: HTTPExceptionJSON):
    return JSONResponse(
        status_code=400,
        content={"message": "UnexpectedRelationshipState"})

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.run(init_mongo())
    # Initialize MongoDB on startup
    await init_mongo()
    # Create superuser for SQLAlchemy-based DB if needed
    with Session(init_db) as session:
        init_db(session)
    yield
    # Close MongoDB connection on shutdown
    await close_mongo_connection()

@app.on_event("startup")
async def startup():
    await init_mongo()
    pass

@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()
    pass

app.include_router(api_router, prefix=settings.API_V1_STR)
app.router.lifespan = lifespan
