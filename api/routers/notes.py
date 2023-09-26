from fastapi.routing import APIRouter
from fastapi import Depends, Response, status

from ..repos import notes_repository
from ..dto import NoteUpdate
from ..db.database import get_session


notes_router = APIRouter(prefix="/notes", tags=["Notes"])


@notes_router.get("/{note_id}")
async def get(note_id: int, db_conn=Depends(get_session)):
    """Get note"""
    dest_note = await notes_repository.get(note_id=note_id, db_conn=db_conn)
    return dest_note


@notes_router.post("/create")
async def create(note: NoteUpdate, db_conn=Depends(get_session)):
    """Create note"""
    inserted_id = await notes_repository.create(note=note, db_conn=db_conn)
    return {"inserted_id": inserted_id}


@notes_router.patch("/{note_id}/update")
async def update(note_id: int, note_update: NoteUpdate, db_conn=Depends(get_session)):
    """Update note"""
    if note_update.model_dump(exclude_unset=True) == {}:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content="Object can't be empty.",
        )
    updated_rows_count = await notes_repository.update(
        note_id=note_id, note_update=note_update, db_conn=db_conn
    )
    if updated_rows_count:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="There is no such note."
        )


@notes_router.delete("/{note_id}/delete")
async def delete(note_id: int, db_conn=Depends(get_session)):
    """Delete note"""
    deleted_rows_count = await notes_repository.delete(note_id=note_id, db_conn=db_conn)
    if deleted_rows_count:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="There is no such note."
        )
