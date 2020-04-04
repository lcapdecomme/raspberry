 #!/usr/bin/env python
# NAME: teleinfoERDF.py
# AUTHOR: Lionel Capdecomme
# DATE  : 24/01/2016
# COMMENT: Lecture des trames Teleinformation 
import serial, sys
# 1. Ouverture du port serie
SERIAL = '/dev/ttyAMA0'
try:
  ser = serial.Serial(
    port=SERIAL,
    baudrate = 1200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.SEVENBITS,
    timeout=1)
except:
  print "Impossible d'ouvrir le port serie" + SERIAL
  print sys.exc_info()
  sys.exit(1)

# 2. Lecture d'une trame complete
compteur=0 
while compteur<=1 :
 line=ser.readline().strip()
 array = line.split(' ')
 if len(array)>1 :
  header, value = array[0], array[1]
  print header + ":" + value
  if header == "ADCO" : compteur=compteur+1 
