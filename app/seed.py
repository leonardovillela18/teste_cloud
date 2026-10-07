"""
Dados iniciais (seed): cardápio populado quando a tabela está vazia.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Lanche

# (nome, descricao, preco_em_reais, obra de origem)
CARDAPIO_INICIAL = [
    ("Cerveja Amanteigada", "Espuma cremosa direto do Três Vassouras", 15.00, "Harry Potter"),
    ("Pão de Lembas", "Uma mordida enche o estômago de um hobbit... por 5 minutos", 12.50, "O Senhor dos Anéis"),
    ("Ramen do Ichiraku", "O favorito de um certo ninja de Konoha", 28.90, "Naruto"),
    ("Bolo de Pokébola", "Recheio surpresa — pode vir um Pikachu de creme", 9.99, "Pokémon"),
    ("Waffles da Eleven", "Servidos de cabeça para baixo (no Mundo Invertido)", 14.00, "Stranger Things"),
    ("Segundo Café da Manhã", "Clássico hobbit, servido pontualmente às 11h", 22.00, "O Hobbit"),
]


def popular_cardapio(db: Session) -> None:
    """Insere o cardápio inicial apenas se a tabela estiver vazia."""
    tabela_vazia = db.scalar(select(Lanche).limit(1)) is None
    if tabela_vazia:
        db.add_all(
            Lanche(nome=nome, descricao=descricao, preco=preco, obra_origem=obra)
            for nome, descricao, preco, obra in CARDAPIO_INICIAL
        )
        db.commit()
