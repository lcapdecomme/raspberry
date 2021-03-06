#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NAME: teleinfoERDF.py
# AUTHOR: Lionel Capdecomme
# DATE  : 24/01/2016
# COMMENT: Lecture des trames Teleinformation 

# Initialisation 
base_dir = '/sys/bus/w1/devices/'
nbSondes=3
nbProps=3 # 1:lieu, 2: nom du fichier, 3:valeur
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

print "Les températures de la maison:"

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
    result=sondes[i][0]+" : "+str(sondes[i][2])+"°"
    print result

print "http://temperatures-1214.appspot.com"
print "#raspberryPi"
