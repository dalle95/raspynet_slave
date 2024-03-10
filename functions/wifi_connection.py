# wifi_connection.py

# Importa le librerie necessarie
import network
import utime


# Funzione per stabilire la connessione WiFi
def do_connect(CONFIG):
    # Ottieni un'istanza del modulo WLAN
    sta_if = network.WLAN(network.STA_IF)

    # Verifica se il modulo WLAN è già connesso
    if not sta_if.isconnected():
        print('Connecting to network...')

        # Attiva il modulo WLAN
        sta_if.active(True)

        # Prova a connettersi alla rete WiFi utilizzando le credenziali dalla configurazione
        sta_if.connect(CONFIG['ssid'], CONFIG['ssid_password'])

        # Attendi fino a quando il modulo WLAN è connesso
        while not sta_if.isconnected():
            print("Attempting to connect....")
            utime.sleep(1)

    # Stampa un messaggio di connessione riuscita e visualizza la configurazione di rete
    print('Connected! Network config:', sta_if.ifconfig())

    # Restituisci l'indirizzo IP assegnato
    ip = sta_if.ifconfig()[0]
    return ip
