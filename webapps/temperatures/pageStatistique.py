# [START imports]
import sys
sys.path.insert(0, 'libs')
import os, jinja2, webapp2, requests, json, datetime, re
from datetime import datetime
from collections import namedtuple
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

http_start = "https://api.mongolab.com/api/1/"
# Ces deux propriétés <nomDataBase> et <nomCollection> sont à personnaliser (fournies par mongolab) !!!!
http_type = "databases/<nomDataBase>/collections/<nomCollection>"
# Cette propriété <clef> est à personnaliser (fournie par mongolab) !!!!
api = {"apiKey": "<clef>","f":"{'_id': 0}"}
headers = {"Content-Type": "application/json"}

Sonde = namedtuple('Sonde', 'heure0,heure1,heure2,heure3,heure4,heure5,heure6,heure7,heure8,heure9,heure10,heure11,heure12,heure13, \
        heure14,heure15,heure16,heure17,heure18,heure19,heure20,heure21,heure22,heure23, \
        minJour1,maxJour1,minJour2,maxJour2,minJour3,maxJour3,minJour4,maxJour4, \
        minJour5,maxJour5,minJour6,maxJour6,minJour7,maxJour7,minJour8,maxJour8,minJour9,maxJour9,minJour10,maxJour10, \
        minJour11,maxJour11,minJour12,maxJour12,minJour13,maxJour13,minJour14,maxJour14, \
        minJour15,maxJour15,minJour16,maxJour16,minJour17,maxJour17,minJour18,maxJour18, \
        minJour19,maxJour19,minJour20,maxJour20,minJour21,maxJour21,minJour22,maxJour22, \
        minJour23,maxJour23,minJour24,maxJour24,minJour25,maxJour25,minJour26,maxJour26, \
        minJour27,maxJour27,minJour28,maxJour28,minJour29,maxJour29,minJour30,maxJour30, \
        minMois1,maxMois1,minMois2,maxMois2,minMois3,maxMois3,minMois4,maxMois4,minMois5,maxMois5,minMois6,maxMois6, \
        minMois7,maxMois7,minMois8,maxMois8,minMois9,maxMois9,minMois10,maxMois10,minMois11,maxMois11,minMois12,maxMois12, \
        libelle,dateTraitement')

