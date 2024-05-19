Actualizar registro DNS de Cloudflare - DDNS
======================

## Referencia rápida

-	**Cloudflare DDNS Updater**
-	**Requisitos**
-	**Variables de Entorno**
-	**Uso**
-	**Environment variables desde archivo (Docker secrets)**
-	**Arquitectura soportada**
-	**Uso en raspberry**
-	**Te invito a visitar mi portafolio**

# Cloudflare DDNS Updater

Este proyecto proporciona un script en Python que actualiza automáticamente el registro DNS de Cloudflare con la IP pública actual del servidor. Esto es útil para configurar un Dynamic DNS (DDNS).

## Requisitos

- Docker
- Cuenta en Cloudflare
- Token de API de Cloudflare con permisos para editar registros DNS

## Variables de Entorno

El script utiliza las siguientes variables de entorno para su configuración:

| Variable      | Función                                                      |
| ------------- | ------------------------------------------------------------ |
| `-e CLOUDFLARE_EMAIL`     | Tu correo electrónico asociado a la cuenta de Cloudflare. |
| `-e CLOUDFLARE_API_TOKEN` | El token de API de Cloudflare con los permisos necesarios. |
| `-e ZONE_ID`  | El ID de la zona de Cloudflare donde se encuentra el registro DNS. |
| `-e DNS_RECORD_NAME`      | El nombre del registro DNS que se actualizará (por ejemplo, `ddns.yonier.com`). |
| `-e SLEEP_INTERVAL`      | Intervalo de tiempo en segundos entre cada verificación de la IP (predeterminado: `600`). |


## Uso

### docker-compose (recomendado)
Fichero compose.yaml

```yaml
---
version: '3.8'
services:
  cloudflare-ddns-updater:
    image: cloudflare-ddns-updater
    restart: always
    environment:
      - CLOUDFLARE_EMAIL=${CLOUDFLARE_EMAIL}
      - CLOUDFLARE_API_TOKEN=${CLOUDFLARE_API_TOKEN}
      - ZONE_ID=${ZONE_ID}
      - DNS_RECORD_NAME=${DNS_RECORD_NAME}
      - SLEEP_INTERVAL=${SLEEP_INTERVAL}
    env_file:
      - variables.env
...
```

### *. Construir la Imagen de Docker

```bash
docker run -d \
  --name cloudflare-ddns-updater \
  -e CLOUDFLARE_EMAIL=tu_correo_ejemplo@dominio.com \
  -e CLOUDFLARE_API_TOKEN=tu_token_de_api \
  -e ZONE_ID=tu_zone_id \
  -e DNS_RECORD_NAME=subdominio.dominio.com \
  -e SLEEP_INTERVAL=600 \
  cloudflare-ddns-updater
```

#### Environment variables desde archivo (Docker secrets)

Se recomienda pasar la variable `CLOUDFLARE_API_TOKEN` a través de un archivo.

fichero oculto .variables.env

```bash
CLOUDFLARE_EMAIL=miemail@ejemplo.com
CLOUDFLARE_API_TOKEN=miTokenDeApi
ZONE_ID=miZoneId
DNS_RECORD_NAME=subdominio.ejemplo.com
SLEEP_INTERVAL=300
```

Crear contenedor docker-compose
```yaml
---
version: '3.8'
services:
  cloudflare-ddns-updater:
    image: cloudflare-ddns-updater
    restart: always
    env_file:
      - variables.env
...
```

Crear contenedor docker cli
```bash
docker run -d \
  --name cloudflare-ddns-updater \
  --env-file variables.env \
  cloudflare-ddns-updater
```

## Arquitectura soportada

La arquitectura soportada es la siguiente:

| Arquitectura | Disponible | Tag descarga                 |
| ------------ | ---------- | ---------------------------- |
| x86-64       | ✅          | docker pull neytor/cloudflare-ddns-updater     |
| arm64        | ✅          | docker pull neytor/cloudflare-ddns-updater:arm |

## Uso en raspberry

Solo cambia la versión de la imagen por la arquitectura soportada.

## Uso manual

Si desea ejecutar el código de manera manual es decir sin usar docker, puede crear un fichero con extensión .py y ejecutar el código reemplazando los campos correspondientes

```python
import requests
import json

# Tu dirección de correo electrónico de Cloudflare
CLOUDFLARE_EMAIL = 'ddns@gmail.com'
# Tu token de API de Cloudflare
CLOUDFLARE_API_TOKEN = 'xxxxx'
# El ID de la zona de Cloudflare (puedes encontrarlo en el panel de Cloudflare)
ZONE_ID = 'xxxxxxxxx'
# El nombre del registro DNS que deseas actualizar (por ejemplo, 'subdominio.dominio.com')
DNS_RECORD_NAME = 'subdominio.dominio.com'

def get_public_ip():
    """Obtiene la IP pública del servidor."""
    response = requests.get('https://api.ipify.org?format=json')
    ip = response.json()['ip']
    return ip

def get_dns_record_id(zone_id, record_name):
    """Obtiene el ID del registro DNS basado en su nombre."""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name={record_name}"
    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_API_TOKEN,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    
    if data['success'] and data['result']:
        return data['result'][0]['id']
    else:
        raise Exception(f"No se encontró el registro DNS con el nombre {record_name}")

def update_dns_record(zone_id, record_id, record_name, ip):
    """Actualiza el registro DNS en Cloudflare."""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_API_TOKEN,
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'A',  # Tipo de registro, puede ser 'A' para IPv4 o 'AAAA' para IPv6
        'name': record_name,
        'content': ip,
        'ttl': 1,  # Configuración del TTL (1 es automático)
        'proxied': False  # Ajustar según sea necesario
    }

    response = requests.put(url, headers=headers, data=json.dumps(data))
    return response.json()

def main():
    # Obtener la IP pública actual
    current_ip = get_public_ip()
    print(f'IP pública actual: {current_ip}')

    # Obtener el ID del registro DNS basado en el nombre
    try:
        record_id = get_dns_record_id(ZONE_ID, DNS_RECORD_NAME)
        print(f'ID del registro DNS: {record_id}')
        
        # Actualizar el registro DNS en Cloudflare
        result = update_dns_record(ZONE_ID, record_id, DNS_RECORD_NAME, current_ip)
        print('Respuesta de la API de Cloudflare:', result)
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()
```
> Nota: Puedes crear un cron para que se ejecute el tiempo que desees. crontab -e y pasar */30 * * * * /ruta/al/script.sh 
        con esto queremos decir que el script se ejecutará cada 30 minutos.

## Te invito a visitar mi portafolio
https://yonier.com


[![Try in PWD](https://github.com/play-with-docker/stacks/raw/cff22438cb4195ace27f9b15784bbb497047afa7/assets/images/button.png)](http://play-with-docker.com?stack=https://raw.githubusercontent.com/docker-library/docs/db214ae34137ab29c7574f5fbe01bc4eaea6da7e/wordpress/stack.yml)

