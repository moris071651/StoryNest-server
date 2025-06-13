from fastapi import FastAPI
from api import router

from exceptions import setup_error_handling

app = FastAPI()

setup_error_handling(app)

app.include_router(router)
