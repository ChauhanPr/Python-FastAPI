
import pytest
from models import Todos, Users
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from database import Base
from main import app
from routers.auth import bcrypt_context

SQLALCHEMEY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMEY_DATABASE_URL,
    connect_args={"check_same_thread":False},
    poolclass = StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'preetichauhan','id':1,'user_role':'admin'}


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn a code.",
        description="Need to learn everyday.",
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todo;"))
        connection.commit()


@pytest.fixture
def user_test():
    users = Users(
        username="preetichauhan",
        email="preet@gmail.com",
        first_name="Preeti",
        last_name="Chauhan",
        hashed_password=bcrypt_context.hash("preet123"),
        role="admin"
    )

    db = TestingSessionLocal()
    db.add(users)
    db.commit()
    yield users
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM user;"))
        connection.commit()
