from typing import Iterable, Optional
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker

from sqlalchemy.engine import Engine as Database
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
_db_conn: Optional[Database] = None


def get_db_conn() -> Database:
    assert _db_conn is not None, "The DB connection is None"
    if _db_conn is not None:
        return _db_conn

    return None


# This is the part that replaces sessionmaker
def get_db_sess(db_conn=Depends(get_db_conn)) -> Iterable[Session]:
    sess = Session(bind=db_conn)

    try:
        yield sess
    finally:
        sess.close()


# * https://github.com/tiangolo/fastapi/issues/726#issuecomment-557687526
def open_db_connections():
    global _db_conn
    if _db_conn is None:
        Base.metadata.create_all(bind=engine)
        _db_conn = create_engine(
            SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )


def close_db_connections():
    if _db_conn:
        _db_conn.dispose()
