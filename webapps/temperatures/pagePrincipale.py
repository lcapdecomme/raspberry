# [START imports]
import sys
sys.path.insert(0, 'libs')
import os, jinja2, webapp2, requests, json, datetime
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

Sonde = namedtuple('Sonde', 'libelle, courant, maxi, maxiDate, maxiHeure, mini, miniDate, miniHeure, dateTraitement')

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

# [START main_page]
class MainPage(webapp2.RequestHandler):
	def get(self):
		r = requests.get(http_start+http_type, params=api, headers=headers)
		data = json.loads(r.text)
		dateTraitement = datetime.strptime(data[0]['dateTraitement']['$date'],'%Y-%m-%dT%H:%M:%S.%fZ') 
		#self.response.write(data)
		#Array Json en une liste d'objets
		listeSondes = [Sonde(**k) for k in data]

		#Data du template
		template_values = {
			'temperatures': listeSondes,
			'date' : dateEnClair(dateTraitement),
			'heure' : datetime.strftime(dateTraitement, "%H:%M"),
		}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))
# [END main_page]

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)