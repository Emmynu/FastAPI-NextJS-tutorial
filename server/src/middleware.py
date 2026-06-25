from fastapi import FastAPI
from fastapi.requests import Request
import logging
import time


logger = logging.getLogger("uvicorn.access")
logger.disabled =  True


def add_middleware(app: FastAPI):

    @app.middleware("http")
    async def middleware_logging(req: Request, call_next):

        start_time = time.time()

        response = await call_next(req)

        processing_time =  start_time - time.time()

        message = f" {req.method} - {response.status_code}- {req.url.path} - completed after {processing_time}"

        print(message)
        return response