"""
Cantina Nerd — cardápio de lanches de filmes e séries

API didática que demonstra Docker Compose com dois serviços:
esta API (FastAPI) e um banco PostgreSQL separado.

Estrutura do projeto (separação de responsabilidades):
- app/main.py      -> cria o app FastAPI e registra os routers
- app/models.py    -> modelos ORM (SQLAlchemy): as tabelas do banco
- app/schemas.py   -> schemas Pydantic: formato do JSON que entra e sai
- app/database.py  -> engine, sessões e a dependência get_db
- app/seed.py      -> cardápio inicial, inserido se a tabela estiver vazia
- app/routers/     -> rotas (endpoints), uma "fatia" por arquivo

Decisões didáticas:
- ORM com SQLAlchemy: compare models.py (tabela) com schemas.py (JSON).
- A sessão do banco é injetada nas rotas via Depends(get_db).
- A conexão vem da variável de ambiente DATABASE_URL (definida no compose.yaml).
- As tabelas são criadas e populadas na inicialização (lifespan).
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import Base, SessionLocal, engine
from app.routers import cardapio
from app.seed import popular_cardapio


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Roda quando a API sobe: cria as tabelas e popula o cardápio inicial
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        popular_cardapio(db)
    yield


app = FastAPI(
    title="Cantina Nerd",
    description="API do cardápio com os lanches mais famosos dos filmes e séries nerds.",
    lifespan=lifespan,
)

# Registra as rotas do cardápio (definidas em app/routers/cardapio.py)
app.include_router(cardapio.router)


@app.get("/health", tags=["util"])
def health():
    """Verifica se a API e o banco estão no ar."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="Banco de dados indisponível")
    return {"status": "ok", "mensagem": "Cantina aberta! Venham, nerds famintos! 🎲"}
