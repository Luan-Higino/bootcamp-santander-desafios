from fastapi import FastAPI
from database.connection import Base, engine
from routers import atleta
from fastapi_pagination import add_pagination

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Rotas
app.include_router(atleta.router)

# Paginação
add_pagination(app)
