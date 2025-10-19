from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.app import app_config
from src.infra.kafka.producers import (
    polling_loop_start,
    polling_loop_stop,
    producer_teardown,
)
from src.presentation.router import router as main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    polling_loop_start()
    
    yield

    polling_loop_stop()
    producer_teardown()


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)


@app.get("/")
def root():
    return f"Hello from {app_config.project_name}"

