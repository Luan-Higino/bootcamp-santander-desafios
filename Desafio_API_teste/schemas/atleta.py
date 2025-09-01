from pydantic import BaseModel

class AtletaBase(BaseModel):
    nome: str
    cpf: str
    centro_treinamento: str
    categoria: str

class AtletaCreate(AtletaBase):
    pass

class AtletaUpdate(BaseModel):
    nome: str | None = None
    centro_treinamento: str | None = None
    categoria: str | None = None

class AtletaResponse(AtletaBase):
    id: int

    model_config = {
        "from_attributes": True
    }
