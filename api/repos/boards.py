from ..dto import Board, BoardUpdate
from ..db.models import Boards, Notes
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update
from .notes import NotesRepository


notes_repository = NotesRepository()


class BoardsRepository:
    async def create(self, board_update: BoardUpdate, db_conn: AsyncSession):
        stmt = insert(Boards).values(**board_update.model_dump())
        result = await db_conn.execute(stmt)
        await db_conn.commit()
        return result.inserted_primary_key[0]

    async def get(self, board_id: int, db_conn: AsyncSession):
        stmt = select(Boards).filter(Boards.id == board_id)
        result = await db_conn.execute(stmt)
        result_scalar = result.scalar_one()
        if result_scalar is None:
            return None
        board = Board.model_validate(result_scalar)
        return board

    async def delete(self, board_id: int, db_conn: AsyncSession):
        stmt = delete(Boards).filter(Boards.id == board_id)
        result = await db_conn.execute(stmt)
        await db_conn.commit()
        return result.rowcount

    async def update(
        self, board_id: int, board_update: BoardUpdate, db_conn: AsyncSession
    ):
        stmt = (
            update(Boards)
            .where(Boards.id == board_id)
            .values(**board_update.model_dump(exclude_unset=True))
        )
        result = await db_conn.execute(stmt)
        await db_conn.commit()
        return result.rowcount

    async def attach_note(self, board_id: int, note_id: int, db_conn: AsyncSession):
        note = await notes_repository.get(note_id=note_id, db_conn=db_conn)
        if note is None:
            return None
        stmt = update(Notes).where(Notes.id == note_id).values({"board_id": board_id})
        result = await db_conn.execute(stmt)
        await db_conn.commit()
        return result.rowcount

    async def detach_note(self, board_id: int, note_id: int, db_conn: AsyncSession):
        note = await notes_repository.get(note_id=note_id, db_conn=db_conn)
        if note is None:
            return None
        stmt = update(Notes).where(Notes.id == note_id).values({"board_id": None})
        result = await db_conn.execute(stmt)
        await db_conn.commit()
        return result.rowcount
