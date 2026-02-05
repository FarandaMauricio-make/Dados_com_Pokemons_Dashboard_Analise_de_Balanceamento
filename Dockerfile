# Usar imagem base do Python
FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos para dentro do container
COPY . .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando de inicialização
CMD ["streamlit", "run", "Pokemon_Balance.py", "--server.port=8501", "--server.headless=true"]
