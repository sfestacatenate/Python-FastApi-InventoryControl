# Dockerfile
FROM python:3.9-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file requirements.txt e installa le dipendenze
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia il contenuto della directory app e static nella directory di lavoro
COPY ./app ./app

# Esponi la porta 8000
EXPOSE 8000

# Comando per avviare il server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]