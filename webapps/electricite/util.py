# -*- coding: utf-8 -*-
# [START imports]
from datetime import datetime, timedelta
from collections import namedtuple
import random
import string

TENSION_VOLT = 230
tarifHP = 0.16360 
tarifHC = 0.11500
tarifHB = 0.14

mois=['Jan.','Fev.','Mar.','Avr.','Mai','Juin','Jui.','Aout','Sep.','Oct.','Nov.','Dec.']

Elec_bilan = namedtuple('Elec_bilan', 'periodeTarifaire, intensiteInstant, intensiteSouscrit, optionTarif, heuresCreuses, \
        intensiteMaximum, adresseConcentrateur, heuresPleines,puissanceApparente, date, heuresPleinesHier, \
        heuresCreusesHier, heuresPleinesAvantHier,heuresCreusesAvantHier, \
        jour1,jour2,jour3,jour4,jour5,jour6,jour7,jour8,jour9,jour10, \
        jour11,jour12,jour13,jour14,jour15,jour16,jour17,jour18, \
        jour19,jour20,jour21,jour22,jour23,jour24,jour25,jour26, \
        jour27,jour28,jour29,jour30, \
		jourUnAn1,jourUnAn2,jourUnAn3,jourUnAn4,jourUnAn5,jourUnAn6,jourUnAn7,jourUnAn8,jourUnAn9,jourUnAn10, \
		jourUnAn11,jourUnAn12,jourUnAn13,jourUnAn14,jourUnAn15,jourUnAn16,jourUnAn17,jourUnAn18, \
		jourUnAn19,jourUnAn20,jourUnAn21,jourUnAn22,jourUnAn23,jourUnAn24,jourUnAn25,jourUnAn26, \
		jourUnAn27,jourUnAn28,jourUnAn29,jourUnAn30, \
        heure0,heure1,heure2,heure3,heure4,heure5,heure6,heure7,heure8,heure9,heure10, \
        heure11,heure12,heure13,heure14,heure15,heure16,heure17,heure18, \
        heure19,heure20,heure21,heure22,heure23, \
        heureHier0,heureHier1,heureHier2,heureHier3,heureHier4,heureHier5,heureHier6,heureHier7,heureHier8,heureHier9,heureHier10, \
        heureHier11,heureHier12,heureHier13,heureHier14,heureHier15,heureHier16,heureHier17,heureHier18, \
        heureHier19,heureHier20,heureHier21,heureHier22,heureHier23, \
        mois1,mois2,mois3,mois4,mois5,mois6,mois7,mois8,mois9,mois10, \
        mois11,mois12, \
        statMaxDate0,statMaxDate1,statMaxDate2,statMaxDate3,statMaxDate4,statMaxDate5,statMaxDate6,statMaxDate7, \
        statMaxTotal0,statMaxTotal1,statMaxTotal2,statMaxTotal3,statMaxTotal4,statMaxTotal5,statMaxTotal6,statMaxTotal7, \
        statMaxhp0,statMaxhp1,statMaxhp2,statMaxhp3,statMaxhp4,statMaxhp5,statMaxhp6,statMaxhp7, \
        statMaxhc0,statMaxhc1,statMaxhc2,statMaxhc3,statMaxhc4,statMaxhc5,statMaxhc6,statMaxhc7, \
        statMinDate0,statMinDate1,statMinDate2,statMinDate3,statMinDate4,statMinDate5,statMinDate6,statMinDate7, \
        statMinTotal0,statMinTotal1,statMinTotal2,statMinTotal3,statMinTotal4,statMinTotal5,statMinTotal6,statMinTotal7, \
        statMinhp0,statMinhp1,statMinhp2,statMinhp3,statMinhp4,statMinhp5,statMinhp6,statMinhp7, \
        statMinhc0,statMinhc1,statMinhc2,statMinhc3,statMinhc4,statMinhc5,statMinhc6,statMinhc7')


def randomString(stringLength=5):
	#Generate a random string of fixed length
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(stringLength))

def randomInt(intLength=100):
	#Generate a random string of fixed length
	return random.randint(1,intLength)


def convertDate(dateTraitement):
	day=datetime.strftime(dateTraitement, "%d")
	month = int(datetime.strftime(dateTraitement, "%m"))
	year=datetime.strftime(dateTraitement, "%Y")
	return day + " " + mois[month-1] + " " + year


