from fastapi import APIRouter

from app.api.routes import ( 
    items,
    login,
    currencies,
    customizationInfo,
    ipAddresses,
    pageviews,
    payments,
    professionals,
    mongo,
    users,
    utils,
    theme,
    services,
    settings,
    otp,
    auditInfos,
    userRoles,
    roles,
    profiles,
)

api_router = APIRouter()
api_router.include_router(auditInfos.router, prefix="/auditInfos", tags=["AuditInfos"])
api_router.include_router(currencies.router, prefix="/currencies", tags=["Currencies"])
api_router.include_router(customizationInfo.router, prefix="/customizationInfo", tags=["CustomizationInfo"])
api_router.include_router(ipAddresses.router, prefix="/ipAddress", tags=["ipAddress"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(mongo.router, prefix="/mongo", tags=["Mongo"])
api_router.include_router(otp.router, prefix="/otp", tags=["OTP"])
api_router.include_router(pageviews.router, prefix="/pageviews", tags=["PageViews"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(professionals.router, prefix="/professionals", tags=["Professionals"])
api_router.include_router(profiles.router, prefix="/settings/profiles", tags=["Profiles"])
api_router.include_router(roles.router, prefix="/settings/roles", tags=["Roles"])
api_router.include_router(services.router, prefix="/services", tags=["Services"])
api_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
api_router.include_router(theme.router, prefix="/theme", tags=["Theme"])
api_router.include_router(userRoles.router, prefix="/userRoles", tags=["UserRoles"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(utils.router, prefix="/utils", tags=["Utils"])
