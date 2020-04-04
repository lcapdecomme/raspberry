#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NAME: teleinfoERDF.py
# AUTHOR: Lionel Capdecomme
# DATE  : 24/01/2016
# COMMENT: Lecture des trames Teleinformation et sauvegarde dans BD MongoLab

import serial, json, sys, pymongo, datetime, time
from pymongo import MongoClient
from datetime import datetime, timedelta

# 0. Initialisation variable Mongo
MONGODB_URI = 'mongodb://user:password@serveur:port/basededonnee' 
MONGODB_COLLECTION='collection'
MONGODB_COLLECTION_BILAN='collection_bilan'
MONGODB_COLLECTION_STAT='collection_stat

#Decalage horaire
decalage=2
nbSondes=3

# Initialisation temperature 
base_dir = '/sys/bus/w1/devices/'
nbSondes=3
nbProps=3 # 1:lieu, 2: nom du fichier, 3:valeur, 4:ordre de tri
sondes=[[0 for row in range(0,nbProps)] for col in range(0,nbSondes)]
sondes[0][0]="salon"
sondes[0][1]="28-031574449aff"
sondes[1][0]="exterieur"
sondes[1][1]="28-0315747700ff"
sondes[2][0]="garage"
sondes[2][1]="28-03157474cdff"

# Fonction ouverture et lecture d'un fichier
def lireFichier(fichier):
    f = open(fichier, 'r')
    lignes = f.readlines()
    f.close()
    return lignes

data = {}
# Lecture des temperatures
for i in range(nbSondes):
    sonde = base_dir + sondes[i][1] + "/w1_slave"
    lignes = lireFichier(sonde)
    while lignes[0].strip()[-3:] != 'YES': # lit les 3 derniers char de la ligne 0 et recommence si pas YES
        sleep(0.2)
        lignes = lireFichier(sonde)

    # Fichier ok, lecture seconde ligne 
    temp_raw = int (lignes[1].split("=")[1])
    value = round(temp_raw / 1000.0, 2)
    sondes[i][2] += value # le 2 arrondi a 2 chiffres apres la virgule
    print sondes[i][0],"=",sondes[i][2] 

# Le tableau sauvegarde en BD
data['sondes']=sondes
data['date']=datetime.now()+timedelta(hours=decalage)

#3. Sauvegarde dans le compte mongolab de cet enrgistrement
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_default_database()
# Choix de la collection 
temperatures = db[MONGODB_COLLECTION]
temperatures.insert(data)



def days_diff(a,b):
    A = a.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    B = b.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    return (A - B).days


def days_diff_an(a,b):
    A = a.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    B = b.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    if A.month > B.month:
       return A.month - B.month
    else:
       return B.month - A.month


