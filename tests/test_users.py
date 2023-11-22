from fastapi.testclient import TestClient
from app.main import app
from app import schemas

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import sessionmaker
from app.config import settings



SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #talking with database

Base = declarative_base() #base class - all models defined to create tables in postgres will extend this class

# Dependency
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)  #from documentation now we can run test

def test_root():
    res = client.get("/") #we dont need the root we just use the app instance since its not a server etc
    print(res.json().get('message'))
    assert res.json().get('message') == 'Welcome to my api testing in progress'

def test_create_user():
    res = client.post("/users/", json={"email":"hello@gmail.com", "password":"1234"})
    new_user = schemas.UserOut(**res.json()) # **sd have to unpack
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201