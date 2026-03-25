# Imagem base com GDAL/GEOS já compilados — evita horas de build
FROM ghcr.io/osgeo/gdal:ubuntu-small-3.8.5

# Python + pip
RUN apt-get update && apt-get install -y python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependências Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia o código
COPY main.py relatorio.py ./

# Porta padrão Render
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
