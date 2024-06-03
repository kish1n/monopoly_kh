from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
from fastapi_users import FastAPIUsers
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from src.auth.base_config import auth_backend
from src.auth.models import User

from src.game.router import router as game_session_router
from src.actions.router import router as actions_router
from src.core import Core
from src.game.websocket import router as websocket_router

app = FastAPI(
    title="Kharkiv monopoly",
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(game_session_router)
app.include_router(actions_router)
app.include_router(websocket_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    response: Response = await call_next(request)
    if request.url.path.startswith("/static"):
        response.headers["Cache-Control"] = "no-store"
    return response

@app.get("/", response_class=HTMLResponse)
async def get():
    with open("../static/html/monopoly.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.head("/retabels",
          summary="Recreate tables",
          description="This endpoint recreates all tables in the database.",
          tags=["game"])
async def retabels():
    await Core.create_tables()
    return {"status": "ok"}