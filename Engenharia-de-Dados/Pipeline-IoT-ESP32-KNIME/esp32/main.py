# main.py - Coleta e Estruturação de Dados
import time
import machine
import dht
from umqtt.simple import MQTTClient
import ujson # Biblioteca otimizada para JSON
import secrets # <--- Importamos as credenciais aqui

# --- CONFIGURAÇÃO DE HARDWARE ---
# Sensor DHT11 no GPIO 48
try:
    sensor_dht = dht.DHT11(machine.Pin(48))   ## GPIO 48
except Exception as e:
    print("Erro ao inicializar DHT:", e)

# Sensor LDR no GPIO 7
# Atenuação de 11dB para ler faixa completa de 0-3.3v
ldr = machine.ADC(machine.Pin(7))     ## GPIO 7
ldr.atten(machine.ADC.ATTN_11DB) 

# --- METADADOS (Importante para DMBOK) ---
SENSOR_ID = "esp32_lab_01"
LOCATION = "escritorio_home"

# --- Configuração MQTT ---
# Não colocamos mais IPs ou Portas aqui
MQTT_SERVER = secrets.MQTT_SERVER
MQTT_PORT = secrets.MQTT_PORT
MQTT_TOPIC = secrets.MQTT_TOPIC


def conectar_mqtt():
    try:
        # Usa o Client ID definido no secrets ou gera um aleatório
        client = MQTTClient(secrets.MQTT_CLIENT_ID, MQTT_SERVER, port=MQTT_PORT)
        client.connect()
        print(f"Conectado ao broker MQTT em {MQTT_SERVER}")
        return client
    except Exception as e:
        print("Erro ao conectar no MQTT: ", e)
        return None

## TEMPOS
# TEMPO DE INICIO
tempo_inicio = 3
# TEMPO DE COLETA (300s = 5 minutos)
tempo_de_coleta = 300

def ler_sensores():
    try:
        sensor_dht.measure()
        temp = sensor_dht.temperature()
        hum = sensor_dht.humidity()
        
        # Leitura analógica (0 - 4095). 
        # Quanto menor o valor, mais luz (depende do circuito), ou vice-versa.
        lum_raw = ldr.read()
        
        return temp, hum, lum_raw
    except OSError as e:
        print("Erro ao ler sensor DHT11:", e)
        return None, None, None

def main_loop():
    print(f"Iniciando coleta de dados para {SENSOR_ID}...")
    
    # Criamos o cliente fora do loop para tentar manter a conexão,
    # mas sua lógica original de reconectar dentro também funciona para resiliência.
    # Vou manter sua estrutura original de reconexão para garantir robustez.
    
    while True:
        temp, hum, lum = ler_sensores()
        
        if temp is not None:
            # Estruturação do Payload (Schema JSON)
            payload = {
                "sensor_id": SENSOR_ID,
                "location": LOCATION,
                "temperature_c": temp,
                "humidity_pct": hum,
                "luminosity_raw": lum,
                # Timestamp será inserido pelo Banco (Ingestion Time) 
            }
            
            # Serialização para JSON
            mensagem_json = ujson.dumps(payload)
            print(f"[DADOS GERADOS]: {mensagem_json}")
            
            # --- Lógica de Envio ---
            # Tenta conectar a cada envio (Robusto para intervalos longos como 5 min)
            client = conectar_mqtt()
            
            if client is not None:
                try:
                    # --- Publicação no MQTT ---
                    client.publish(MQTT_TOPIC, mensagem_json)
                    print("-> Enviado via MQTT")
                    client.disconnect() # Desconecta limpo para economizar recurso até o próximo ciclo
                except OSError:
                    print("[ERRO] Falha durante publicação.")
            else:
                print("[AVISO] Não foi possível conectar ao Broker neste ciclo.")
            
        else:
            print("[ERRO] Leitura inválida dos sensores. Tentando novamente no próximo ciclo...")
            time.sleep(2)
            continue
            
        # Coleta a cada 5 minutos
        print(f"Aguardando {tempo_de_coleta} segundos...")
        time.sleep(tempo_de_coleta)

# Executar
if __name__ == '__main__':
    print(f"Iniciando as leituras em {tempo_inicio} segundos")
    time.sleep(tempo_inicio)
    main_loop()