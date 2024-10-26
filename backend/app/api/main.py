from fastapi import APIRouter

from app.api.routes import ip_addresses, items, login, page_views, users, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(ip_addresses.router, prefix="/ipaddress", tags=["ipaddress"])
api_router.include_router(page_views.router, prefix="/pageviews", tags=["pageviews"])
