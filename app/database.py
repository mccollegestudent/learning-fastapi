from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from.config import settings

#format of connection string that we have to pass to sqlalchemy
#SQLALCHEMY_DATABASE_URL = 'postgressql://<username>:<password>@<ip-address/hostname:database_port>/<databse_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #talking with database

Base = declarative_base() #base class - all models defined to create tables in postgres will extend this class

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()