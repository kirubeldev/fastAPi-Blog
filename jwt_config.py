# jwt_config.py
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

# Settings for AuthJWT
class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"headers", "cookies"}  # Use headers and cookies
    authjwt_cookie_csrf_protect: bool = False
    authjwt_access_token_expires: int = 60 * 1500
    authjwt_refresh_token_expires: int = 60 * 60 * 24 * 30  # 30 days

@AuthJWT.load_config
def get_config():
    return Settings()

# Exception handler that works safely in Python 3.12
def register_jwt_exception_handler(app):
    @app.exception_handler(AuthJWTException)
    async def authjwt_exception_handler(request: Request, exc):
        # If exc has status_code and message, use them; otherwise fallback
        status_code = getattr(exc, "status_code", 401)
        message = getattr(exc, "message", "Access token required")
        return JSONResponse(
            status_code=status_code,
            content={"detail": message}
        )
