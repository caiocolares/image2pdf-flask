# Use uma imagem base do Python
FROM python:3.13.7-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para pdf2image e Pillow
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta que a aplicação usa
EXPOSE 5000

# Define variáveis de ambiente
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Comando para executar a aplicação com Gunicorn (produção)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "main:app"]
