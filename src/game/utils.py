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

data_game_model = {
    'properties': [
        {
            'number': 'number',
            'name': 'name',
            'typre': 'type',
            'price': 'price',
            'owner_id': 'owner_id',
            'street_color': 'street_color',
            'hotel_level': 'hotel_level',

            'improvement_value': [],
            'rent_value': [],
            'mortgage': False,
        },
        {
            'number': 'number',
            'name': 'name',
            'typre': 'type',
            'price': 'price',
            'owner_id': 'owner_id',
            'street_color': 'street_color',
            'hotel_level': 'hotel_level',

            'improvement_value': [],
            'rent_value': [],
            'mortgage': False,
        }
    ],
    'gamer': [
        {
            'id': 'id',
            'name': 'name',
            'user_id': 'user_id',
            'game_session_id': 'game_session_id',
            'q': 'q',
            'position': 'position',
            'balance': 'balance',

            'owned_fields': [],
        }
    ]
}
