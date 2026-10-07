"""
Schemas Pydantic: definem o formato dos dados que entram e saem da API.

Separação dos schemas:
- LancheCreate: o que o cliente envia para cadastrar (sem id).
- Lanche: o que a API devolve (com id vindo do banco).

Compare com app/models.py:
- Schemas (este arquivo): validação do JSON na fronteira da API.
- ORM: representação da tabela no banco.
"""

from pydantic import BaseModel, ConfigDict


class LancheCreate(BaseModel):
    """Dados enviados pelo cliente ao cadastrar um lanche."""

    nome: str
    descricao: str
    preco: float
    obra_origem: str


class Lanche(LancheCreate):
    """Lanche completo, como é devolvido pela API (inclui o id do banco)."""

    # Permite criar o schema a partir de um objeto ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)

    id: int
