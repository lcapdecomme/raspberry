 #!/usr/bin/env python
# NAME: sauveTeleInformation.py
# AUTHOR: Lionel Capdecomme
# DATE  : 24/01/2016
# COMMENT: Lecture des trames Teleinformation et sauvegarde dans BD MongoLab

import serial, json, sys, pymongo, datetime
from pymongo import MongoClient

# 0. Init variable 
SERIAL = '/dev/ttyAMA0'
MONGODB_URI = 'mongodb://user:password@serveur:port/basededonnee' 
MONGODB_COLLECTION='collection'

# 1. Ouverture du port serie
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
data = {}
while True :
 line=ser.readline().strip()
 array = line.split(' ')
 if len(array)>1 :
  header, value = array[0], array[1]
  # Si ADCO 2 fois alors tour complet
  if header == "ADCO" : 
    if 'adresseConcentrateur' in data : break 
    data['adresseConcentrateur']=value
  elif header == "OPTARIF" : data['optionTarif']=value
  elif header == "PTEC" : data['periodeTarifaire']=value
  elif header == "IINST" : data['intensiteInstant']=value
  elif header == "ADPS" : data['avertissementDepassement']=value
  elif header == "PAPP" : data['puissanceApparente']=value
  elif header == "IMAX" : data['intensiteMaximum']=value
  elif header == "ISOUSC" : data['intensiteSouscrit']=value
  elif header == "HCHC" : data['heuresCreuses']=value
  elif header == "HCHP" : data['heuresPleines']=value

data['date']=datetime.datetime.now()

#3. Sauvegarde dans le compte mongolab
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_default_database()
# Choix de la collection 
teleinfo = db[MONGODB_COLLECTION]
teleinfo.insert(data)

