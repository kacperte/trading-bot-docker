from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db import Base


class NewToken(Base):
    __tablename__ = "new_token"
    id = Column(Integer, primary_key=True, index=True)
    instId = Column(String, index=True)
    market = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow())
