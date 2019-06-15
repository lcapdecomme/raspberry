#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NAME: teleinfoERDF.py
# AUTHOR: Lionel Capdecomme
# DATE  : 24/01/2016
# COMMENT: Lecture des trames Teleinformation et sauvegarde dans BD MongoLab

import serial, json, sys, pymongo, datetime, time
from pymongo import MongoClient
from datetime import datetime, timedelta


# 0. Init variable 
SERIAL = '/dev/ttyAMA0'
MONGODB_URI = 'mongodb://vidocq:leteckel@ds037415.mongolab.com:37415/edf' 
MONGODB_COLLECTION='edf'
MONGODB_COLLECTION_BILAN='edf_bilan'

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

#Decalage horaire
decalage=1

dateDuJour=datetime.now()+timedelta(hours=decalage)
data['date']=dateDuJour

#3. Sauvegarde dans le compte mongolab
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_default_database()
# Choix de la collection 
teleinfo = db[MONGODB_COLLECTION]
teleinfo.insert(data)


def consommation(d):
    hp = int(d['heuresPleines'])
    hc = int(d['heuresCreuses'])
    return hp + hc


def days_diff(a,b):
    A = a.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    B = b.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    return (A - B).days


def isVeille(a,b):
    A = a.replace(minute = 0, second = 0, microsecond = 0)
    B = b.replace(minute = 0, second = 0, microsecond = 0)
    diff=(A-B).total_seconds()
    if diff == 86400:
       return True
    else:
       return False


def isAvantVeille(a,b):
    A = a.replace(minute = 0, second = 0, microsecond = 0)
    B = b.replace(minute = 0, second = 0, microsecond = 0)
    diff=(A-B).total_seconds()
    if diff == (86400*2):
       return True
    else:
       return False


def days_diff_an(a,b):
    A = a.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    B = b.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    if A.month > B.month:
       return A.month - B.month
    else:
       return B.month - A.month


def initStat():
    #Jour : Valeur min et max sur 24 heures
    for num in range(0,24): 
	data["heure" + str(num)]=""
 
    #Semaine & mois : valeur min et max sur 30 derniers jours
    for num in range(1,31): 
	data["jour" + str(num)]=""

    #Annee : valeur min et max sur 12 derniers mois
    for num in range(1,13): 
	data["mois" + str(num)]=""


def completeStatSav():
    #Semaine & mois : valeur min et max sur 30 derniers jours
    total=0
    nbElements=0
    for num in range(1,31): 
        # On cherche deux jours consécutifs qui ont des valeurs
	if num>2:
	   if data["jour" + str(num)] <> "" and data["jour" + str(num-1)] <> "":
              # On additonne les écrats entre deux jours
              total=total+ data["jour" + str(num)] - data["jour" + str(num-1)]
              nbElements=nbElements+1

    moyennePeriode=total/nbElements
    print "Moyenne période ", moyennePeriode

    for num in range(1,31): 
	if data["jour" + str(num)] == "":
	   data["jour" + str(num)]= data["jour" + str(num-1)] + moyennePeriode;
        print "Jour ", num, ":", data["jour" + str(num)]


def completeStat():
    #Semaine & mois : valeur min et max sur 30 derniers jours
    total=0
    nbElements=0
    depart=0
    valDepart=0
    valFin=0

    for num in range(1,31): 
        print "Jour ", num, ":", data["jour" + str(num)]

    for num in range(1,31): 
        # On cherche des jours qui n'ont pas de valeurs
        if num>1 and data["jour" + str(num)] == "" and depart==0:
           depart=num

        if data["jour" + str(num)] <> "" and depart<>0:
           total=0
           nbElements=0
           print "bouche les trous du jour ", depart, " au jour ", num - 1
           valDepart= data["jour" + str(depart-1)]
           valFin= data["jour" + str(num)]
           total=valFin-valDepart
           nbElements=num-depart+1
           moyennePeriode=total/nbElements
           print "Ajoute en moyenne ", moyennePeriode, " - elements : ", nbElements

           for num2 in range(depart,num): 
  	       data["jour" + str(num2)]= data["jour" + str(num2-1)] + moyennePeriode;

           depart=0
           valDepart=0
           valFin=0

    for num in range(1,31): 
        print "Jour ", num, ":", data["jour" + str(num)]



def testSuperieur(s, t):
    if s == "":
       return True
    if float(s) > t:
       return True
    return False


def testInferieur(s, t):
    if s == "":
       return True
    if float(s) < t:
       return True
    return False

    


#4. Construction du bilan
stat = []
cursor = teleinfo.find()
heure = datetime.strftime(dateDuJour, "%H")
jour = datetime.strftime(dateDuJour, "%d")
mois = datetime.strftime(dateDuJour, "%m")
annee = datetime.strftime(dateDuJour, "%Y")
start_date_mois = dateDuJour + timedelta(-30)
start_date_an = dateDuJour + timedelta(-360)
print "h:",heure," j:", jour, " m:", mois, " année:", annee, " => Passé:", start_date_mois, " ==> Passé an:", start_date_an
dateHier=dateDuJour + timedelta(-1)
hcHier=0
hpHier=0

