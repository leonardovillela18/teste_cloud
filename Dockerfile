# Escolha da imagem base
FROM python:3.13-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar e instalar dependências primeiro (aproveita o cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expor a porta (apenas documentação; quem publica é o compose.yaml)
EXPOSE 8000

# Subir a API com hot-reload (útil em aula: editar o código já reflete)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
