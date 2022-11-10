from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Float
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


class SaleAlert(Base):
    __tablename__ = "sales_alert"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    volumenOfSale = Column(Float)
    percent = Column(Float)
    price = Column(Float)
    instId = Column(String)
    date = Column(DateTime, default=datetime.utcnow())


def add_to_sales_alert_db(session, type, volumenOfSale, percent, price, instId):
    new_transaction = SaleAlert(
        type=type,
        volumenOfSale=volumenOfSale,
        percent=percent,
        price=price,
        instId=instId,
        date=datetime.utcnow(),
    )

    try:
        session.add(new_transaction)
        session.commit()
        session.refresh(new_transaction)
    finally:
        session.close()
