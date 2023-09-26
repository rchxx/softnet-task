from ..dto import Note, NoteUpdate
from ..db.models import Notes
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update


class NotesRepository:
    async def _views_counter(self, note_id: int, db_conn: AsyncSession):
        stmt = (
            update(Notes)
            .filter(Notes.id == note_id)
            .values({Notes.views: Notes.views + 1})
        )
        await db_conn.execute(stmt)
        await db_conn.commit()

    async def create(self, note: NoteUpdate, db_conn: AsyncSession):
        stmt = insert(Notes).values(**note.model_dump())
        result = await db_conn.execute(stmt)
        await db_conn.commit()
        return result.inserted_primary_key[0]

    async def get(self, note_id: int, db_conn: AsyncSession):
        stmt = select(Notes).filter(Notes.id == note_id)
        result = await db_conn.execute(stmt)
        result_scalar = result.scalar()
        if result_scalar is None:
            return None
        note = Note.model_validate(result_scalar)
        await self._views_counter(note_id=note_id, db_conn=db_conn)
        return note

    async def delete(self, note_id: int, db_conn: AsyncSession):
        stmt = delete(Notes).filter(Notes.id == note_id)
        result = await db_conn.execute(stmt)
        await db_conn.commit()
        return result.rowcount

    async def update(
        self, note_id: int, note_update: NoteUpdate, db_conn: AsyncSession
    ):
        stmt = (
            update(Notes)
            .where(Notes.id == note_id)
            .values(**note_update.model_dump(exclude_unset=True))
        )
        result = await db_conn.execute(stmt)
        await db_conn.commit()
        return result.rowcount
