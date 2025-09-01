from fastapi import FastAPI
from database.connection import Base, engine, SessionLocal
from routers import atleta
from fastapi_pagination import add_pagination
from models.atleta_model import Atleta

Base.metadata.create_all(bind=engine)

db = SessionLocal()
if not db.query(Atleta).first():
    atletas_exemplo = [
        Atleta(nome="João", cpf="12345678900", centro_treinamento="Centro A", categoria="Adulto"),
        Atleta(nome="Maria", cpf="98765432100", centro_treinamento="Centro B", categoria="Juvenil"),
        Atleta(nome="Carlos", cpf="11122233344", centro_treinamento="Centro C", categoria="Adulto")
    ]
    db.add_all(atletas_exemplo)
    db.commit()
db.close()

app = FastAPI(title="API de Atletas")
app.include_router(atleta.router)
add_pagination(app)