def initStat():
    tableauStat = {}
    #Jour : Valeur min et max sur 24 heures
    for num in range(0,24): 
	tableauStat["heure" + str(num)]=""
 
    #Semaine & mois : valeur min et max sur 30 derniers jours
    for num in range(1,31): 
	tableauStat["minJour" + str(num)]=""
	tableauStat["maxJour" + str(num)]=""

    #Annee : valeur min et max sur 12 derniers mois
    for num in range(1,13): 
	tableauStat["minMois" + str(num)]=""
	tableauStat["maxMois" + str(num)]=""

    return tableauStat


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
stat = {}
bilan = {}
cursor = temperatures.find()
dateDuJour=datetime.now()+timedelta(hours=decalage)
heure = datetime.strftime(dateDuJour, "%H")
jour = datetime.strftime(dateDuJour, "%d")
mois = datetime.strftime(dateDuJour, "%m")
annee = datetime.strftime(dateDuJour, "%Y")
start_date_mois = dateDuJour + timedelta(-29)
start_date_an = dateDuJour + timedelta(-360)
#print "h:",heure," j:", jour, " m:", mois, " année:", annee, " => Passé:", start_date_mois, " ==> Passé an:", start_date_an
for document in cursor:
    #print(document['_id'])
    #print(document['sondes'])
    sonde=document['sondes']
    date=document['date']
    dateTraitement= datetime.strftime(date, "%d-%m-%Y")
    heureTraitement = datetime.strftime(date, "%H:%M")
    for s in sonde:
        libelle = s[0]
        temp = float(s[2])

	#1. Calcul du bilan 
        if libelle in bilan :
	   temperatureSonde = bilan[libelle]
           temperatureSonde['libelle']=libelle
           temperatureSonde['courant']=temp
           temperatureSonde['dateTraitement']=dateDuJour
	   if float(temperatureSonde['mini']) > temp:
	       temperatureSonde['mini'] = temp
	       temperatureSonde['miniDate'] = dateTraitement
	       temperatureSonde['miniHeure'] = heureTraitement
	   if float(temperatureSonde['maxi']) < temp:
	       temperatureSonde['maxi'] = temp
	       temperatureSonde['maxiDate'] = dateTraitement
	       temperatureSonde['maxiHeure'] = heureTraitement

        else:
           #Cette sonde n'existe pas dans le tableau bilan 
	   temperatureSonde = {}
           temperatureSonde['libelle']=libelle
           temperatureSonde['courant']=temp
           temperatureSonde['mini']=temp
           temperatureSonde['maxi']=temp
	   temperatureSonde['maxiDate'] = dateTraitement
	   temperatureSonde['maxiHeure'] = heureTraitement
	   temperatureSonde['miniDate'] = dateTraitement
	   temperatureSonde['miniHeure'] = heureTraitement
           temperatureSonde['dateTraitement']=dateDuJour

	#Ajout de cette sone au tableau bilan
 	bilan[libelle]=temperatureSonde


	
        #2. Calcul des statistiques 
        if libelle in stat :
	   statSonde = stat[libelle]
        else:
           #Cette sonde n'existe pas encore dans le tableau stat
	   statSonde =initStat()

        statSonde['libelle']=libelle
        statSonde['dateTraitement']=dateDuJour
        # 1. Statistique aujourd'hui
        heureTrait = str(int(datetime.strftime(date, "%H")))
        jourTrait = datetime.strftime(date, "%d")
        moisTrait = datetime.strftime(date, "%m")
        anneeTrait = datetime.strftime(date, "%Y")
        if jourTrait == jour and moisTrait == mois and anneeTrait == annee:
	   statSonde['heure'+str(heureTrait)] = temp

        # 2. Statistique 30 jours précédent               
        if start_date_mois <= date :
           #Retourne l'index dans le tableau de 30 elements en fonction de la date du jour
           #Ex. on est le 6. Si jourTrait=6, cela retourne 30 (30+6-6),
           #si jourTrait=3, cela retourne 27 (30-6+3),
           #si jourTrtait=15, cela retourne 9 (30-6-15)
           jourTableau=30-days_diff(dateDuJour, date)
           #print dateDuJour,",",date,",",jourTableau
           #La temperature min. pour cette sonde est-elle supérieur à la température lue en BD ?
           if testSuperieur(statSonde['minJour'+str(jourTableau)], temp):
              statSonde['minJour'+str(jourTableau)]= temp
           #La temperature max. pour cette sonde est-elle supérieur à la température lue en BD ?
           if testInferieur(statSonde['maxJour'+str(jourTableau)], temp):
              statSonde['maxJour'+str(jourTableau)]= temp
           #if libelle=="salon" and jourTableau==30:
           #    print "ap.",jourTableau, ":", temp,":",statSonde['minJour'+str(jourTableau)]
                 
        # 3. Statistique 360 jours précédent dans un tableau de 12 valeurs (2/mois)              
        if start_date_an <= date :
           #Retourne l'index dans le tableau de 12 elements en fonction de la date du jour
           #Ex. on est en fevrier. cela retourne 12,
           #si moisTrait=3, cela retourne 1 (12-(3-2)),
           #si jourTrtait=9, cela retourne 7 (12-(7-2))
           jourTableau=12-days_diff_an(dateDuJour, date)
           #La temperature min. pour cette sonde est-elle supérieur à la température lue en BD ?
           if testSuperieur(statSonde['minMois'+str(jourTableau)], temp):
              statSonde['minMois'+str(jourTableau)]= temp
           #La temperature max. pour cette sonde est-elle supérieur à la température lue en BD ?
           if testInferieur(statSonde['maxMois'+str(jourTableau)], temp):
              statSonde['maxMois'+str(jourTableau)]= temp
                 
	#Ajout de cette sone au tableau bilan
 	stat[libelle]=statSonde

	

#5. Sauvegarde dans le compte mongolab des nouvelles statistiques
temperature_stat = db[MONGODB_COLLECTION_STAT]
#Suppression de tous les documents
temperature_stat.remove({});
#Ajout d'un document par sonde dans l'ordre de declaration initiale
for i in range(nbSondes):
	for key, value in stat.iteritems():
		if sonde[i][0] in key:
			temperature_stat.insert(value)



#5.bis Sauvegarde dans le compte mongolab du nouveau bilan
temperature_bilan = db[MONGODB_COLLECTION_BILAN]
#Suppression de tous les documents
temperature_bilan.remove({});
#Ajout d'un document par sonde dans l'ordre de declaration initiale
for i in range(nbSondes):
	for key, value in bilan.iteritems():
		if sonde[i][0] in key:
			temperature_bilan.insert(value)



