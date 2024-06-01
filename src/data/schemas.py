from pydantic import BaseModel
from typing import List, Optional

class PropertyModel(BaseModel):
    number: int
    name: str
    type: str
    price: int
    owner_id: int
    street_color: str
    hotel_level: int
    improvement_value: List
    rent_value: List
    mortgage: int

class GamerModel(BaseModel):
    id: int
    name: str
    user_id: int
    game_session_id: int
    q: int
    position: int
    balance: int
    owned_fields: List