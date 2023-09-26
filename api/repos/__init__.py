from .notes import NotesRepository
from .boards import BoardsRepository


notes_repository = NotesRepository()
boards_repository = BoardsRepository()

__all__ = ["notes_repository", "boards_repository"]
