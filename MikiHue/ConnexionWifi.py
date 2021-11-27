#Auteur : Michael GOMES
# Complete project details at https://RandomNerdTutorials.com

try:
  import usocket as socket
except:
  import socket

from machine import Pin
from network import WLAN
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'inserer_votre_ssid_ici'
password = 'inserer_le_mot_de_passe_de_votre_wifi_ici'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)

#Source : code boot.py vu en cours