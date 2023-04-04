from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.config import db


origins = ["http://localhost:3000"]


def init_app():
    db.init()

    app = FastAPI(
        title="CRUD app",
        description="CRUD sort pagination page",
        version="1"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    return app


app = init_app()


def start():
    """ Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)
