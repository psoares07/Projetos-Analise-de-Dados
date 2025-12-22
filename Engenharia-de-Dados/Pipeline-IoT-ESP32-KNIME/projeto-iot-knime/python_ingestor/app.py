import os
import json
import time
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import psycopg2
from datetime import datetime

# --- CONFIGURAÇÕES DE AMBIENTE  ---

MQTT_BROKER = os.getenv('MQTT_BROKER', 'mosquitto') # Default 'mosquitto' é aceitável aqui
MQTT_TOPIC = "sensores/dados"

# Credenciais do Banco
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_NAME = os.getenv('DB_NAME')  # Pega do .env via Docker
DB_USER = os.getenv('DB_USER')  # Pega do .env via Docker
DB_PASS = os.getenv('DB_PASS')  # Pega do .env via Docker

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"[ERRO DB] Falha ao conectar no Postgres: {e}")
        print(f"Debug Info -> Host: {DB_HOST}, User: {DB_USER}, DB: {DB_NAME}")
        return None

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"[RECEBIDO] Tópico: {msg.topic} | Payload: {payload}")
    
    try:
        dados = json.loads(payload)
        
        # Validar dados essenciais (Data Quality)
        if 'temperature_c' not in dados or 'sensor_id' not in dados:
            print("[ALERTA] JSON incompleto ignorado.")
            return

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            query = """
                INSERT INTO tb_medicoes (sensor_id, location, temperature_c, humidity_pct, luminosity_raw)
                VALUES (%s, %s, %s, %s, %s)
            """
            cur.execute(query, (
                dados.get('sensor_id'),
                dados.get('location'),
                dados.get('temperature_c'),
                dados.get('humidity_pct'),
                dados.get('luminosity_raw')
            ))
            conn.commit()
            cur.close()
            conn.close()
            print("[SUCESSO] Dado persistido no PostgreSQL.")
        else:
            print("[ERRO] Não foi possível salvar no banco (sem conexão).")

    except json.JSONDecodeError:
        print("[ERRO] Payload não é um JSON válido.")
    except Exception as e:
        print(f"[ERRO GERAL] {e}")

# --- SETUP DO MQTT ---
def start_worker():
    print("Iniciando Worker de Ingestão IoT...")
    # Aguarda o Postgres acordar totalmente
    time.sleep(10) 
    
    # Inicialização API V2
    client = mqtt.Client(CallbackAPIVersion.VERSION2)
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, 1883, 60)
        client.subscribe(MQTT_TOPIC)
        print(f"Inscrito no tópico: {MQTT_TOPIC}")
        print(f"Conectado ao Broker: {MQTT_BROKER}")
        client.loop_forever()
    except Exception as e:
        print(f"[ERRO FATAL MQTT] {e}")
        time.sleep(5)
        start_worker()

if __name__ == "__main__":
    start_worker()
