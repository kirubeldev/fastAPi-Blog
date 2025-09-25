from fastapi import FastAPI
from database import Base, engine
from AuthRouter import Auth_router
from BlogRouter import Blog_router
from middleware import check_jwt_middleware
from jwt_config import register_jwt_exception_handler
from swagger_api import custom_openapi

app = FastAPI(
    title="Blog backend for testing FastAPI",
    description="This is a simple blog backend for testing FastAPI",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(engine)

# Middleware
app.middleware("http")(check_jwt_middleware)

# Exception handler
register_jwt_exception_handler(app)

# Custom OpenAPI
app.openapi = lambda: custom_openapi(app)

# Routers
app.include_router(Auth_router)
app.include_router(Blog_router)
