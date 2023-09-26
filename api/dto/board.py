from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Board(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = "text"
    created_at: datetime = datetime.utcnow
    updated_at: datetime = datetime.utcnow


class BoardUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = "text"
