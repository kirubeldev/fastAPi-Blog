from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

async def check_jwt_middleware(request: Request, call_next):
    public_paths = {"/api/v1/login", "/api/v1/register", "/docs", "/openapi.json"}

    if request.url.path not in public_paths:
        try:
            authorize = AuthJWT(request)
            authorize.jwt_required()
        except Exception as e:
            return JSONResponse(
                status_code=getattr(e, "status_code", 401),
                content={"detail": getattr(e, "message", "Access token required")}
            )

    response = await call_next(request)
    return response
