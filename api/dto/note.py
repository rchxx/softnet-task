from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Note(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str = "text"
    views: int = 0
    board_id: int | None = None
    created_at: datetime = datetime.utcnow
    updated_at: datetime = datetime.utcnow


class NoteUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str | None = None
    views: int = 0
    board_id: int | None = None