def convertDate(dateTraitement):
	day=datetime.strftime(dateTraitement, "%d")
	month = int(datetime.strftime(dateTraitement, "%m"))
	year=datetime.strftime(dateTraitement, "%Y")
	mois=['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
	return day + " " + mois[month-1] + " " + year


def dateEnClair(dateTraitement):
	dateTemp=datetime.strftime(dateTraitement, "%d-%m-%Y")
	dateDuJour=datetime.strftime(datetime.now(), "%d-%m-%Y")
	if dateTemp == dateDuJour :
		return "Aujourd'hui"
	else:
		return convertDate(dateTraitement)

def getJour(s):
    return removeFirstComma((str(s.heure0)+","+str(s.heure1)+","+str(s.heure2)+","+str(s.heure3)+","+str(s.heure4)+","+str(s.heure5)+","+ \
		   str(s.heure6)+","+str(s.heure7)+","+str(s.heure8)+","+str(s.heure9)+","+str(s.heure10)+","+str(s.heure11)+","+ \
		   str(s.heure12)+","+str(s.heure13)+","+str(s.heure14)+","+str(s.heure15)+","+str(s.heure16)+","+str(s.heure17)+","+ \
		   str(s.heure18)+","+str(s.heure19)+","+str(s.heure20)+","+str(s.heure21)+","+str(s.heure22)+","+str(s.heure23)).replace(",,", ""))

	
def getminSemaine(s):
	return removeFirstComma((str(s.minJour24)+","+str(s.minJour25)+","+str(s.minJour26)+","+str(s.minJour27)+","+str(s.minJour28)+","+ \
	       str(s.minJour29)+","+str(s.minJour30)).replace(",,", ""))


def getmaxSemaine(s):
	return removeFirstComma((str(s.maxJour24)+","+str(s.maxJour25)+","+str(s.maxJour26)+","+str(s.maxJour27)+","+str(s.maxJour28)+","+ \
	       str(s.maxJour29)+","+str(s.maxJour30)).replace(",,", ""))


def getminMois(s):
	return removeFirstComma((str(s.minJour1)+","+str(s.minJour2)+","+str(s.minJour3)+","+str(s.minJour4)+","+str(s.minJour5)+","+str(s.minJour6) \
		   +","+str(s.minJour7)+","+str(s.minJour8)+","+str(s.minJour9)+","+str(s.minJour10)+","+str(s.minJour11)+","+str(s.minJour12) \
		   +","+str(s.minJour13)+","+str(s.minJour14)+","+str(s.minJour15)+","+str(s.minJour16)+","+str(s.minJour17)+","+str(s.minJour8) \
		   +","+str(s.minJour19)+","+str(s.minJour20)+","+str(s.minJour21)+","+str(s.minJour22)+","+str(s.minJour23)+","+str(s.minJour24) \
		   +","+str(s.minJour25)+","+str(s.minJour26)+","+str(s.minJour27)+","+str(s.minJour28)+","+str(s.minJour29)+","+str(s.minJour30)).replace(",,", ""))


def getmaxMois(s):
	return removeFirstComma((str(s.maxJour1)+","+str(s.maxJour2)+","+str(s.maxJour3)+","+str(s.maxJour4)+","+str(s.maxJour5)+","+str(s.maxJour6) \
		   +","+str(s.maxJour7)+","+str(s.maxJour8)+","+str(s.maxJour9)+","+str(s.maxJour10)+","+str(s.maxJour11)+","+str(s.maxJour12) \
		   +","+str(s.maxJour13)+","+str(s.maxJour14)+","+str(s.maxJour15)+","+str(s.maxJour16)+","+str(s.maxJour17)+","+str(s.maxJour8) \
		   +","+str(s.maxJour19)+","+str(s.maxJour20)+","+str(s.maxJour21)+","+str(s.maxJour22)+","+str(s.maxJour23)+","+str(s.maxJour24) \
		   +","+str(s.maxJour25)+","+str(s.maxJour26)+","+str(s.maxJour27)+","+str(s.maxJour28)+","+str(s.maxJour29)+","+str(s.maxJour30)).replace(",,", ""))


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


#Retourne l'echelle pour le graphique semaine
#Cela devrait ressembler a qq chose comme  "\"Lu.\", \"Ma.\", \"Me.\", ...
def getjourSemaine(d, s):
	occur = s.count(',')
	chaine=""
	if occur>0:
		#Tableau des jours de 0 a 6
		semaine=['Lu.','Ma.','Me.','Je.','Ve.','Sa.','Di.']
		pos = d.weekday()
		chaine="\""+semaine[pos]+"\""
		for i in range(occur,0,-1):
			pos = pos - 1
			if pos < 0:
				pos=6
			chaine="\""+semaine[pos]+"\","+chaine

	return chaine


#Retourne l'echelle pour le graphique annee
#Cela devrait ressembler a qq chose comme  "\"J.\", \"F.\", \"M.\", ...
def getnomMois(d, s):
	occur = s.count(',')
	chaine=""
	#Tableau des mois de 0 a 11
	mois=['Ja.','Fe.','Ma.','Av.','Ma.','Ju.','Ji.','Ao.','Se.','Oc.','No.','De.']

	#1. nom des mois precedents
	pos = d.month-1
	chaine="\""+mois[pos]+"\""
	for i in range(occur,0,-1):
		pos = pos - 1
		if pos < 0:
			pos=11
		chaine="\""+mois[pos]+"\","+chaine
  
    #Si moins d'une annee, on complete avec les mois suivants
	occur = s.count(',')
	pos = d.month-1
	for i in range(12-occur):
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


def getminSerie(s):
	min=100
	values = s.split(",")  
	for i in values:
		if isfloat(i):
			num = float(i)
			if num<min:
				min=num
	return min


def getmaxSerie(s):
	max=0
	values = s.split(",")  
	for i in values:
		if isfloat(i):
			num = float(i)
			if num>max:
				max=num

	return max


# [START main_page]
class StatPage(webapp2.RequestHandler):
	def get(self):
		libelle = self.request.get('libelle')
		#self.response.write(libelle)
		api["q"] = "{'libelle': '"+libelle+"'}"
		r = requests.get(http_start+http_type, params=api, headers=headers)
		data = json.loads(r.text)
		#self.response.write(data)
		dateTraitement = datetime.strptime(data[0]['dateTraitement']['$date'],'%Y-%m-%dT%H:%M:%S.%fZ') 

		#Array Json en une liste d'objets
		listeSondes = [Sonde(**k) for k in data]

		#self.response.write(getminSemaine(listeSondes[0]).count(','))

		#Data du template
		template_values = {
			'libelle' : libelle,
			'date' : dateEnClair(dateTraitement),
			'heure' : datetime.strftime(dateTraitement, "%H:%M"),
			'seriesJour' : getJour(listeSondes[0]),
			'minJour' : getminSerie(getJour(listeSondes[0])),
			'maxJour' : getmaxSerie(getJour(listeSondes[0])),
			'minSeriesSemaine' : getminSemaine(listeSondes[0]),
			'maxSeriesSemaine' : getmaxSemaine(listeSondes[0]),
			'minSemaine' : getminSerie(getminSemaine(listeSondes[0])),
			'maxSemaine' : getmaxSerie(getmaxSemaine(listeSondes[0])),
			'jourSemaine' : getjourSemaine(dateTraitement, getminSemaine(listeSondes[0])),
			'minSeriesMois' : getminMois(listeSondes[0]),
			'maxSeriesMois' : getmaxMois(listeSondes[0]),
			'minMois' : getminSerie(getminMois(listeSondes[0])),
			'maxMois' : getmaxSerie(getmaxMois(listeSondes[0])),
			'minSeriesAnnee' : getminAnnee(listeSondes[0]),
			'maxSeriesAnnee' : getmaxAnnee(listeSondes[0]),
			'minAnnee' : getminSerie(getminAnnee(listeSondes[0])),
			'maxAnnee' : getmaxSerie(getmaxAnnee(listeSondes[0])),
			'nomMois' : getnomMois(dateTraitement, getminAnnee(listeSondes[0])),
		}
		template = JINJA_ENVIRONMENT.get_template('stat.html')
		self.response.write(template.render(template_values))
# [END main_page]

app = webapp2.WSGIApplication([
    ('/stat', StatPage),
], debug=True)