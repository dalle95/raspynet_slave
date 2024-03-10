# pin.py

# Importa le librerie necessarie
import machine
import time

# Variabili globali per il pin del sensore e il LED
sensor_pin = None
led = None


# Funzione per configurare i pin
def setup_pins():
    global sensor_pin
    global led

    # Inizializza il pin del sensore come pin ADC (Analog-to-Digital Converter)
    sensor_pin = machine.ADC(4)

    # Inizializza il pin del LED come pin di uscita
    led = machine.Pin("LED", machine.Pin.OUT)


# Funzione per leggere la temperatura
def read_temperature():
    # Leggi il valore ADC dal sensore
    adc_value = sensor_pin.read_u16()

    # Calcola la tensione in base al valore ADC
    volt = (3.3 / 65535) * adc_value

    # Calcola la temperatura in base alla tensione
    temperature = 27 - (volt - 0.706) / 0.001721

    # Arrotonda la temperatura a una cifra decimale
    return round(temperature, 1)


# Funzione per lampeggiare il LED
def blink_led():
    # Accendi il LED per mezzo secondo
    led.value(1)
    time.sleep(0.5)

    # Spegni il LED
    led.value(0)