initStat()

for document in cursor:
    #print(document['_id'])
    date=document['date']
    dateTraitement= datetime.strftime(date, "%d-%m-%Y")
    heureTraitement = datetime.strftime(date, "%H:%M")
    if isVeille(dateDuJour, date):
       data['heuresCreusesHier']=document['heuresCreuses']
       data['heuresPleinesHier']=document['heuresPleines']
    if isAvantVeille(dateDuJour, date):
       data['heuresCreusesAvantHier']=document['heuresCreuses']
       data['heuresPleinesAvantHier']=document['heuresPleines']
        
    # 1. Statistique aujourd'hui
    minuteTrait = int(datetime.strftime(date, "%M"))
    heureTrait = str(int(datetime.strftime(date, "%H")))
    jourTrait = datetime.strftime(date, "%d")
    moisTrait = datetime.strftime(date, "%m")
    anneeTrait = datetime.strftime(date, "%Y")
    if jourTrait == jour and moisTrait == mois and anneeTrait == annee and minuteTrait == 0:
       data['heure'+str(heureTrait)] = consommation(document)
       #print "Heure ",str(heureTrait), ":", consommation(document)

    # 2. Statistique 30 jours précédent               
    if start_date_mois <= date :
       #Retourne l'index dans le tableau de 30 elements en fonction de la date du jour
       #Ex. on est le 6. Si jourTrait=6, cela retourne 30 (30+6-6),
       #si jourTrait=3, cela retourne 27 (30-6+3),
       #si jourTrtait=15, cela retourne 9 (30-6-15)
       jourTableau=30-days_diff(dateDuJour, date)
       #Si minuit, on sauve la consommation ?
       if int(heureTrait) == 0 and int(minuteTrait) == 0:
          data['jour'+str(jourTableau)]= consommation(document)
          # print "Jour ",str(jourTableau), ":", consommation(document)

    # 3. Statistique 360 jours précédent dans un tableau de 12 valeurs (2/mois)              
    if start_date_an <= date :
       #Retourne l'index dans le tableau de 12 elements en fonction de la date du jour
       #Ex. on est en fevrier. cela retourne 12,
       #si moisTrait=3, cela retourne 1 (12-(3-2)),
       #si jourTrtait=9, cela retourne 7 (12-(7-2))
       jourTableau=12-days_diff_an(dateDuJour, date)
       #Si minuit le jour 1, on sauve la consommation
       if int(heureTrait) == 0 and int(jourTrait)==1 and minuteTrait == 0:
          data['mois'+str(jourTableau)]= consommation(document)
          #print "Mois ",str(jourTableau), ":", consommation(document)

    # 4. Recherche des consommations max.             
    if int(heureTrait) == 0  and int(minuteTrait) == 0  :
       try:
          hc=int(document['heuresCreuses'])
          hp=int(document['heuresPleines'])
       except ValueError:
          print date, "Erreur  : hc:", hc, " : hp:", hp
       if hcHier != 0  and hpHier != 0 and isVeille(date,dateHier):
          diffHc = hc-hcHier
          diffHp = hp-hpHier
          # print date, "-", dateHier,":hc auj:", hc, ", hc hier:", hcHier,"-hp auj:", hp,", hp hier:", hpHier
          if hc<>hcHier and  hp<>hpHier and hc>1000 and hp>1000 and hpHier>1000 and hcHier>1000: 
             #if diffHc+diffHp>500000: 
             #   print "+500000:",date, "-", dateHier,":hc auj:", hc, ", hc hier:", hcHier,"-hp auj:", hp,", hp hier:", hpHier, "Diff:",diffHc+diffHp
             #if diffHc+diffHp<100: 
             #   print "_100:", date, "-", dateHier,":hc auj:", hc, ", hc hier:", hcHier,"-hp auj:", hp,", hp hier:", hpHier
             # print date, " : hc:", diffHc, " : hp:", diffHp
             stat.append([diffHc+diffHp, date, diffHc, diffHp])
       
       dateHier=date
       hcHier=hc
       hpHier=hp



liste = sorted(stat, key=lambda x: x[0], reverse=True)
i=0
for max in liste :
    data['statMaxTotal'+str(i)]=max[0]
    data['statMaxDate'+str(i)]=max[1]
    data['statMaxhc'+str(i)]=max[2]
    data['statMaxhp'+str(i)]=max[3]
    print max[0]
    i+=1
    if i==5 : 
       break


liste = sorted(stat, key=lambda x: x[0])
i=0
for min in liste :
    data['statMinTotal'+str(i)]=min[0]
    data['statMinDate'+str(i)]=min[1]
    data['statMinhc'+str(i)]=min[2]
    data['statMinhp'+str(i)]=min[3]
    print min[0]
    i+=1
    if i==5 : 
       break

# Bouche les eventuels trous dans les tableaux
completeStat()


#5.bis Sauvegarde dans le compte mongolab du nouveau bilan
edf_bilan = db[MONGODB_COLLECTION_BILAN]
#Suppression de tous les documents
edf_bilan.remove({});
#Ajout d'un document par sonde dans l'ordre de declaration initiale
edf_bilan.insert(data)


