import pytest
from fastapi.testclient import TestClient
from main import app
from database.connection import Base, engine, SessionLocal
from models.atleta_model import Atleta

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.query(Atleta).delete()
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

def test_criar_atleta(setup_database):
    response = client.post("/atletas/", json={
        "nome": "Ana",
        "cpf": "55566677788",
        "centro_treinamento": "Centro D",
        "categoria": "Adulto"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Ana"

def test_listar_atletas(setup_database):
    response = client.get("/atletas/")
    assert response.status_code == 200
    data = response.json()
    assert data["items"][0]["nome"] == "Ana"

def test_atualizar_atleta(setup_database):
    response = client.put("/atletas/1", json={"nome": "Ana Atualizada"})
    assert response.status_code == 200
    assert response.json()["nome"] == "Ana Atualizada"

def test_deletar_atleta(setup_database):
    response = client.delete("/atletas/1")
    assert response.status_code == 200
    assert response.json()["detail"] == "Atleta deletado com sucesso"

def test_listar_atletas_vazio(setup_database):
    response = client.get("/atletas/")
    assert response.status_code == 200
    assert response.json()["items"] == []
