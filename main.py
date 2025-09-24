from fastapi import FastAPI
from AuthRouter import Auth_router
from BlogRouter import Blog_router
from database import Base , engine


app= FastAPI(
    title="Blog backend for testing Fast api",
    description="This is a simple blog backend for testing FastAPI",
    version="1.0.0",
) 

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(engine)

app.include_router(Auth_router)
app.include_router(Blog_router)
