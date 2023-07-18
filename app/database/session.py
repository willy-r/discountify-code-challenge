from typing import Generator

from sqlalchemy.orm import Session

from app.database.base import SessionLocal


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
