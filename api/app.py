from fastapi import FastAPI

from .db.database import initialize_database, dispose_database
from .routers.notes import notes_router
from .routers.boards import boards_router


app = FastAPI()
app.include_router(router=notes_router)
app.include_router(router=boards_router)


@app.on_event("startup")
async def startup():
    """Startup event for application"""
    await initialize_database()


@app.on_event("shutdown")
async def shutdown():
    """Startup event for application"""
    await dispose_database()
