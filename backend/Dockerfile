# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependências de compilação, bibliotecas para OpenCV e curl
RUN apt-get update && apt-get install -y \
    gcc g++ build-essential \
    libgl1-mesa-glx libglib2.0-0 \
    libsm6 libxext6 libxrender1 \
    ffmpeg \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Cache de dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install motor

# Copiar código da aplicação
COPY . .

# Expõe a porta
EXPOSE 8000

# Inicia o servidor FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