def dateEnClair(dateTraitement):
	dateHier=dateTraitement + timedelta(-1)
	dateTemp=datetime.strftime(dateHier, "%d-%m-%Y")
	return convertDate(dateHier)


def concatDifference(chaine,val, derniereVal, ecart):
	if val != "":
		if derniereVal != 0:
			ecart = derniereVal - val
			if chaine == "":
				chaine=str(ecart)
			else:
				chaine=str(ecart)+","+chaine
		else:
			ecart = 0
		derniereVal = val
	else:
		derniereVal = derniereVal-(ecart*1.2)
		if chaine == "":
			chaine=str(ecart)
		else:
			chaine=str(ecart)+","+chaine

	return derniereVal, chaine, ecart



def getJour(s):
	ecart = 0
	derniereVal = 0
	chaine=""
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure23, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure22, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure21, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure20, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure19, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure18, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure17, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure16, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure15, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure14, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure13, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure12, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure11, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heure10, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heure9, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heure8, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heure7, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heure6, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heure5, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heure4, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heure3, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heure2, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heure1, derniereVal, ecart)	
	derniereVal, chaine, ecart =concatDifference(chaine, s.heure0, derniereVal, ecart)	
	return chaine


def getJourHier(s):
	ecart = 0
	derniereVal = 0
	chaine=""
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier23, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier22, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier21, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier20, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier19, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier18, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier17, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier16, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier15, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier14, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier13, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier12, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier11, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.heureHier10, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heureHier9, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heureHier8, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heureHier7, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heureHier6, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heureHier5, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heureHier4, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heureHier3, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heureHier2, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.heureHier1, derniereVal, ecart)	
	derniereVal, chaine, ecart =concatDifference(chaine, s.heureHier0, derniereVal, ecart)	
	return chaine


def getMois(s):
	ecart = 0
	derniereVal = 0
	chaine=""
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour30, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour29, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour28, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour27, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour26, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour25, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour24, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour23, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour22, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour21, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour20, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour19, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour18, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour17, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour16, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour15, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour14, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour13, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour12, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour11, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jour10, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jour9, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jour8, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jour7, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jour6, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jour5, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jour4, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jour3, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jour2, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jour1, derniereVal, ecart)
	return chaine


def getMoisAn(s):
	ecart = 0
	derniereVal = 0
	chaine=""
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn30, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn29, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn28, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn27, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn26, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn25, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn24, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn23, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn22, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn21, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn20, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn19, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn18, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn17, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn16, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn15, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn14, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn13, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn12, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn11, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine,s.jourUnAn10, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jourUnAn9, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jourUnAn8, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jourUnAn7, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jourUnAn6, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jourUnAn5, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jourUnAn4, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jourUnAn3, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jourUnAn2, derniereVal, ecart)
	derniereVal, chaine, ecart =concatDifference(chaine, s.jourUnAn1, derniereVal, ecart)
	return chaine


# Retourne la valeur max de la liste mensuel 
def getValueMax(liste):
	maxValue=0
	minValue=99999999999
	for element in liste:
		if int(element['diff'])>maxValue:
			maxValue=int(element['diff'])
		if int(element['diff'])<minValue and int(element['diff'])!= 0:
			minValue=int(element['diff'])
	return maxValue, minValue


# Retourne les douze dernières valeures de l'année en cours 
def getSommesAn(liste):
	cpt=0
	serieValeurs=""
	nomMois=""
	totalAn = 0
	mini=9999999999
	maxi=-1
	
	lastElements = liste[-12:]
	for element in lastElements:
		serieValeurs=serieValeurs+str(element['diff'])+","
		nmois=mois[int(element['mo'])-1]
		nomMois=nomMois+"'"+nmois+" "+element['an']+"',"
		conso=int(element['diff'])
		totalAn=totalAn+conso
		if conso<mini:
			mini=conso
		if conso>maxi:
			maxi=conso

		cpt=cpt+1
		if cpt >= 12:
			break
	totalAnEuros=totalAn*tarifHB
	return serieValeurs, nomMois, totalAn, totalAnEuros, mini, maxi



