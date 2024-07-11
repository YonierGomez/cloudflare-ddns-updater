import os
import requests
import json
import time

# Obtener variables de entorno
CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
ZONE_ID = os.getenv('ZONE_ID')
DNS_RECORD_NAMES = os.getenv('DNS_RECORD_NAME').split(',')  # Separar los nombres por comas
SLEEP_INTERVAL = int(os.getenv('SLEEP_INTERVAL', 600))  # Valor predeterminado de 600 segundos

def get_public_ip():
    """Obtiene la IP pública del servidor."""
    response = requests.get('https://api.ipify.org?format=json')
    ip = response.json()['ip']
    return ip

def get_dns_record_id(zone_id, record_name):
    """Obtiene el ID del registro DNS basado en su nombre."""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name={record_name.strip()}"
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
        'type': 'A',
        'name': record_name.strip(),
        'content': ip,
        'ttl': 1,
        'proxied': False
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    return response.json()

def main():
    current_ip = None
    record_ids = {}
    
    while True:
        try:
            new_ip = get_public_ip()
            if new_ip != current_ip:
                print(f'Nueva IP detectada: {new_ip}')
                
                for record_name in DNS_RECORD_NAMES:
                    record_name = record_name.strip()
                    # Obtener el ID del registro DNS basado en el nombre, solo la primera vez o si falla
                    if record_name not in record_ids:
                        record_ids[record_name] = get_dns_record_id(ZONE_ID, record_name)
                        print(f'ID del registro DNS para {record_name}: {record_ids[record_name]}')
                    
                    # Actualizar el registro DNS en Cloudflare
                    result = update_dns_record(ZONE_ID, record_ids[record_name], record_name, new_ip)
                    print(f'Respuesta de la API de Cloudflare para {record_name}:', result)
                
                # Actualizar la IP almacenada
                current_ip = new_ip
            else:
                print('La IP no ha cambiado.')
            
            # Espera antes de la próxima verificación
            time.sleep(SLEEP_INTERVAL)
        except Exception as e:
            print(f'Error: {e}')
            time.sleep(SLEEP_INTERVAL)  # Espera antes de intentar nuevamente en caso de error

if __name__ == "__main__":
    main()