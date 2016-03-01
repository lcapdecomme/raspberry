#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NAME: listeTemperature.py
# AUTHOR: Lionel Capdecomme
# DATE  : 04/02/2016
# COMMENT: Lecture des releves depuis la BD MongoLab et affiche les valeurs mini/maxi/courante d'une sonde en particulier

import serial, json, sys, pymongo, datetime, time
from pymongo import MongoClient
from datetime import datetime

# 0. Initialisation variable Mongo
# Ces trois propriétés sont à personnaliser !!!!
MONGODB_URI = 'mongodb://user:password@serveur:port/basededonnee' 
MONGODB_COLLECTION='collection'

#3. Sauvegarde dans le compte mongolab
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_default_database()
# Choix de la collection 
temperatures = db[MONGODB_COLLECTION]

#4. Construction du bilan
bilan = {}
cursor = temperatures.find()
for document in cursor:
    #print(document['_id'])
    #print(document['sondes'])
    sonde=document['sondes']
    date=document['date']
    dateTraitement= datetime.strftime(date, "%d-%m-%Y")
    heureTraitement = datetime.strftime(date, "%H:%M:%S")
    for s in sonde:
        libelle = s[0]
        temp = float(s[2])
 
        if libelle in bilan :
	   temperatureSonde = bilan[libelle]
           temperatureSonde['courant']=temp
	   if float(temperatureSonde['mini']) > temp:
	       temperatureSonde['mini'] = temp
	       temperatureSonde['miniDate'] = dateTraitement
	       temperatureSonde['miniHeure'] = heureTraitement
	   if float(temperatureSonde['maxi']) < temp:
	       temperatureSonde['maxi'] = temp
	       temperatureSonde['maxiDate'] = dateTraitement
	       temperatureSonde['maxiHeure'] = heureTraitement

        else:
           #Cette sonde n'existe pas dans le tableau 
	   temperatureSonde = {}
           temperatureSonde['courant']=temp
           temperatureSonde['mini']=temp
           temperatureSonde['maxi']=temp
	   temperatureSonde['maxiDate'] = date
	   temperatureSonde['maxiDate'] = date

	#Ajout de cette sone au tableau
 	bilan[libelle]=temperatureSonde

maintenant=time.strftime('%d/%m/%Y')
print maintenant
maintenant=time.strftime('%H:%M:%S')
print maintenant

libelle='salon'
print '==============='
temperatureSonde = bilan[libelle]
print "Il fait : ", temperatureSonde['courant']
print temperatureSonde['mini'], " le ",  temperatureSonde['miniDate']
print temperatureSonde['maxi'], " le ",  temperatureSonde['maxiDate']
print '==============='
print bilan

