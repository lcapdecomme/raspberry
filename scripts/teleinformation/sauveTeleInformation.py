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
MONGODB_URI = 'mongodb://credential@url:port/base'
MONGODB_COLLECTION='edf'
MONGODB_COLLECTION_BILAN='edf_bilan'
MONGODB_COLLECTION_MENSUEL='edf_bilan_mensuel'
MONGODB_COLLECTION_ANNUEL='edf_bilan_annuel'
MONGODB_COLLECTION_ANNUEL_JUILLET='edf_bilan_annuel_juillet'

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
    try:
       hc=int(d['heuresCreuses'])
       hp=int(d['heuresPleines'])
    except ValueError:
       hc=0
       hp=0
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


def completeStat():
    #Semaine & mois : valeur min et max sur 30 derniers jours
    total=0
    nbElements=0
    depart=0
    valDepart=0
    valFin=0

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


def completeStatMensuel():
    depart=0
    index=0
    obj_mensuel_prec=0
    print "Bouche les trous dans les mois"
    # Premier passage pour boucher les trous
    for obj_mensuel in list_data_mensuel:
        if obj_mensuel_prec <> 0:
           # Si trou ? on les bouche
           if (int(obj_mensuel_prec["numMois"])+1) <> int(obj_mensuel["numMois"]):
              nbElements=int(obj_mensuel["numMois"])-int(obj_mensuel_prec["numMois"])
              total=int(obj_mensuel["value"])-int(obj_mensuel_prec["value"])
              moyennePeriode=total/nbElements
              for num2 in range(1,nbElements):
                  data_mensuel = {}
                  anneeTrait=int(obj_mensuel_prec["an"])
                  moisTrait=int(obj_mensuel_prec["mo"])+num2
                  if (moisTrait>12):
                      moisTrait=moisTrait-12;
                      anneeTrait=anneeTrait+1;
                  data_mensuel['an']= str(anneeTrait)
                  data_mensuel['mo']= str(moisTrait)
                  data_mensuel['numMois']= (int(obj_mensuel_prec["numMois"]+num2))
                  data_mensuel['value']= str((moyennePeriode*num2)+int(obj_mensuel_prec["value"]))
                  list_data_mensuel2.append(data_mensuel)
                  # print index,":Ajout de   ", data_mensuel

        list_data_mensuel2.append(obj_mensuel)
        # print index,":Analyse de :", obj_mensuel
        obj_mensuel_prec = obj_mensuel
        index=index+1

    obj_mensuel_prec=0
    # Deuxieme passage pour boucher les trous
    for obj_mensuel in list_data_mensuel2:
        if obj_mensuel_prec <> 0:
           difference=int(obj_mensuel["value"])-int(obj_mensuel_prec["value"])
           obj_mensuel['diff']= int(difference)/1000
        else:
           obj_mensuel['diff']= 0

        print "Mensuel :", obj_mensuel
        obj_mensuel_prec = obj_mensuel


def completeStatAnnuel():
    obj_annuel_prec=0
    # Passage pour calculer les diffÃ©rences des stats annuel
    for obj_annuel in list_data_annuel:
        if obj_annuel_prec <> 0:
           difference=int(obj_annuel["value"])-int(obj_annuel_prec["value"])
           obj_annuel['diff']= int(difference)/1000
        else:
           obj_annuel['diff']= 0

        print "Annuel :", obj_annuel
        obj_annuel_prec = obj_annuel
        list_data_annuel2.append(obj_annuel)


    obj_annuel_juillet_prec=0
    # Passage pour calculer les diffÃ©rences des stats annuel au mois de juillet
    for obj_annuel_juillet in list_data_annuel_juillet:
        if obj_annuel_juillet_prec <> 0:
           difference=int(obj_annuel_juillet["value"])-int(obj_annuel_juillet_prec["value"])
           obj_annuel_juillet['diff']= int(difference)/1000
        else:
           obj_annuel_juillet['diff']= 0

        print "Annuel :", obj_annuel_juillet
        obj_annuel_juillet_prec = obj_annuel_juillet
        list_data_annuel_juillet2.append(obj_annuel_juillet)



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
print "h:",heure," j:", jour, " m:", mois, " annÃ©e:", annee, " => PassÃ©:", start_date_mois, " ==> PassÃ© an:", start_date_an
dateHier=dateDuJour + timedelta(-1)
hcHier=0
hpHier=0

list_data_mensuel=[]
list_data_mensuel2=[]

list_data_annuel=[]
list_data_annuel2=[]

list_data_annuel_juillet=[]
list_data_annuel_juillet2=[]

initStat()

