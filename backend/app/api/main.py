from fastapi import APIRouter

from app.api.routes import ip_addresses, items, login, payments, page_views, mongo, users, utils, otp

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(ip_addresses.router, prefix="/ipaddress", tags=["ipaddress"])
api_router.include_router(page_views.router, prefix="/pageviews", tags=["pageviews"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(mongo.router, prefix="/mongo", tags=["mongo"])
api_router.include_router(otp.router, prefix="/otp", tags=["otp"])