# Retourne les douze dernières valeures de l'année precédente 
def getSommesAnPrec(liste):
	cpt=0
	serieValeurs=""
	nomMois=""
	totalAn = 0
	mini=9999999999
	maxi=-1
	
	lastElements = liste[-24:]
	for element in lastElements:
		serieValeurs=serieValeurs+str(element['diff'])+","
		nmois=mois[int(element['mo'])-1]
		nomMois=nomMois+"'"+nmois+" "+element['an']+"',"
		conso=int(element['diff'])
		totalAn=totalAn+conso
		if conso<mini:
			mini=conso
		if conso>maxi:
			maxi=conso

		cpt=cpt+1
		if cpt >= 12:
			break
	totalAnEuros=totalAn*tarifHB
	return serieValeurs, nomMois, totalAn, totalAnEuros, mini, maxi



def getminAnnee(s):
	return removeFirstComma((str(s.minMois1)+","+str(s.minMois2)+","+str(s.minMois3)+","+str(s.minMois4)+","+str(s.minMois5)+","+str(s.minMois6) \
		   +","+str(s.minMois7)+","+str(s.minMois8)+","+str(s.minMois9)+","+str(s.minMois10)+","+str(s.minMois11)+","+str(s.minMois12)).replace(",,", ""))


def getmaxAnnee(s):
	return removeFirstComma((str(s.maxMois1)+","+str(s.maxMois2)+","+str(s.maxMois3)+","+str(s.maxMois4)+","+str(s.maxMois5)+","+str(s.maxMois6) \
		   +","+str(s.maxMois7)+","+str(s.maxMois8)+","+str(s.maxMois9)+","+str(s.maxMois10)+","+str(s.maxMois11)+","+str(s.maxMois12)).replace(",,", ""))


def removeFirstComma(temp):
	if temp[0] == ",":
		return temp[1:]
	return temp


def diffNombre(a, b):
	try: 
		x=int(a)
		y=int(b)
		return x-y
	except ValueError:
		return 0


def calculIndicateurs(v, to, mi, ma, der):
	tot=to
	mini=mi
	maxi=ma
	if v != "":
		if der != 0:
			ecart = der - v
		else:
			ecart = 0
		der = v
		if ecart>0:
			tot=to+ecart
			if ecart<mi:
				mini=ecart
			if ecart>ma:
				maxi=ecart
	return tot, mini, maxi, der



