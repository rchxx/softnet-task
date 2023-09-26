from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func

from ..database import Base


class Boards(Base):
    """Boards DB table"""

    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text(), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
