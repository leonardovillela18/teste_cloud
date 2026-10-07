"""
Modelos ORM (SQLAlchemy): representam as tabelas do banco.

Compare com app/schemas.py:
- ORM (este arquivo): como o dado é GUARDADO no Postgres.
- Schemas Pydantic: como o dado ENTRA e SAI da API (JSON).
"""

from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Lanche(Base):
    __tablename__ = "lanches"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    preco: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    obra_origem: Mapped[str] = mapped_column(String(100), nullable=False)
