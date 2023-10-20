from pydantic import BaseModel
from typing import Optional

class RecipesSchema(BaseModel):
    id: str[Optional]
    title: str
    description: bool
    preparation_time_minutes: str
    id_user: str
    id_category: str
    average_ranking: str[Optional]
    popularity: str[Optional]
    created_at: str
    updated_at: str
