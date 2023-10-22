from pydantic import BaseModel
from typing import Optional

class SendMessage(BaseModel):
    receptor_id: int
    asunto: str
    mensaje: str

class ReplyMessage(BaseModel):
    id: int
    respuesta : str