# ---------------------------
# Étape 1 : Image de base
# ---------------------------
FROM python:3.11-slim

# ---------------------------
# Étape 2 : Variables d'environnement
# ---------------------------
# Empêche Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Buffers stdout/stderr pour voir les logs en temps réel
ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
