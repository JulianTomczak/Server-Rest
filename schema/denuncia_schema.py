from pydantic import BaseModel
from typing import Optional

class DenunciaSchema(BaseModel):
    motivo: str
    id_recipe: str
    resuelta: bool