# get_config.py

# Importa la libreria 'ujson' con alias 'json'
import ujson as json

# Definizione dei valori di default per la configurazione
CONFIG = {
    "ssid": "Vodafone-C01920097",
    "ssid_password": "bAFmbRxf9CZAraxs",
    "broker": "192.168.1.15",
    "sensor_pin": 4,
    "client_id": "PICO-1",
    "topic": "test_topic"
}


# Funzione per caricare la configurazione dal file 'config.json'
def load_config():
    try:
        # Apri il file 'config.json' in modalità lettura
        with open("../config.json") as f:
            # Carica il contenuto del file JSON
            config = json.loads(f.read())
    except (OSError, ValueError):
        # Gestisci eventuali errori durante il caricamento della configurazione
        print("Couldn't load /config.json")
        # Salva la configurazione di default nel file
        save_config()
    else:
        # Aggiorna la configurazione con i valori letti dal file
        CONFIG.update(config)
        # Stampa un messaggio indicando che la configurazione è stata caricata con successo
        print("Loaded config from /config.json")

    # Restituisci la configurazione letta dal file
    return config


# Funzione per salvare la configurazione nel file 'config.json'
def save_config():
    try:
        # Apri il file 'config.json' in modalità scrittura
        with open("../config.json", "w") as f:
            # Scrivi la configurazione nel file come stringa JSON
            f.write(json.dumps(CONFIG))
    except OSError:
        # Gestisci eventuali errori durante il salvataggio della configurazione
        print("Couldn't save /config.json")
