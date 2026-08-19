from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

URL_DB = "sqlite:///./apteka.db"

engine = create_engine(URL_DB)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()