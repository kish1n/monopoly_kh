from typing import List, Optional
import os
from functools import partial
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import get_session

from src.core import Core
from src.game_session.database import GameSession, GameUser
from src.auth.base_config import current_user


router = APIRouter(
    tags=["game_session"],
    prefix="/game_session"
)

@router.post("/create")
async def create_game_session():
    id = await Core.create_game_session()
    return {"message": f"game session created {id}"}

@router.post("/join/{session_id}")
async def join_game_session(session_id: int, name: str):
    try:
        new_user = await Core.join_game_session(session_id, name)
        return new_user
    except HTTPException as e:
        raise e