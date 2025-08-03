# Image de base légère avec Python 3.11
FROM python:3.11-slim

# Empêche les fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Active le mode unbuffered (utile pour logs)
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg gcc libffi-dev libssl-dev && update-ca-certificates && rm -rf /var/lib/apt/lists/*


ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV REQUEST_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV PIP_CERT=/etc/ssl/certs/ca-certificates.crt

# Crée un dossier pour l'app
WORKDIR /app

# Copie les fichiers nécessaires
COPY requirements.txt .
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y plantuml default-jre
COPY . .

# Commande de lancement par défaut
CMD ["python", "main.py"]
