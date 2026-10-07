# Cantina Nerd — API de lanches de filmes e séries

API simples e didática de uma cantina nerd: os lanches (Cerveja Amanteigada, Pão de Lembas, Ramen do Ichiraku...) ficam guardados em um banco **PostgreSQL** e a **API FastAPI** sobe junto pelo **Docker Compose**.

## Como rodar

```bash
docker compose up --build
```

Depois acesse:

- API: <http://localhost:8000>
- Documentação interativa (Swagger): <http://localhost:8000/docs>

A primeira execução já cria a tabela e popula o cardápio com lanches dos filmes e séries. 🍺✨

## Estrutura do projeto

```
api-compose/
├── compose.yaml         # orquestra os dois serviços (api + db)
├── Dockerfile           # imagem da API FastAPI
├── requirements.txt     # dependências Python
└── app/
    ├── main.py          # cria o app FastAPI e registra os routers
    ├── models.py        # modelos ORM (SQLAlchemy): as tabelas do banco
    ├── schemas.py       # schemas Pydantic: formato do JSON que entra e sai
    ├── database.py      # engine, sessões e a dependência get_db
    ├── seed.py          # cardápio inicial (inserido se a tabela estiver vazia)
    └── routers/
        └── cardapio.py  # endpoints do cardápio (GET/POST/DELETE)
```

## O que observar (pontos didáticos)

- **Dois serviços**: `api` (FastAPI) e `db` (Postgres) conversando pela rede interna do Compose.
- **Hostname do banco**: dentro do container, o Postgres é acessado pelo nome do serviço (`db`), não por `localhost`. Veja `DATABASE_URL` no `compose.yaml`.
- **Variáveis de ambiente**: as credenciais do banco ficam no `compose.yaml` e são lidas pelo código (`os.getenv` em `app/database.py`).
- **Volume**: os dados do Postgres persistem no volume `db_data` — pare e suba de novo e os lanches continuam lá.
- **healthcheck + depends_on**: a API só sobe depois que o banco responde que está pronto.
- **--reload + volume de código**: o código local é montado em `/app`, então editar o código recarrega a API automaticamente.
- **ORM x schemas**: compare `app/models.py` (como o dado é guardado no Postgres, via SQLAlchemy) com `app/schemas.py` (como o dado entra e sai da API em JSON, via Pydantic). A sessão do banco chega nas rotas por injeção de dependência (`Depends(get_db)`).

## Comandos úteis

```bash
docker compose up --build     # sobe tudo
docker compose up -d          # sobe em background
docker compose ps             # lista os serviços
docker compose logs -f api    # acompanha os logs da API
docker compose down           # para tudo (mantém os dados)
docker compose down -v        # para tudo e apaga o volume do banco
```

## Testando a API

```bash
curl http://localhost:8000/cardapio                    # lista os lanches
curl http://localhost:8000/cardapio/1                  # detalhe de um lanche

curl -X POST http://localhost:8000/cardapio \
  -H "Content-Type: application/json" \
  -d '{"nome": "Feijoada do Hagrid", "descricao": "Receita secreta das cabanas de Hogwarts", "preco": 32.00, "obra_origem": "Harry Potter"}'

curl -X DELETE http://localhost:8000/cardapio/1        # remove um lanche
```
