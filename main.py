from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import close_db_connections, open_db_connections

from router import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    open_db_connections()

    yield

    close_db_connections()


# ** FastAPI Routers and Setup

app = FastAPI(lifespan=lifespan)
app.include_router(router)
