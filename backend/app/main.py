from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/")
def home():
    return "Welcome home!"


def start():
    """ Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)
