# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Installer les paquets nécessaires
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installer les dépendances Python
RUN pip3 install --no-cache-dir fastapi "uvicorn[standard]" sqlalchemy "python-jose[cryptography]" "passlib[bcrypt]"

RUN pip3 install psycopg2-binary python-multipart requests

#EXPOSE 8000
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["python", "main.py"]
