from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, paginate
from models.atleta import Atleta
from schemas.atleta import AtletaBase, AtletaResponse
from database.connection import get_db

router = APIRouter(prefix="/atletas", tags=["Atletas"])

@router.post("/", response_model=AtletaResponse)
def criar_atleta(atleta: AtletaBase, db: Session = Depends(get_db)):
    novo_atleta = Atleta(**atleta.dict())
    db.add(novo_atleta)
    try:
        db.commit()
        db.refresh(novo_atleta)
        return novo_atleta
    except IntegrityError as e:
        db.rollback()
        if "cpf" in str(e.orig).lower():
            raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")
        raise HTTPException(status_code=400, detail="Erro de integridade nos dados")

@router.get("/", response_model=Page[AtletaResponse])
def listar_atletas(nome: str | None = None, cpf: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Atleta)
    if nome:
        query = query.filter(Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(Atleta.cpf == cpf)
    return paginate(query.all())
