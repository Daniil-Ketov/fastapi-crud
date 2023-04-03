from fastapi import FastAPI
import uvicorn
from app.config import db


def init_app():
    db.init()

    app = FastAPI(
        title="CRUD app",
        description="CRUD sort pagination page",
        version="1"
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
