import network
import urequests
import time
from machine import I2C, Pin 
from i2c_lcd import I2cLcd 
from time import sleep, sleep_ms, ticks_ms 

led = Pin(2, Pin.OUT)

push_button = Pin(13, Pin.IN)

AddressOfLcd = 0x27
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 

lcd = I2cLcd(i2c, AddressOfLcd, 2, 16)


#Conectando a WiFi
print ("Conectando a la Red", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print("*", end="")
  time.sleep(0.50)
print("\nConectando exitosamente !\n")

latitude = 40.712776
longitude = -74.005974

print("Listo! Presione el botón en caso de una Emergencia\n", end="")
lcd.move_to(1,0)
lcd.putstr('Ready! CITYSOS')
lcd.move_to(2,1)
lcd.putstr("Alert Police")
while True:
  logic_state = push_button.value()
  if logic_state :
      led.value(1)
      #Envio del requerimiento por HTTPS
      print("Enviando alerta...\n", end="")
      lcd.clear()
      lcd.move_to(3,0)
      lcd.putstr('Sending...')
      data = {'message': "Se solicita Ayuda policial",'latitude': latitude, 'longitude': longitude}
      response = urequests.post("https://reqres.in/api/users", json=data)
      print(response.text)
      print("Alerta enviada!\n")
      print("Bloqueado por 5 segundos\n", end="")
      lcd.clear()
      lcd.move_to(1,0)
      lcd.putstr('Alert sended!')
      lcd.move_to(1,1)
      lcd.putstr('Blocked 5 sec')
      sleep(5)
      led.value(0)
      
      lcd.clear()
      lcd.move_to(1,0)
      lcd.putstr('Ready! CITYSOS')
      lcd.move_to(2,1)
      lcd.putstr("Alert Police")
      print("Listo! Presione el botón en caso de una Emergencia\n", end="")
      while push_button.value():
        sleep(0.1) 
  else:
      led.value(0)


  

