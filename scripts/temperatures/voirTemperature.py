#!/usr/bin/env python
# NAME: voirTemperature.py
# AUTHOR: Lionel Capdecomme
# DATE  : 02/02/2016
# COMMENT: Lecture des valeurs des trois sondes de températures 

# Initialisation 
base_dir = '/sys/bus/w1/devices/'
# Ces propriétés sont à personnaliser !!!!
nbSondes=3
nbProps=3 # 1:lieu, 2: nom du fichier, 3:valeur
sondes=[[0 for row in range(0,nbProps)] for col in range(0,nbSondes)]
#Nom et id de la sonde 1
sondes[0][0]="salon"
sondes[0][1]="28-031512449dff"
#Nom et id de la sonde 2
sondes[1][0]="chambre"
sondes[1][1]="28-03151874c1ff"
#Nom et id de la sonde 3
sondes[2][0]="exterieur"
sondes[2][1]="28-0314567700ff"

# Fonction ouverture et lecture d'un fichier
def lireFichier(fichier):
    f = open(fichier, 'r')
    lignes = f.readlines()
    f.close()
    return lignes

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

