# main.py

import sys
import time
import json
import machine
from umqtt.simple import MQTTClient

# Importa funzioni personalizzate dal modulo 'functions'
from functions import wifi_connection
from functions import get_config
from functions import pin
from functions import webserver

# Aggiungi il percorso della sottodirectory 'functions' al sys.path
sys.path.insert(0, './functions')

# Intervallo di pubblicazione MQTT
publish_interval = 5
last_publish = time.time()


# Callback per i messaggi MQTT ricevuti
def sub_cb(topic, msg):
    print((topic, msg))
    if msg.decode() == "ON":
        pin.led.value(1)
    else:
        pin.led.value(0)


# Funzione di reset
def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()


# Funzione principale
def main(CONFIG, ip):
    print(f"Begin connection with MQTT Broker :: {CONFIG['broker']}")
    mqttClient = MQTTClient(CONFIG['client_id'], CONFIG['broker'], keepalive=60)
    # mqttClient.set_callback(sub_cb)
    mqttClient.connect()
    # mqttClient.subscribe(SUBSCRIBE_TOPIC)
    print(f"Connected to MQTT Broker :: {CONFIG['broker']}, and waiting for callback function to be called!")

    while True:
        # Controllo non bloccante per eventuali messaggi MQTT
        # mqttClient.check_msg()
        global last_publish
        if (time.time() - last_publish) >= publish_interval:
            # Leggi la temperatura utilizzando la funzione del modulo 'pin'
            data = pin.read_temperature()

            json_message = {
                "client": CONFIG['client_id'],
                "sensore": "Temperatura",
                "valore": data
            }

            # Serializza il JSON in una stringa
            message_string = json.dumps(json_message)

            # Pubblica il dato sulla temperatura sul topic MQTT
            mqttClient.publish(CONFIG['topic'], str(message_string).encode())

            print('Topic: {} | Message: {}'.format(CONFIG['topic'], message_string))

            # Aggiorna il timestamp dell'ultima pubblicazione
            last_publish = time.time()

            # Esegui un lampeggio del LED
            pin.blink_led()

        # Attendi per un breve periodo
        time.sleep(0.5)


# Blocco principale eseguito solo se questo script è il principale
if __name__ == "__main__":

    # Carica la configurazione dal modulo 'get_config'
    CONFIG = get_config.load_config()

    print("Connecting to your wifi...")

    # Esegui la connessione WiFi utilizzando il modulo 'wifi_connection'
    ip = wifi_connection.do_connect(CONFIG)

    # Configura i pin utilizzando il modulo 'pin'
    pin.setup_pins()

    while True:
        try:
            # Esegui la funzione principale
            main(CONFIG, ip)
        except OSError as e:
            print("Error: " + str(e))

            # In caso di errore, esegui un reset del dispositivo
            reset()
