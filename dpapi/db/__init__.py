from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from dpapi import config

engine = create_engine(config['DATABASE_URI'])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

Base = declarative_base()


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
