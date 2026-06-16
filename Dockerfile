# Usa la imagen base de Python 3.12 en Alpine
FROM python:alpine

# Crea usuario no-root antes de instalar dependencias
RUN adduser -D -h /app appuser

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias necesarias
RUN pip install --no-cache-dir requests

# Copia el script de Python a la imagen
COPY --chown=appuser:appuser cloudflare_ddns.py .

USER appuser

# Comando para ejecutar el script
CMD ["python", "cloudflare_ddns.py"]
