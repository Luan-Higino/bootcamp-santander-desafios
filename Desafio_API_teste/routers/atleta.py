from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.atleta_model import Atleta
from schemas.atleta import AtletaCreate, AtletaUpdate, AtletaResponse
from fastapi_pagination import Page, add_pagination, paginate

router = APIRouter(prefix="/atletas", tags=["Atletas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AtletaResponse)
def criar_atleta(atleta: AtletaCreate, db: Session = Depends(get_db)):
    existing = db.query(Atleta).filter(Atleta.cpf == atleta.cpf).first()
    if existing:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    novo = Atleta(**atleta.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/", response_model=Page[AtletaResponse])
def listar_atletas(db: Session = Depends(get_db)):
    atletas = db.query(Atleta).all()
    return paginate(atletas)

@router.put("/{atleta_id}", response_model=AtletaResponse)
def atualizar_atleta(atleta_id: int, atleta: AtletaUpdate, db: Session = Depends(get_db)):
    db_atleta = db.query(Atleta).filter(Atleta.id == atleta_id).first()
    if not db_atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    for key, value in atleta.dict(exclude_unset=True).items():
        setattr(db_atleta, key, value)
    db.commit()
    db.refresh(db_atleta)
    return db_atleta

@router.delete("/{atleta_id}", response_model=dict)
def deletar_atleta(atleta_id: int, db: Session = Depends(get_db)):
    db_atleta = db.query(Atleta).filter(Atleta.id == atleta_id).first()
    if not db_atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    db.delete(db_atleta)
    db.commit()
    return {"detail": "Atleta deletado com sucesso"}

add_pagination(router)
