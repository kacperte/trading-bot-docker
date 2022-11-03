from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import NewToken

conf = {
    "host": "0.0.0.0",
    "port": "5431",
    "database": "postgres",
    "user": "myusername",
    "password": "mypassword",
}
engine = create_engine(
    "postgresql://{user}:{password}@{host}:{port}/{database}".format(**conf)
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def add_to_new_token_db(session, instId, market):
    new_token = NewToken(instId=instId, market=market)

    try:
        session.add(new_token)
        session.commit()
        session.refresh(new_token)
    finally:
        session.close()
