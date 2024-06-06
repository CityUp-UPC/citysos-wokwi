import network
import urequests
import time
from machine import I2C, Pin
from i2c_lcd import I2cLcd
from time import sleep, sleep_ms
import json

# Configuración de pines
led = Pin(2, Pin.OUT)
push_button = Pin(13, Pin.IN, Pin.PULL_DOWN)  # Asegúrate de usar Pin.PULL_DOWN

# Configuración de la pantalla LCD
AddressOfLcd = 0x27
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, AddressOfLcd, 2, 16)

# Conectando a WiFi
print("Conectando a la Red", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print("*", end="")
    time.sleep(0.50)
print("\nConexión exitosa!\n")

# Coordenadas y token
latitude = "40.712776"
longitude = "-74.005974"
#COLOCAR TOKEN XD
token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJIaXJvIiwiaWF0IjoxNzE3NjU0NTQ1LCJleHAiOjE3MTc2NTU5ODV9.EIuQ8Pg1ApULxdG37poUej5V-CIJxdAmL5LL3Om0348"

print("Listo! Presione el botón en caso de una Emergencia\n", end="")
lcd.move_to(1, 0)
lcd.putstr('Ready! CITYSOS')
lcd.move_to(2, 1)
lcd.putstr("Alert Police")

while True:
    logic_state = push_button.value()
    #print(f"Estado del botón: {logic_state}")  # Depuración del estado del botón
    if logic_state == 1:
        led.value(1)
        # Envio del requerimiento por HTTPS
        print("Enviando alerta...\n", end="")
        lcd.clear()
        lcd.move_to(3, 0)
        lcd.putstr('Sending...')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        data = {
            'description': "Se solicita Ayuda policial",
            'latitude': latitude,
            'longitude': longitude,
            'address': "Direccion del incidente",
            'district': "Distrito del incidente",
            'citizenId': 1  # Reemplazar con el ID del ciudadano correspondiente
        }
        try:
            # Asegurarse de usar 'data' y no 'json' para evitar encabezados duplicados
            response = urequests.post("https://citysos-api.onrender.com/api/v1/incidents", headers=headers, data=json.dumps(data))
            if response.status_code == 201:
                print(response.text)
                print("Alerta enviada!\n")
                lcd.clear()
                lcd.move_to(1, 0)
                lcd.putstr('Alert sended!')
            else:
                print(f"Error: {response.status_code} - {response.text}")
                lcd.clear()
                lcd.move_to(1, 0)
                lcd.putstr('Error sending alert')
            response.close()
        except Exception as e:
            print(f"An error occurred: {e}\n")
            lcd.clear()
            lcd.move_to(1, 0)
            lcd.putstr('Error sending alert')

        print("Bloqueado por 5 segundos\n", end="")
        lcd.clear()
        lcd.move_to(1, 1)
        lcd.putstr('Blocked 5 sec')
        sleep(5)
        led.value(0)

        lcd.clear()
        lcd.move_to(1, 0)
        lcd.putstr('Ready! CITYSOS')
        lcd.move_to(2, 1)
        lcd.putstr("Alert Police")
        print("Listo! Presione el botón en caso de una Emergencia\n", end="")
        while push_button.value() == 1:
            sleep(0.1)
    else:
        led.value(0)
    sleep(0.1)  # Agregar un pequeño retardo para evitar alta carga en el bucle
