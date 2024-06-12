# Usa la imagen base de Python 3.12 en Alpine
FROM python:alpine

# Establece el directorio de trabajo
WORKDIR /app

# Copia el script de Python a la imagen
COPY cloudflare_ddns.py .

# Instala las dependencias necesarias
RUN pip install requests

# Comando para ejecutar el script
CMD ["python", "cloudflare_ddns.py"]
