#Auteur : Michael GOMES
# Complete project details at https://RandomNerdTutorials.com
import socket
from machine import Pin
import machine
import time
import onewire
import ds18x20
import websocket
from machine import Pin


# Configuration des pins
lightSensor = Pin(4,Pin.IN)
ow = onewire.OneWire(Pin(5))
ds = ds18x20.DS18X20(ow)
led=Pin(2,Pin.OUT)
ds=ds18x20.DS18X20(ow)
temp = 0

# ESP32 GPIO 26
relay = Pin(26, Pin.OUT)

#Generation du code html
def web_page(temp, light):
  #Recuperation du l'état de la led  
  if led.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"

  #Recuperation de l'etat du relais  
  if relay.value() == (1):
    relay_state = "ON"
  else:
    relay_state = "OFF"  
  html = """<html><head> <title>Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #FF0000; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #000000;}</style></head>
  <body> <h1>Michael Gomes Web Server</h1>
  
   <div style="width: 100%; overflow: hidden;">
     <p>Lumiere : <strong>""" + relay_state + """</strong></p>
      <p><a href="/?alim=on"><button class="button">ON</button></a></p>   
      <p><a href="/?alim=off"><button class="button button2">OFF</button></a></p>
    </br>
    </br>
    </br>    
    Lumiere detectee : <strong>"""+light+"""</strong></br>
    Temperature : <strong>"""+temp+"""</strong>°C
    <p><a href="/"><button class="button button">Actualiser</button></a></p>  
 </div>
 
  </body>
  </html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


while True:
  print("run")    
  conn, addr = s.accept()
  roms=ds.scan()
  ds.convert_temp()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  #print('Content = %s' % request)
  #Recuperation en get de la valeur de la led
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  
  #Recuperation en get de la valeur du relais
  alim_on = request.find('/?alim=on')
  alim_off = request.find('/?alim=off')
  
  lightOn = lightSensor.value()
  
  #Gestion du capteur de la lumière
  if(lightOn == 1):
        print("lumière captée")
        light = "oui"
  else:
        print("lumière pas captée")
        light = "non"
  
  #Gestion de l'alimentation
  if alim_on == 6:
    print('Alim ON')
    relay.value(1)
  if alim_off == 6:
    print('Alim OFF')
    relay.value(0)
  
  #Gestion de la led
  if(light == 'non'):
      led.value(1)
  else:
      led.value(0)
  
  for rom in roms: 
      temp = ds.read_temp(rom)
         
  response = web_page(str(temp), light)
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()
  
  
 #Sources : https://randomnerdtutorials.com/micropython-relay-module-esp32-esp8266/ 