firstRecord=True

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

    # 2. Statistique 30 jours prÃ©cÃ©dent
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

    # 3. Statistique 360 jours prÃ©cÃ©dent dans un tableau de 12 valeurs (2/mois)
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
          # On Ã©limine les erreurs de captation
          if hc<>hcHier and  hp<>hpHier and hc>1000 and hp>1000 and hpHier>1000 and hcHier>1000:
             stat.append([diffHc+diffHp, date, diffHc, diffHp])

       dateHier=date
       hcHier=hc
       hpHier=hp


    # 5. Recherche des consommations en dÃ©but de chaque mois
    if int(jourTrait) == 1 and int(heureTrait) == 0 and int(minuteTrait) == 0:
       data_mensuel = {}
       data_mensuel['an']= str(int(anneeTrait))
       data_mensuel['mo']= str(int(moisTrait))
       data_mensuel['numMois']= (int(anneeTrait)*12)+int(moisTrait)
       data_mensuel['value']= consommation(document)
       list_data_mensuel.append(data_mensuel)
       #print "Stat Mensuel trouve", str(anneeTrait)+str(moisTrait),":", document['heuresCreuses'],"-", document['heuresPleines']
       #print data_mensuel
       #print moisTrait,"/",anneeTrait,"===>","HC/HP", int(document['heuresCreuses']), "-",int(document['heuresPleines'])


    # 6. Recherche des consommations en debut de chaque annee
    if firstRecord or (int(moisTrait) == 1 and int(jourTrait) == 1 and int(heureTrait) == 0):
       data_annuel = {}
       data_annuel['an']= str(int(anneeTrait))
       data_annuel['value']= consommation(document)
       list_data_annuel.append(data_annuel)
       #print "Stat Annuel trouve", str(anneeTrait),":", document['heuresCreuses'],"-", document['heuresPleines']


    # 6. Recherche des consommations en debut de chaque mois de juillet
    # Vu que le premier enregistrement de la BD est en mars, on prendra comme premier enreg celui de juillet 2019
    if int(moisTrait) == 7 and int(jourTrait) == 1 and int(heureTrait) == 0:
       data_annuel_juillet = {}
       data_annuel_juillet['an']= str(int(anneeTrait))
       data_annuel_juillet['value']= consommation(document)
       list_data_annuel_juillet.append(data_annuel_juillet)
       #print "Stat Annuel trouve", str(anneeTrait),":", document['heuresCreuses'],"-", document['heuresPleines']

    firstRecord=False



# 6.bis On ajoute enfin la derniere valeur de l'annee en cours
data_annuel = {}
data_annuel['an']= str(int(anneeTrait)+1)
data_annuel['value']= consommation(document)
list_data_annuel.append(data_annuel)
# 6.ter On ajoute enfin la derniere valeur de l'annee en cours pour la collection de juillet
data_annuel = {}
data_annuel['an']= str(int(anneeTrait)+1)
data_annuel['value']= consommation(document)
list_data_annuel_juillet.append(data_annuel)
# print "Stat Annuel trouve", str(anneeTrait),":", document['heuresCreuses'],"-", document['heuresPleines']


# Recherche des consommations max.
liste = sorted(stat, key=lambda x: x[0], reverse=True)
i=0
for max in liste :
    data['statMaxTotal'+str(i)]=max[0]
    data['statMaxDate'+str(i)]=max[1]
    data['statMaxhc'+str(i)]=max[2]
    data['statMaxhp'+str(i)]=max[3]
    print "Max ", str(i), " donne ", max[0]
    i+=1
    if i==8 :
       break


# Recherche des consommations min.
liste = sorted(stat, key=lambda x: x[0])
i=0
for min in liste :
    data['statMinTotal'+str(i)]=min[0]
    data['statMinDate'+str(i)]=min[1]
    data['statMinhc'+str(i)]=min[2]
    data['statMinhp'+str(i)]=min[3]
    print "Min ", str(i), " donne ", min[0]
    i+=1
    if i==8 :
       break


# Bouche les eventuels trous dans les tableaux
completeStat()
completeStatMensuel()
completeStatAnnuel()


#5.bis Sauvegarde dans le compte mongolab du nouveau bilan
edf_bilan = db[MONGODB_COLLECTION_BILAN]
#Suppression de tous les documents
edf_bilan.remove({});
#Ajout d'un document par sonde dans l'ordre de declaration initiale
edf_bilan.insert(data)

#5.ter Sauvegarde dans le compte mongolab du nouveau bilan mensuel
edf_bilan_mensuel = db[MONGODB_COLLECTION_MENSUEL]
#Suppression de tous les documents
edf_bilan_mensuel.remove({});
for obj_mensuel in list_data_mensuel2:
    edf_bilan_mensuel.insert(obj_mensuel)

#5.qua Sauvegarde dans le compte mongolab du nouveau bilan annuel
edf_bilan_annuel = db[MONGODB_COLLECTION_ANNUEL]
#Suppression de tous les documents
edf_bilan_annuel.remove({});
for obj_annuel in list_data_annuel2:
    print obj_annuel
    edf_bilan_annuel.insert(obj_annuel)

#5.cinq Sauvegarde dans le compte mongolab du nouveau bilan annuel au mois de juillet
edf_bilan_annuel_juillet = db[MONGODB_COLLECTION_ANNUEL_JUILLET]
#Suppression de tous les documents
edf_bilan_annuel_juillet.remove({});
for obj_annuel_juillet in list_data_annuel_juillet2:
    print obj_annuel_juillet
    edf_bilan_annuel_juillet.insert(obj_annuel_juillet)


