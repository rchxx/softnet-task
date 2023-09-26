from fastapi.routing import APIRouter
from fastapi import Depends, Response, status

from ..repos import boards_repository
from ..dto import BoardUpdate
from ..db.database import get_session


boards_router = APIRouter(prefix="/boards", tags=["Boards"])


@boards_router.get("/{board_id}")
async def get(board_id: int, db_conn=Depends(get_session)):
    """Get board"""
    dest_note = await boards_repository.get(board_id=board_id, db_conn=db_conn)
    return dest_note


@boards_router.post("/create")
async def create(board_update: BoardUpdate, db_conn=Depends(get_session)):
    """Create board"""
    inserted_id = await boards_repository.create(
        board_update=board_update, db_conn=db_conn
    )
    return {"inserted_id": inserted_id}


@boards_router.patch("/{board_id}/update")
async def update(
    board_id: int, board_update: BoardUpdate, db_conn=Depends(get_session)
):
    """Update board"""
    if board_update.model_dump(exclude_unset=True) == {}:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content="Object can't be empty.",
        )
    updated_rows_count = await boards_repository.update(
        board_id=board_id, board_update=board_update, db_conn=db_conn
    )
    if updated_rows_count:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="There is no such board."
        )


@boards_router.delete("/{board_id}/delete")
async def delete(board_id: int, db_conn=Depends(get_session)):
    """Delete board"""
    deleted_rows_count = await boards_repository.delete(
        board_id=board_id, db_conn=db_conn
    )
    if deleted_rows_count:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="There is no such board."
        )


@boards_router.post("/{board_id}/attach_note")
async def attach_note(board_id: int, note_id: int, db_conn=Depends(get_session)):
    """Attach note"""
    result = await boards_repository.attach_note(
        board_id=board_id, note_id=note_id, db_conn=db_conn
    )
    if result is None:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="There is no such board."
        )
    else:
        return Response(status_code=status.HTTP_200_OK)


@boards_router.delete("/{board_id}/detach_note")
async def detach_note(board_id: int, note_id: int, db_conn=Depends(get_session)):
    """Detach note"""
    result = await boards_repository.detach_note(
        board_id=board_id, note_id=note_id, db_conn=db_conn
    )
    if result is None:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="There is no such board."
        )
    else:
        return Response(status_code=status.HTTP_200_OK)
