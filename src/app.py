from fastapi import FastAPI

from api.router import router
from di import Container

app = FastAPI()
app.include_router(router)
app.container = Container()
