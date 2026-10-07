"""
Rotas do cardápio: toda a lógica HTTP dos lanches fica aqui.

O router funciona como um "mini-app": definimos as rotas nele
e depois registramos no app principal (app/main.py).

A sessão do banco chega por injeção de dependência (Depends(get_db)):
o FastAPI abre uma sessão por requisição e fecha ao final.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

# prefix="/cardapio" -> todas as rotas começam com /cardapio
# tags -> agrupa as rotas na documentação automática (/docs)
router = APIRouter(prefix="/cardapio", tags=["cardapio"])


@router.get("", response_model=list[schemas.Lanche])
def listar_cardapio(db: Session = Depends(get_db)):
    """Lista todos os lanches disponíveis."""
    return db.scalars(select(models.Lanche).order_by(models.Lanche.id)).all()


@router.get("/{lanche_id}", response_model=schemas.Lanche)
def detalhar_lanche(lanche_id: int, db: Session = Depends(get_db)):
    """Mostra os detalhes de um lanche."""
    lanche = db.get(models.Lanche, lanche_id)
    if lanche is None:
        raise HTTPException(status_code=404, detail="Lanche não encontrado neste multiverso")
    return lanche


@router.post("", status_code=201, response_model=schemas.Lanche)
def criar_lanche(lanche: schemas.LancheCreate, db: Session = Depends(get_db)):
    """Cadastra um novo lanche no cardápio."""
    novo = models.Lanche(**lanche.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)  # recarrega para pegar o id gerado pelo banco
    return novo


@router.delete("/{lanche_id}")
def remover_lanche(lanche_id: int, db: Session = Depends(get_db)):
    """Remove um lanche do cardápio."""
    lanche = db.get(models.Lanche, lanche_id)
    if lanche is None:
        raise HTTPException(status_code=404, detail="Lanche não encontrado neste multiverso")
    db.delete(lanche)
    db.commit()
    return {"mensagem": f"Lanche {lanche_id} removido do cardápio com um estalo de dedos ✨"}
