import os
import requests
import json
import time
from datetime import datetime

# Obtener variables de entorno
CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
ZONE_ID = os.getenv('ZONE_ID')
DNS_RECORD_NAMES = os.getenv('DNS_RECORD_NAME').split(',')  # Separar los nombres por comas
SLEEP_INTERVAL = int(os.getenv('SLEEP_INTERVAL', 600))  # Valor predeterminado de 600 segundos
PROXY_ENABLED = os.getenv('PROXY_ENABLED', 'True').lower() == 'true'

def log_message(message):
    """Imprime un mensaje de log con marca de tiempo."""
    print(f"[{datetime.now().isoformat()}] {message}")

def get_public_ip():
    """Obtiene la IP pública del servidor."""
    log_message("Obteniendo IP pública...")
    response = requests.get('https://api.ipify.org?format=json')
    ip = response.json()['ip']
    log_message(f"IP pública obtenida: {ip}")
    return ip

def get_dns_record_id(zone_id, record_name):
    """Obtiene el ID del registro DNS basado en su nombre."""
    log_message(f"Obteniendo ID del registro DNS para {record_name}...")
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name={record_name.strip()}"
    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_API_TOKEN,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if data['success'] and data['result']:
        record_id = data['result'][0]['id']
        log_message(f"ID del registro DNS obtenido para {record_name}: {record_id}")
        return record_id
    else:
        log_message(f"Error: No se encontró el registro DNS con el nombre {record_name}")
        raise Exception(f"No se encontró el registro DNS con el nombre {record_name}")

def update_dns_record(zone_id, record_id, record_name, ip, proxied=True):
    """Actualiza el registro DNS en Cloudflare."""
    log_message(f"Actualizando registro DNS {record_name} con IP {ip}...")
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_API_TOKEN,
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'A',
        'name': record_name.strip(),
        'content': ip,
        'ttl': 1,
        'proxied': proxied
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    result = response.json()
    log_message(f"Respuesta de la API de Cloudflare para {record_name}: {json.dumps(result, indent=2)}")
    return result

def main():
    current_ip = None
    record_ids = {}
    
    log_message("Iniciando el script de actualización de DNS...")
    log_message(f"Registros DNS a actualizar: {', '.join(DNS_RECORD_NAMES)}")
    log_message(f"Intervalo de verificación: {SLEEP_INTERVAL} segundos")
    log_message(f"Proxy habilitado: {PROXY_ENABLED}")
    
    while True:
        try:
            new_ip = get_public_ip()
            if new_ip != current_ip:
                log_message(f'Nueva IP detectada: {new_ip}')
                
                for record_name in DNS_RECORD_NAMES:
                    record_name = record_name.strip()
                    if record_name not in record_ids:
                        record_ids[record_name] = get_dns_record_id(ZONE_ID, record_name)
                    
                    result = update_dns_record(ZONE_ID, record_ids[record_name], record_name, new_ip, proxied=PROXY_ENABLED)
                    if result['success']:
                        log_message(f"Actualización exitosa para {record_name}")
                    else:
                        log_message(f"Error en la actualización para {record_name}: {result['errors']}")
                
                current_ip = new_ip
            else:
                log_message('La IP no ha cambiado.')
            
            log_message(f"Esperando {SLEEP_INTERVAL} segundos antes de la próxima verificación...")
            time.sleep(SLEEP_INTERVAL)
        except Exception as e:
            log_message(f'Error: {e}')
            log_message(f"Reintentando en {SLEEP_INTERVAL} segundos...")
            time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    main()