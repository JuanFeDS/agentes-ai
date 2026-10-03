FROM python:3.12-slim

# Crear directorio de trabajo
WORKDIR /infoagent

# Instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY src/ ./src
COPY data/ ./data
COPY main.py ./ 

# Ejecutar el entrypoint
CMD ["python", "main.py"]
