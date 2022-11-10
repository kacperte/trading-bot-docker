from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

conf = {
    "host": "db",
    "port": "5432",
    "database": "postgres",
    "user": "postgres",
    "password": "postgres",
}
engine = create_engine(
    "postgresql://{user}:{password}@{host}:{port}/{database}".format(**conf)
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


class Transactions(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    side = Column(String)
    ordId = Column(
        String
    )
    instId = Column(String)
    date = Column(DateTime, default=datetime.utcnow())


def add_to_transaction_db(session, instId, side, ordId):
    new_transaction = Transactions(
        side=side,
        ordId=ordId,
        instId=instId,
    )

    try:
        session.add(new_transaction)
        session.commit()
        session.refresh(new_transaction)
    finally:
        session.close()
