<p align="center">
  <img src="https://cdn.simpleicons.org/cloudflare/F38020" width="80" alt="Cloudflare">
</p>

<h1 align="center">Cloudflare DDNS Updater</h1>

<p align="center">
  Contenedor Docker multi-arquitectura que mantiene tus registros DNS de Cloudflare sincronizados con tu IP pública.
</p>

<p align="center">
  <a href="https://github.com/YonierGomez/cloudflare-ddns-updater/stargazers"><img src="https://img.shields.io/github/stars/YonierGomez/cloudflare-ddns-updater?style=flat-square&color=f97316" alt="Stars"></a>
  <a href="https://github.com/YonierGomez/cloudflare-ddns-updater/issues"><img src="https://img.shields.io/github/issues/YonierGomez/cloudflare-ddns-updater?style=flat-square&color=ef4444" alt="Issues"></a>
  <a href="https://github.com/YonierGomez/cloudflare-ddns-updater/releases"><img src="https://img.shields.io/github/v/release/YonierGomez/cloudflare-ddns-updater?style=flat-square&color=10b981" alt="Release"></a>
  <a href="https://hub.docker.com/r/neytor/cloudflare-ddns-updater"><img src="https://img.shields.io/docker/pulls/neytor/cloudflare-ddns-updater?style=flat-square&color=2563eb" alt="Docker Pulls"></a>
  <a href="https://hub.docker.com/r/neytor/cloudflare-ddns-updater"><img src="https://img.shields.io/docker/image-size/neytor/cloudflare-ddns-updater/latest?style=flat-square&color=8b5cf6" alt="Image Size"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Cloudflare-F38020?style=flat-square&logo=cloudflare&logoColor=white" alt="Cloudflare">
  <img src="https://img.shields.io/badge/Alpine_Linux-0D597F?style=flat-square&logo=alpinelinux&logoColor=white" alt="Alpine">
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions">
</p>

---

## Arquitecturas soportadas

| Arquitectura | Plataforma | Dispositivos |
|---|---|---|
| amd64 | linux/amd64 | Servidores, PCs, VPS |
| arm64 | linux/arm64 | Raspberry Pi 4, Raspberry Pi 5, Orange Pi, Apple Silicon |
| armv7 | linux/arm/v7 | Raspberry Pi 2, Raspberry Pi 3, Orange Pi Zero/One |

> Compatible con cualquier placa ARM: Raspberry Pi, Orange Pi, Banana Pi, Rock Pi, ODROID, etc.

## Requisitos

- Docker
- Cuenta en Cloudflare
- Token de API de Cloudflare con permisos para editar registros DNS

## Variables de entorno

| Variable | Descripción | Default |
|---|---|---|
| `CLOUDFLARE_EMAIL` | Email de tu cuenta Cloudflare | — |
| `CLOUDFLARE_API_TOKEN` | API Key o Token de Cloudflare | — |
| `ZONE_ID` | Zone ID del dominio en Cloudflare | — |
| `DNS_RECORD_NAME` | Registros DNS separados por coma | — |
| `SLEEP_INTERVAL` | Segundos entre verificaciones | `600` |
| `PROXY_ENABLED` | Activar proxy de Cloudflare | `true` |

## Uso

### Docker Compose (recomendado)

```yaml
services:
  cloudflare-ddns:
    image: neytor/cloudflare-ddns-updater:latest
    container_name: cloudflare-ddns
    restart: unless-stopped
    env_file:
      - variables.env
```

Fichero `variables.env`:

```bash
CLOUDFLARE_EMAIL=tu@email.com
CLOUDFLARE_API_TOKEN=tu-api-token
ZONE_ID=tu-zone-id
DNS_RECORD_NAME=ejemplo.com,sub.ejemplo.com
SLEEP_INTERVAL=300
PROXY_ENABLED=true
```

### Docker CLI

```bash
docker run -d \
  --name cloudflare-ddns \
  --restart unless-stopped \
  -e CLOUDFLARE_EMAIL="tu@email.com" \
  -e CLOUDFLARE_API_TOKEN="tu-api-token" \
  -e ZONE_ID="tu-zone-id" \
  -e DNS_RECORD_NAME="ejemplo.com,sub.ejemplo.com" \
  -e SLEEP_INTERVAL=300 \
  -e PROXY_ENABLED=true \
  neytor/cloudflare-ddns-updater:latest
```

### Raspberry Pi / Orange Pi / Placas ARM

No necesitas hacer nada especial. La imagen es multi-arquitectura, Docker detecta automáticamente tu plataforma:

```bash
# Funciona igual en RPi 5, Orange Pi, o cualquier placa ARM
docker pull neytor/cloudflare-ddns-updater:latest
```

## CI/CD

Este proyecto usa GitHub Actions con:

- **Auto-Release**: Detecta nuevas versiones de Python semanalmente, hace build multi-arch y crea un release con changelog
- **PR Validation**: Valida que el Dockerfile compile para las 3 arquitecturas antes de mergear

## Uso manual (sin Docker)

Si prefieres ejecutar el script directamente:

```bash
pip install requests
export CLOUDFLARE_EMAIL="tu@email.com"
export CLOUDFLARE_API_TOKEN="tu-api-token"
export ZONE_ID="tu-zone-id"
export DNS_RECORD_NAME="ejemplo.com"
python cloudflare_ddns.py
```

> También puedes usar cron: `*/30 * * * * /ruta/al/script.sh` para ejecutar cada 30 minutos.

---

<p align="center">
  <a href="https://yonier.com">yonier.com</a> · 
  <a href="https://hub.docker.com/r/neytor/cloudflare-ddns-updater">Docker Hub</a>
</p>
