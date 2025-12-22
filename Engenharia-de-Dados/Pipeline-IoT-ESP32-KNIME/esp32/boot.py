# boot.py - Gerenciamento de Rede
import network
import time
import secrets

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('Conectando ao Wi-Fi...')
        wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        timeout = 0
        while not wlan.isconnected() and timeout < 10:
            time.sleep(1)
            timeout += 1
            print('.', end='')
    
    if wlan.isconnected():
        print('\nConectado! IP:', wlan.ifconfig()[0])
    else:
        print('\nFalha na conexão Wi-Fi.')

# Executa a conexão ao iniciar
connect_wifi()