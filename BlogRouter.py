from fastapi import APIRouter

Blog_router = APIRouter(
    prefix="/api/v1",
    tags=["Blog"]
)



@Blog_router.get("/blog")
def index():
    return "Hello, World!"