#FROM nvidia/cuda:12.3.2-devel-ubuntu20.04

#ENV DEBIAN_FRONTEND=noninteractive

# 1. Instalar Python 3.11 desde deadsnakes
#RUN apt-get update && apt-get install -y \
#    software-properties-common \
#    && add-apt-repository ppa:deadsnakes/ppa -y \
#    && apt-get update \
#    && apt-get install -y \
#        python3.11 \
#        python3.11-venv \
#        python3.11-dev \
#        python3-pip \
#    && rm -rf /var/lib/apt/lists/*

# 2. Configurar Python 3.11 como predeterminado
#RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Directorio de trabajo
#WORKDIR /workspace

# Copiar requirements e instalar dependencias
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
#COPY . .

# Exponer puerto de Streamlit
#EXPOSE 8501

# Comando de arranque
#CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

FROM python:3.12.11-slim-bookworm

WORKDIR /service

# Instalar dependencias necesarias para face_recognition
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copiar todos los archivos
COPY . /service/

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto
EXPOSE 8000

# Ejecutar Gunicorn + UvicornWorker
CMD ["gunicorn", "app.main:app",  "-w", "4", "-b", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker", "--capture-output", "--log-level=info"]