 #!/usr/bin/env python
# NAME: sauveTemperature.py
# AUTHOR: Lionel Capdecomme
# DATE  : 24/01/2016
# COMMENT: Lecture des valeurs des sondes de températures et sauvegarde dans BD MongoLab

import serial, json, sys, pymongo, datetime, time
from pymongo import MongoClient
from datetime import datetime

# 0. Initialisation variable Mongo
# Ces trois propriétés sont à personnaliser !!!!
MONGODB_URI = 'mongodb://user:password@serveur:port/basededonnee' 
MONGODB_COLLECTION='collection'
MONGODB_COLLECTION_BILAN='collection_bilan'

# Initialisation temperature 
# Ces propriétés sont à personnaliser !!!!
base_dir = '/sys/bus/w1/devices/'
nbSondes=3
nbProps=3 # 1:lieu, 2: nom du fichier, 3:valeur
sondes=[[0 for row in range(0,nbProps)] for col in range(0,nbSondes)]
#Nom et id de la sonde 1
sondes[0][0]="salon"
sondes[0][1]="28-031574449aff"
#Nom et id de la sonde 2
sondes[1][0]="chambre"
sondes[1][1]="28-03157474cdff"
#Nom et id de la sonde 3
sondes[2][0]="exterieur"
sondes[2][1]="28-0315747700ff"


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
data['date']=datetime.now()

#3. Sauvegarde dans le compte mongolab de cet enrgistrement
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_default_database()
# Choix de la collection 
temperatures = db[MONGODB_COLLECTION]
temperatures.insert(data)


#4. Construction du bilan
bilan = {}
cursor = temperatures.find()
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
 
        if libelle in bilan :
	   temperatureSonde = bilan[libelle]
           temperatureSonde['libelle']=libelle
           temperatureSonde['courant']=temp
           temperatureSonde['dateTraitement']=datetime.now()
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
           temperatureSonde['libelle']=libelle
           temperatureSonde['courant']=temp
           temperatureSonde['mini']=temp
           temperatureSonde['maxi']=temp
	   temperatureSonde['maxiDate'] = dateTraitement
	   temperatureSonde['maxiHeure'] = heureTraitement
	   temperatureSonde['miniDate'] = dateTraitement
	   temperatureSonde['miniHeure'] = heureTraitement
           temperatureSonde['dateTraitement']=datetime.now()

	#Ajout de cette sone au tableau
 	bilan[libelle]=temperatureSonde


#5. Sauvegarde dans le compte mongolab du nouveau bilan
temperature_bilan = db[MONGODB_COLLECTION_BILAN]
#Suppression de tous les documents
temperature_bilan.remove({});
#Ajout d'un document par sonde
for key, value in bilan.iteritems():
	temperature_bilan.insert(value)

