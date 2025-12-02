FROM python:3.9-slim

# 1. Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Configura diretório de trabalho
WORKDIR /app

# 3. Copia primeiro o requirements.txt
COPY requirements.txt .

# 4. Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todo o conteúdo (incluindo a pasta app)
COPY . .

# 6. Configura variáveis para o Ultralytics
ENV YOLO_CONFIG_DIR=/tmp
ENV YOLO_DISABLE_DOWNLOADS=1
ENV PYTHONPATH=/app 

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]