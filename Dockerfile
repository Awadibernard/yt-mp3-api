FROM python:3.11-slim

# Empêche Python de buffer les logs (utile pour Koyeb)
ENV PYTHONUNBUFFERED=1

# Dossier de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --no-cache-dir yt-dlp flask gunicorn

# Copier le serveur
COPY server.py /app/server.py
COPY cookies.txt /app/cookies.txt

# Exposer le port (informatif pour Docker)
EXPOSE 8080

# ⚠️ COMMANDE CRITIQUE POUR KOYEB
CMD gunicorn server:app --bind 0.0.0.0:$PORT
