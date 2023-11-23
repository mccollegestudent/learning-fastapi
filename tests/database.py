from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db

from app.database import Base

from app.oauth2 import create_access_token

import pytest
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #talking with database

# @pytest.fixture(scope="function")
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine) #create tables brefore code runs
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture(scope="function")
# def client(session):
#     def override_get_db():
#         db = TestingSessionLocal()
#         try:
#             yield session
#         finally:
#             session.close()
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)

