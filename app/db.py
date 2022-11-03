from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

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

class NewToken(Base):
    __tablename__ = "new_token"
    id = Column(Integer, primary_key=True, index=True)
    instId = Column(String, index=True)
    market = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow())


def add_to_new_token_db(session, instId, market):
    new_token = NewToken(instId=instId, market=market)

    try:
        session.add(new_token)
        session.commit()
        session.refresh(new_token)
    finally:
        session.close()
