# -*- coding: utf-8 -*-
# [START imports]
import sys
sys.path.insert(0, 'libs')
import os, jinja2, webapp2, requests, json
from datetime import datetime
from util import diffNombre, getJour, getSommesJour, getSommesMois, format_int,dateEnClair, convertir_euro, getMois, getMoisAn, \
			getJourHier, getjourMois, getSommesJourHier, Elec_bilan, getSommesMoisAn, getSommesAn, getJuillet, getValueMax, \
			randomString, randomInt, getSommesAnPrec

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]


CLEF="<clef>"

http_start = "https://api.mongolab.com/api/1/"

http_type = "databases/edf/collections/edf_bilan"
http_type_mensuel = "databases/edf/collections/edf_bilan_mensuel"
http_type_annuel = "databases/edf/collections/edf_bilan_annuel"
http_type_annuel_juillet = "databases/edf/collections/edf_bilan_annuel_juillet"

api = {"apiKey": CLEF,"f":'{"_id": 0}'}
api_order_mensuel = {"apiKey": CLEF,"f":'{"_id": 0}', "s":'{"numMois": 1}'}
api_order_annuel = {"apiKey": CLEF,"f":'{"_id": 0}', "s":'{"an": 1}'}

headers = {"Content-Type": "application/json"}


# [START main_page]
class pagePrincipale(webapp2.RequestHandler):


	def get(self):
		# Request sur les valeurs/an
		a = requests.get(http_start+http_type_annuel, params=api_order_annuel, headers=headers)
		data_annuel = json.loads(a.text)

		# Request sur les valeurs/an au mois de juillet
		aj = requests.get(http_start+http_type_annuel_juillet, params=api_order_annuel, headers=headers)
		data_annuel_juillet = json.loads(aj.text)

		# Request sur les valeurs/mois
		m = requests.get(http_start+http_type_mensuel, params=api_order_mensuel, headers=headers)
		data_mensuel = json.loads(m.text)
		#self.response.write(data_mensuel)

		# Request sur les valeurs du bilan
		r = requests.get(http_start+http_type, params=api, headers=headers)
		data = json.loads(r.text)

		#self.response.write(data)
		dateTraitement = datetime.strptime(data[0]['date']['$date'],'%Y-%m-%dT%H:%M:%S.%fZ') 
		heureTraitement = datetime.strftime(dateTraitement, "%H")

		#Array Json en un objet
		bilan_edf = [Elec_bilan(**k) for k in data]
		bilan=bilan_edf[0]

		#self.response.write(getminSemaine(listeSondes[0]).count(','))
		consoJourHc = diffNombre(bilan.heuresCreuses, bilan.heuresCreusesHier) 
		consoJourHp = diffNombre(bilan.heuresPleines, bilan.heuresPleinesHier) 
		consoJourHcVeille = diffNombre(bilan.heuresCreusesHier, bilan.heuresCreusesAvantHier) 
		consoJourHpVeille = diffNombre(bilan.heuresPleinesHier, bilan.heuresPleinesAvantHier) 
		consoJourHcVeille = diffNombre(consoJourHc, consoJourHcVeille) 
		consoJourHpVeille = diffNombre(consoJourHp, consoJourHpVeille) 
		totalJour, minJour, maxJour, totalJourEuro = getSommesJour(bilan)
		totalJourHier, minJourHier, maxJourHier, totalJourEuroHier = getSommesJourHier(bilan)
		totalMois, minMois, maxMois, totalMoisEuro = getSommesMois(bilan)
		totalMoisAn, minMoisAn, maxMoisAn, totalMoisAnEuro = getSommesMoisAn(bilan)
		
		serieAn,labelMois, totalAn, totalAnEuros, minAn, maxAn = getSommesAn(data_mensuel)
		serieAnPrec, labelMoisPrec, totalAnPrec, totalAnPrecEuros, minAnPrec, maxAnPrec = getSommesAnPrec(data_mensuel)
			
		labelJuillet, serieJuillet = getJuillet(data_annuel_juillet)

		maxConsoMensuel, minConsoMensuel = getValueMax(data_mensuel)
		
		#Data du template
		template_values = {
			'date' : dateEnClair(dateTraitement),
			'heure' : datetime.strftime(dateTraitement, "%H:%M"),
			#'puissanceWatt': format_nombre(int(bilan.intensiteInstant)*TENSION_VOLT), 
			'puissanceWatt': format_int(int(bilan.puissanceApparente)), 
			'puissanceEuro': convertir_euro(bilan.puissanceApparente,heureTraitement), 
			
			'intensiteInstant': int(bilan.intensiteInstant), 
			'intensiteSouscrit': int(bilan.intensiteSouscrit), 
        	'intensiteMaximum': int(bilan.intensiteMaximum), 
			'optionTarif': bilan.optionTarif.replace('.',''), 
			'periodeTarifaire': bilan.periodeTarifaire.replace('.',''), 
			'heuresCreuses': format_int(bilan.heuresCreuses),
        	'augmentationHc': format_int(consoJourHc), 
        	'augmentationHcVeille': consoJourHcVeille, 
        	'heuresPleines': format_int(bilan.heuresPleines),
        	'augmentationHp': format_int(consoJourHp),
        	'augmentationHpVeille': consoJourHpVeille, 
        	'adresseConcentrateur': bilan.adresseConcentrateur, 
        	'puissanceApparente': bilan.puissanceApparente, 

        	'totalJour' : format_int(totalJour),
        	'totalJourEuro' : totalJourEuro,
        	'minJour' : format_int(minJour),
        	'maxJour' : format_int(maxJour),
			'serieJour' : getJour(bilan),


        	'totalJourHier' : format_int(totalJourHier),
        	'totalJourEuroHier' : totalJourEuroHier,
        	'minJourHier' : format_int(minJourHier),
        	'maxJourHier' : format_int(maxJourHier),
			'serieJourHier' : getJourHier(bilan),

			'totalMois' : format_int(totalMois),
			'totalMoisEuro' : totalMoisEuro,
			'minMois' : format_int(minMois),
			'maxMois' : format_int(maxMois),
			'totalMoisAn' : format_int(totalMoisAn),
			'totalMoisAnEuro' : totalMoisAnEuro,
			'minMoisAn' : format_int(minMoisAn),
			'maxMoisAn' : format_int(maxMoisAn),
        	'serieMois' : getMois(bilan),
        	'serieMoisAn' : getMoisAn(bilan),
			'jourMois' : getjourMois(dateTraitement, getMois(bilan)),
			
			'serieAn' : serieAn,
			'labelMois' : labelMois,
			'totalAn' : format_int(totalAn),
			'totalAnEuros' : totalAnEuros,
			'minAn' : format_int(minAn),
			'maxAn' : format_int(maxAn),

			'serieAnPrec' : serieAnPrec,
			'labelMoisPrec' : labelMoisPrec,
			'totalAnPrec' : format_int(totalAnPrec),
			'totalAnPrecEuros' : totalAnPrecEuros,
			'minAnPrec' : format_int(minAnPrec),
			'maxAnPrec' : format_int(maxAnPrec),

			'labelJuillet' : labelJuillet,
			'serieJuillet' : serieJuillet,
			
			'statMaxDate0' : dateEnClair(datetime.strptime(bilan.statMaxDate0['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
			'statMaxDate1' : dateEnClair(datetime.strptime(bilan.statMaxDate1['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
			'statMaxDate2' : dateEnClair(datetime.strptime(bilan.statMaxDate2['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
			'statMaxDate3' : dateEnClair(datetime.strptime(bilan.statMaxDate3['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
			'statMaxDate4' : dateEnClair(datetime.strptime(bilan.statMaxDate4['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
			'statMaxDate5' : dateEnClair(datetime.strptime(bilan.statMaxDate5['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
			'statMaxDate6' : dateEnClair(datetime.strptime(bilan.statMaxDate6['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
			'statMaxDate7' : dateEnClair(datetime.strptime(bilan.statMaxDate7['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
            'statMaxTotal0' : bilan.statMaxTotal0,
            'statMaxTotal1' : bilan.statMaxTotal1,
            'statMaxTotal2' : bilan.statMaxTotal2,
            'statMaxTotal3' : bilan.statMaxTotal3,
            'statMaxTotal4' : bilan.statMaxTotal4,
            'statMaxTotal5' : bilan.statMaxTotal5,
            'statMaxTotal6' : bilan.statMaxTotal6,
            'statMaxTotal7' : bilan.statMaxTotal7,
            'statMaxhp0' : int(bilan.statMaxhp0)/1000,
            'statMaxhp1' : int(bilan.statMaxhp1)/1000,
            'statMaxhp2' : int(bilan.statMaxhp2)/1000,
            'statMaxhp3' : int(bilan.statMaxhp3)/1000,
            'statMaxhp4' : int(bilan.statMaxhp4)/1000,
            'statMaxhp5' : int(bilan.statMaxhp5)/1000,
            'statMaxhp6' : int(bilan.statMaxhp6)/1000,
            'statMaxhp7' : int(bilan.statMaxhp7)/1000,
            'statMaxhc0' : int(bilan.statMaxhc0)/1000,
            'statMaxhc1' : int(bilan.statMaxhc1)/1000,
            'statMaxhc2' : int(bilan.statMaxhc2)/1000,
            'statMaxhc3' : int(bilan.statMaxhc3)/1000,
            'statMaxhc4' : int(bilan.statMaxhc4)/1000,
            'statMaxhc5' : int(bilan.statMaxhc5)/1000,
            'statMaxhc6' : int(bilan.statMaxhc6)/1000,
            'statMaxhc7' : int(bilan.statMaxhc7)/1000,
            'statMinDate0' : dateEnClair(datetime.strptime(bilan.statMinDate0['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
            'statMinDate1' : dateEnClair(datetime.strptime(bilan.statMinDate1['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
            'statMinDate2' : dateEnClair(datetime.strptime(bilan.statMinDate2['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
            'statMinDate3' : dateEnClair(datetime.strptime(bilan.statMinDate3['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
            'statMinDate4' : dateEnClair(datetime.strptime(bilan.statMinDate4['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
            'statMinDate5' : dateEnClair(datetime.strptime(bilan.statMinDate5['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
            'statMinDate6' : dateEnClair(datetime.strptime(bilan.statMinDate6['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
            'statMinDate7' : dateEnClair(datetime.strptime(bilan.statMinDate7['$date'],'%Y-%m-%dT%H:%M:%S.%fZ')),
            'statMinTotal0' : bilan.statMinTotal0,
            'statMinTotal1' : bilan.statMinTotal1,
            'statMinTotal2' : bilan.statMinTotal2,
            'statMinTotal3' : bilan.statMinTotal3,
            'statMinTotal4' : bilan.statMinTotal4,
            'statMinTotal5' : bilan.statMinTotal5,
            'statMinTotal6' : bilan.statMinTotal6,
            'statMinTotal7' : bilan.statMinTotal7,
            'statMinhp0' : bilan.statMinhp0,
            'statMinhp1' : bilan.statMinhp1,
            'statMinhp2' : bilan.statMinhp2,
            'statMinhp3' : bilan.statMinhp3,
            'statMinhp4' : bilan.statMinhp4, 
            'statMinhp5' : bilan.statMinhp5, 
            'statMinhp6' : bilan.statMinhp6, 
            'statMinhp7' : bilan.statMinhp7, 
            'statMinhc0' : bilan.statMinhc0,
            'statMinhc1' : bilan.statMinhc1,
            'statMinhc2' : bilan.statMinhc2,
            'statMinhc3' : bilan.statMinhc3,
            'statMinhc4' : bilan.statMinhc4,
            'statMinhc5' : bilan.statMinhc5,
            'statMinhc6' : bilan.statMinhc6,
            'statMinhc7' : bilan.statMinhc7,
            'randomString' : randomString(),
            'randomInt' : randomInt(),
            'mensuel' : data_mensuel,
            'maxConsoMensuel' : maxConsoMensuel,
            'minConsoMensuel' : minConsoMensuel,
            'annuel' : data_annuel,
            'annuel_juillet' : data_annuel_juillet
			#'libelle' : libelle,
			#'date' : dateEnClair(dateTraitement),
			#'heure' : datetime.strftime(dateTraitement, "%H:%M"),
			#'seriesJour' : getJour(listeSondes[0]),
			#'minJour' : getminSerie(getJour(listeSondes[0])),
			#'maxJour' : getmaxSerie(getJour(listeSondes[0])),
			#'minSeriesSemaine' : getminSemaine(listeSondes[0]),
			#'maxSeriesSemaine' : getmaxSemaine(listeSondes[0]),
			#'minSemaine' : getminSerie(getminSemaine(listeSondes[0])),
			#'maxSemaine' : getmaxSerie(getmaxSemaine(listeSondes[0])),
			#'jourSemaine' : getjourSemaine(dateTraitement, getminSemaine(listeSondes[0])),
			#'minSeriesMois' : getminMois(listeSondes[0]),
			#'maxSeriesMois' : getmaxMois(listeSondes[0]),
			#'minMois' : getminSerie(getminMois(listeSondes[0])),
			#'maxMois' : getmaxSerie(getmaxMois(listeSondes[0])),
			#'jourMois' : getjourMois(dateTraitement, getminMois(listeSondes[0])),
			#'minSeriesAnnee' : getminAnnee(listeSondes[0]),
			#'maxSeriesAnnee' : getmaxAnnee(listeSondes[0]),
			#'minAnnee' : getminSerie(getminAnnee(listeSondes[0])),
			#'maxAnnee' : getmaxSerie(getmaxAnnee(listeSondes[0])),
			#'nomMois' : getnomMois(dateTraitement, getminAnnee(listeSondes[0])),
		}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))
# [END main_page]

app = webapp2.WSGIApplication([
    ('/', pagePrincipale),
], debug=True)