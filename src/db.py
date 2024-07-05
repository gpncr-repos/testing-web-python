from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import settings

engine = create_engine(str(settings.db_url))

SessionLocal = scoped_session(sessionmaker(engine))


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