def getSommesMois(s):
	totalMois = 0
	minMois = 9999999999999
	maxMois = 0
	der=0
	totalEuro=0
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour30, totalMois, minMois, maxMois,der)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour29, totalMois, minMois, maxMois,der)
	if s.jour30!= "" : totalEuro = totalEuro + ((s.jour30-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour28, totalMois, minMois, maxMois,der)
	if s.jour29!= "" : totalEuro = totalEuro + ((s.jour29-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour27, totalMois, minMois, maxMois,der)
	if s.jour28!= "" : totalEuro = totalEuro + ((s.jour28-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour26, totalMois, minMois, maxMois,der)
	if s.jour27!= "" : totalEuro = totalEuro + ((s.jour27-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour25, totalMois, minMois, maxMois,der)
	if s.jour26!= "" : totalEuro = totalEuro + ((s.jour26-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour24, totalMois, minMois, maxMois,der)
	if s.jour25!= "" : totalEuro = totalEuro + ((s.jour25-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour23, totalMois, minMois, maxMois,der)
	if s.jour24!= "" : totalEuro = totalEuro + ((s.jour24-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour22, totalMois, minMois, maxMois,der)
	if s.jour23!= "" : totalEuro = totalEuro + ((s.jour23-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour21, totalMois, minMois, maxMois,der)
	if s.jour22!= "" : totalEuro = totalEuro + ((s.jour22-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour20, totalMois, minMois, maxMois,der)
	if s.jour21!= "" : totalEuro = totalEuro + ((s.jour21-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour19, totalMois, minMois, maxMois,der)
	if s.jour20!= "" : totalEuro = totalEuro + ((s.jour20-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour18, totalMois, minMois, maxMois,der)
	if s.jour19!= "" : totalEuro = totalEuro + ((s.jour19-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour17, totalMois, minMois, maxMois,der)
	if s.jour18!= "" : totalEuro = totalEuro + ((s.jour18-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour16, totalMois, minMois, maxMois,der)
	if s.jour17!= "" : totalEuro = totalEuro + ((s.jour17-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour15, totalMois, minMois, maxMois,der)
	if s.jour16!= "" : totalEuro = totalEuro + ((s.jour16-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour14, totalMois, minMois, maxMois,der)
	if s.jour15!= "" : totalEuro = totalEuro + ((s.jour15-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour13, totalMois, minMois, maxMois,der)
	if s.jour14!= "" : totalEuro = totalEuro + ((s.jour14-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour12, totalMois, minMois, maxMois,der)
	if s.jour13!= "" : totalEuro = totalEuro + ((s.jour13-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour11, totalMois, minMois, maxMois,der)
	if s.jour12!= "" : totalEuro = totalEuro + ((s.jour12-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs(s.jour10, totalMois, minMois, maxMois,der)
	if s.jour11!= "" : totalEuro = totalEuro + ((s.jour11-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs( s.jour9, totalMois, minMois, maxMois,der)
	if s.jour10!= "" : totalEuro = totalEuro + ((s.jour10-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs( s.jour8, totalMois, minMois, maxMois,der)
	if s.jour9!= "" : totalEuro = totalEuro + ((s.jour9-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs( s.jour7, totalMois, minMois, maxMois,der)
	if s.jour8!= "" : totalEuro = totalEuro + ((s.jour8-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs( s.jour6, totalMois, minMois, maxMois,der)
	if s.jour7!= "" : totalEuro = totalEuro + ((s.jour7-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs( s.jour5, totalMois, minMois, maxMois,der)
	if s.jour6!= "" : totalEuro = totalEuro + ((s.jour6-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs( s.jour4, totalMois, minMois, maxMois,der)
	if s.jour5!= "" : totalEuro = totalEuro + ((s.jour5-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs( s.jour3, totalMois, minMois, maxMois,der)
	if s.jour4!= "" : totalEuro = totalEuro + ((s.jour4-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs( s.jour2, totalMois, minMois, maxMois,der)
	if s.jour3!= "" : totalEuro = totalEuro + ((s.jour3-der)/1000*tarifHB)
	totalMois, minMois, maxMois, der =calculIndicateurs( s.jour1, totalMois, minMois, maxMois,der)	
	if s.jour2!= "" : totalEuro = totalEuro + ((s.jour2-der)/1000*tarifHB)
	return totalMois, minMois, maxMois, totalEuro


def getSommesMoisAn(s):
	totalMoisAn = 0
	minMoisAn = 9999999999999
	maxMoisAn = 0
	der=0
	totalEuro=0
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn30, totalMoisAn, minMoisAn, maxMoisAn,der)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn29, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn30!= "" : totalEuro = totalEuro + ((s.jourUnAn30-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn28, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn29!= "" : totalEuro = totalEuro + ((s.jourUnAn29-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn27, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn28!= "" : totalEuro = totalEuro + ((s.jourUnAn28-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn26, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn27!= "" : totalEuro = totalEuro + ((s.jourUnAn27-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn25, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn26!= "" : totalEuro = totalEuro + ((s.jourUnAn26-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn24, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn25!= "" : totalEuro = totalEuro + ((s.jourUnAn25-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn23, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn24!= "" : totalEuro = totalEuro + ((s.jourUnAn24-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn22, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn23!= "" : totalEuro = totalEuro + ((s.jourUnAn23-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn21, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn22!= "" : totalEuro = totalEuro + ((s.jourUnAn22-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn20, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn21!= "" : totalEuro = totalEuro + ((s.jourUnAn21-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn19, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn20!= "" : totalEuro = totalEuro + ((s.jourUnAn20-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn18, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn19!= "" : totalEuro = totalEuro + ((s.jourUnAn19-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn17, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn18!= "" : totalEuro = totalEuro + ((s.jourUnAn18-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn16, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn17!= "" : totalEuro = totalEuro + ((s.jourUnAn17-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn15, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn16!= "" : totalEuro = totalEuro + ((s.jourUnAn16-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn14, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn15!= "" : totalEuro = totalEuro + ((s.jourUnAn15-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn13, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn14!= "" : totalEuro = totalEuro + ((s.jourUnAn14-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn12, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn13!= "" : totalEuro = totalEuro + ((s.jourUnAn13-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn11, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn12!= "" : totalEuro = totalEuro + ((s.jourUnAn12-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs(s.jourUnAn10, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn11!= "" : totalEuro = totalEuro + ((s.jourUnAn11-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs( s.jourUnAn9, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn10!= "" : totalEuro = totalEuro + ((s.jourUnAn10-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs( s.jourUnAn8, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn9!= "" : totalEuro = totalEuro + ((s.jourUnAn9-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs( s.jourUnAn7, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn8!= "" : totalEuro = totalEuro + ((s.jourUnAn8-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs( s.jourUnAn6, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn7!= "" : totalEuro = totalEuro + ((s.jourUnAn7-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs( s.jourUnAn5, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn6!= "" : totalEuro = totalEuro + ((s.jourUnAn6-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs( s.jourUnAn4, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn5!= "" : totalEuro = totalEuro + ((s.jourUnAn5-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs( s.jourUnAn3, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn4!= "" : totalEuro = totalEuro + ((s.jourUnAn4-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs( s.jourUnAn2, totalMoisAn, minMoisAn, maxMoisAn,der)
	if s.jourUnAn3!= "" : totalEuro = totalEuro + ((s.jourUnAn3-der)/1000*tarifHB)
	totalMoisAn, minMoisAn, maxMoisAn, der =calculIndicateurs( s.jourUnAn1, totalMoisAn, minMoisAn, maxMoisAn,der)	
	if s.jourUnAn2!= "" : totalEuro = totalEuro + ((s.jourUnAn2-der)/1000*tarifHB)
	return totalMoisAn, minMoisAn, maxMoisAn, totalEuro



def getSommesJour(s):
	totalJour = 0
	minJour = 9999999999999
	maxJour = 0
	der=0
	totalEuro=0
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure23, totalJour, minJour, maxJour,der)
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure22, totalJour, minJour, maxJour,der)
	if s.heure23!= "" : totalEuro = totalEuro + ((s.heure23-der)/1000*tarifHC)
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure21, totalJour, minJour, maxJour,der)
	if s.heure22!= "" : totalEuro = totalEuro + ((s.heure22-der)/1000*tarifHC)
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure20, totalJour, minJour, maxJour,der)
	if s.heure21!= "" : totalEuro = totalEuro + ((s.heure21-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure19, totalJour, minJour, maxJour,der)
	if s.heure20!= "" : totalEuro = totalEuro + ((s.heure20-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure18, totalJour, minJour, maxJour,der)
	if s.heure19!= "" : totalEuro = totalEuro + ((s.heure19-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure17, totalJour, minJour, maxJour,der)
	if s.heure18!= "" : totalEuro = totalEuro + ((s.heure18-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure16, totalJour, minJour, maxJour,der)
	if s.heure17!= "" : totalEuro = totalEuro + ((s.heure17-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure15, totalJour, minJour, maxJour,der)
	if s.heure16!= "" : totalEuro = totalEuro + ((s.heure16-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure14, totalJour, minJour, maxJour,der)
	if s.heure15!= "" : totalEuro = totalEuro + ((s.heure15-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure13, totalJour, minJour, maxJour,der)
	if s.heure14!= "" : totalEuro = totalEuro + ((s.heure14-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure12, totalJour, minJour, maxJour,der)
	if s.heure13!= "" : totalEuro = totalEuro + ((s.heure13-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure11, totalJour, minJour, maxJour,der)
	if s.heure12!= "" : totalEuro = totalEuro + ((s.heure12-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs(s.heure10, totalJour, minJour, maxJour,der)
	if s.heure11!= "" : totalEuro = totalEuro + ((s.heure11-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs( s.heure9, totalJour, minJour, maxJour,der)
	if s.heure10!= "" : totalEuro = totalEuro + ((s.heure10-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs( s.heure8, totalJour, minJour, maxJour,der)
	if s.heure9!= "" : totalEuro = totalEuro + ((s.heure9-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs( s.heure7, totalJour, minJour, maxJour,der)
	if s.heure8!= "" : totalEuro = totalEuro + ((s.heure8-der)/1000*tarifHP)
	totalJour, minJour, maxJour, der =calculIndicateurs( s.heure6, totalJour, minJour, maxJour,der)
	if s.heure7!= "" : totalEuro = totalEuro + ((s.heure7-der)/1000*tarifHC)
	totalJour, minJour, maxJour, der =calculIndicateurs( s.heure5, totalJour, minJour, maxJour,der)
	if s.heure6!= "" : totalEuro = totalEuro + ((s.heure6-der)/1000*tarifHC)
	totalJour, minJour, maxJour, der =calculIndicateurs( s.heure4, totalJour, minJour, maxJour,der)
	if s.heure5!= "" : totalEuro = totalEuro + ((s.heure5-der)/1000*tarifHC)
	totalJour, minJour, maxJour, der =calculIndicateurs( s.heure3, totalJour, minJour, maxJour,der)
	if s.heure4!= "" : totalEuro = totalEuro + ((s.heure4-der)/1000*tarifHC)
	totalJour, minJour, maxJour, der =calculIndicateurs( s.heure2, totalJour, minJour, maxJour,der)
	if s.heure3!= "" : totalEuro = totalEuro + ((s.heure3-der)/1000*tarifHC)
	totalJour, minJour, maxJour, der =calculIndicateurs( s.heure1, totalJour, minJour, maxJour,der)	
	if s.heure2!= "" : totalEuro = totalEuro + ((s.heure2-der)/1000*tarifHC)
	totalJour, minJour, maxJour, der =calculIndicateurs( s.heure0, totalJour, minJour, maxJour,der)
	if s.heure1!= "" : totalEuro = totalEuro + ((s.heure1-der)/1000*tarifHC)
	return totalJour, minJour, maxJour, totalEuro



def getSommesJourHier(s):
	totalJourHier = 0
	minJourHier = 9999999999999
	maxJourHier = 0
	der=0
	totalEuroHier=0
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier23, totalJourHier, minJourHier, maxJourHier,der)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier22, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier23!= "" : totalEuroHier = totalEuroHier + ((s.heureHier23-der)/1000*tarifHC)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier21, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier22!= "" : totalEuroHier = totalEuroHier + ((s.heureHier22-der)/1000*tarifHC)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier20, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier21!= "" : totalEuroHier = totalEuroHier + ((s.heureHier21-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier19, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier20!= "" : totalEuroHier = totalEuroHier + ((s.heureHier20-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier18, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier19!= "" : totalEuroHier = totalEuroHier + ((s.heureHier19-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier17, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier18!= "" : totalEuroHier = totalEuroHier + ((s.heureHier18-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier16, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier17!= "" : totalEuroHier = totalEuroHier + ((s.heureHier17-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier15, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier16!= "" : totalEuroHier = totalEuroHier + ((s.heureHier16-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier14, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier15!= "" : totalEuroHier = totalEuroHier + ((s.heureHier15-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier13, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier14!= "" : totalEuroHier = totalEuroHier + ((s.heureHier14-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier12, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier13!= "" : totalEuroHier = totalEuroHier + ((s.heureHier13-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier11, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier12!= "" : totalEuroHier = totalEuroHier + ((s.heureHier12-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs(s.heureHier10, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier11!= "" : totalEuroHier = totalEuroHier + ((s.heureHier11-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs( s.heureHier9, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier10!= "" : totalEuroHier = totalEuroHier + ((s.heureHier10-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs( s.heureHier8, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier9!= "" : totalEuroHier = totalEuroHier + ((s.heureHier9-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs( s.heureHier7, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier8!= "" : totalEuroHier = totalEuroHier + ((s.heureHier8-der)/1000*tarifHP)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs( s.heureHier6, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier7!= "" : totalEuroHier = totalEuroHier + ((s.heureHier7-der)/1000*tarifHC)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs( s.heureHier5, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier6!= "" : totalEuroHier = totalEuroHier + ((s.heureHier6-der)/1000*tarifHC)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs( s.heureHier4, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier5!= "" : totalEuroHier = totalEuroHier + ((s.heureHier5-der)/1000*tarifHC)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs( s.heureHier3, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier4!= "" : totalEuroHier = totalEuroHier + ((s.heureHier4-der)/1000*tarifHC)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs( s.heureHier2, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier3!= "" : totalEuroHier = totalEuroHier + ((s.heureHier3-der)/1000*tarifHC)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs( s.heureHier1, totalJourHier, minJourHier, maxJourHier,der)	
	if s.heureHier2!= "" : totalEuroHier = totalEuroHier + ((s.heureHier2-der)/1000*tarifHC)
	totalJourHier, minJourHier, maxJourHier, der =calculIndicateurs( s.heureHier0, totalJourHier, minJourHier, maxJourHier,der)
	if s.heureHier1!= "" : totalEuroHier = totalEuroHier + ((s.heureHier1-der)/1000*tarifHC)
	return totalJourHier, minJourHier, maxJourHier, totalEuroHier



#Retourne l'echelle pour le graphique semaine
#Cela devrait ressembler a qq chose comme  "\"Lu.\", \"Ma.\", \"Me.\", ...
def getjourSemaine(d, s):
	occur = s.count(',')
	chaine=""
	if occur>0:
		#Tableau des jours de 0 a 6
		semaine=['Lu','Ma','Me','Je','Ve','Sa','Di']
		maDate=d
		pos = maDate.weekday()
		posd = maDate.day
		chaine="\""+semaine[pos]+" "+str(posd)+"\""
		for _ in range(occur,0,-1):
			maDate = maDate + timedelta(-1)
			pos = maDate.weekday()
			posd = maDate.day
			if pos < 0:
				pos=6
			chaine="\""+semaine[pos]+" "+str(posd)+"\","+chaine

	return chaine


# Retourne deux séries avec les années et les valeurs 
def getJuillet(serie):
	serieValeurs=""
	nomAnnees=""
	for element in serie:
		if int(element['diff']) != 0:
			serieValeurs=serieValeurs+str(int(element['diff']))+","
			nomAnnees=nomAnnees+"'"+element['an']+"',"

	return nomAnnees, serieValeurs



#Retourne l'echelle pour le graphique mois
#Pour plus de lisibilit�, un jour sur quatre est affich� avec inter
#Cela devrait ressembler a qq chose comme  "4 fev.", "", "", "", "8 fev"
def getjourMois(d, s):
	occur = s.count(',')
	#Tableau des mois de 0 a 11
	mois=['Ja.','Fe.','Ma.','Av.','Ma.','Ju.','Ji.','Ao.','Se.','Oc.','No.','De.']
	#1. nom des mois precedents
	maDate=d+timedelta(-1)
	pos = maDate.day
	posm = maDate.month-1
	chaine="\""+str(pos)+" "+mois[posm]+"\""
	inter=1
	for _ in range(occur,0,-1):
		inter+=1
		maDate = maDate + timedelta(-1)
		pos = maDate.day
		posm = maDate.month-1
		if inter==4:
			chaine="\""+str(pos)+" "+mois[posm]+"\","+chaine
			inter=1
		else:
			chaine="\"\","+chaine
	
	#Si moins d'une annee, on complete avec les mois suivants
	occur = s.count(',')
	maDate=d
	inter=1
	for _ in range(30-occur):
		inter+=1
		maDate = maDate + timedelta(1)
		pos = maDate.day
		posm = maDate.month-1
		if inter==4:
			chaine=chaine+",\""+str(pos)+" "+mois[posm]+"\""
			inter=1
		else:
			chaine=chaine+",\"\""

	return chaine



#Retourne l'echelle pour le graphique annee
#Cela devrait ressembler a qq chose comme  "\"J.\", \"F.\", \"M.\", ...
def getnomMois(d, s):
	occur = s.count(',')
	#Tableau des mois de 0 a 11
	mois=['Ja.','Fe.','Ma.','Av.','Ma.','Ju.','Ji.','Ao.','Se.','Oc.','No.','De.']

	#1. nom des mois precedents
	pos = d.month-1
	chaine="\""+mois[pos]+"\""
	for _ in range(occur,0,-1):
		pos = pos - 1
		if pos < 0:
			pos=11
		chaine="\""+mois[pos]+"\","+chaine

	#Si moins d'une annee, on complete avec les mois suivants
	occur = s.count(',')
	pos = d.month-1
	for _ in range(12-occur):
		pos = pos + 1
		if pos >11:
			pos=0
		chaine=chaine+",\""+mois[pos]+"\""

	return chaine


def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False



def format_int (s):
	b = int(s);
	return '{:,}'.format(b).replace(',', ' ')


def convertir_euro (s, heure):
	b = int(s);
	if heure<7 or heure>21:
		return b*tarifHC/1000
	else:
		return b*tarifHP/1000
