"""
Camada de acesso ao banco de dados (SQLAlchemy).

Centraliza tudo que envolve PostgreSQL:
- a URL de conexão (vinda do compose.yaml via variável de ambiente);
- o engine e a fábrica de sessões;
- a dependência get_db, injetada pelo FastAPI em cada requisição.
"""

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Dentro da rede do Compose, o banco é acessado pelo NOME do serviço: "db"
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://cantina:segredo123@db:5432/cantina"
)

engine = create_engine(DATABASE_URL)

# autocommit/autoflush desligados: quem controla a transação é a rota
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    """Classe base de todos os modelos ORM (as tabelas herdam dela)."""


def get_db() -> Generator[Session, None, None]:
    """Dependência do FastAPI: abre uma sessão por requisição e sempre fecha."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
