from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


conf = {
    "host": "localhost",
    "port": "5432",
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
    new_token = NewToken(instId=instId, market=market, date=datetime.utcnow())

    try:
        session.add(new_token)
        session.commit()
        session.refresh(new_token)
    finally:
        session.close()

"""
docker run --name postgresql -e POSTGRES_USER=myusername -e POSTGRES_PASSWORD=mypassword -p 5432:5432 -d postgres

"""