from fastapi import FastAPI

from src.config.app import app_config
from src.presentation.router import router as main_router

app = FastAPI()
app.include_router(main_router)


@app.get("/")
def orders_root():
    return f"Hello from {app_config.project_name}"

