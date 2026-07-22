#tests\conftest.py:

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db

# Тестовая БД в памяти (SQLite in-memory)
# StaticPool нужен, чтобы все соединения использовали одну и ту же БД
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestSessionLocal = sessionmaker(bind=test_engine)


@pytest.fixture(autouse=True)
def setup_database():
    # create_all принимает ENGINE (подключение), а не Session
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db_session():
    # TestSessionLocal() создаёт ЭКЗЕМПЛЯР сессии (вызов фабрики)
    session = TestSessionLocal()
    yield session
    session.close()


@pytest.fixture()
def client(db_session):  # ← db_session как ПАРАМЕТР (pytest подставит автоматически)
    def override_get_db():
        yield db_session  # ← Просто yield сессию, НЕ вызов client()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()