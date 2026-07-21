from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.masters.api import tally as tally_api
from src.masters.ui import routes as ui_routes

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="ODOS Starter Pack 5.6 - Tally Integration")

templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(tally_api.router)
app.include_router(ui_routes.router)


@app.get("/")
async def root():
    return {"status": "ok", "message": "ODOS Starter Pack 5.6 - Tally Integration"}
