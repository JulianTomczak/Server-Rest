from pydantic import BaseModel
from typing import Optional

class ModeradorSchema(BaseModel):
    name: str
    last_name: str
    email: str
    username: str
    password: str