# WebApp temperatures

Cette webapp permet d'afficher les temp�ratures capt�es par le #raspberryPi et stock�es dans une base mLab (anciennement mongoLab).

![Temperature1](https://github.com/lcapdecomme/raspberry/blob/master/img/temperature1.png)
![Temperature2](https://github.com/lcapdecomme/raspberry/blob/master/img/temperature2.png)


## Fonctionnement 

L'application est �crite en python et d�ploy�e sur Google AppEngine. Il est donc n�cessaire de cr�er un compte sur cette plateforme.

Les donn�es sont r�cup�r�es de la bd mongoDb sur mLab. Un compte est l� aussi n�cessaire pour le stockage et la restitution des donn�es.

La base mongoLab contient trois collections :

1. **temperature** : relev�s toutes les heures des temp�ratures pour l'ensemble des sondes

2. **temperature_bilan** : donn�es de la page d'accueil. Ces donn�es sont calcul�es par le batch sauveTemperature.py. On trouve donc uniquement un enrgistrement par sonde.

3. **temperature_stat** : donn�es des pages statistiques. Ces donn�es sont calcul�es �galement par le batch sauveTemperature.py. On trouve donc uniquement un enrgistrement par sonde.


## Param�trage

Pour les deux pages WEB, il faut juste renseigner les informations pour se connecter � l'api Rest de mlab.
Les informations sont identiques sur les deux pages � l'exception du nom de la collection (cf ci-dessus)

```python
http_start = "https://api.mongolab.com/api/1/"
# Ces deux propri�t�s <nomDataBase> et <nomCollection> sont � personnaliser (fournies par mongolab) !!!!
http_type = "databases/<nomDataBase>/collections/<nomCollection>"
# Cette propri�t� <clef> est � personnaliser (fournie par mongolab) !!!!
api = {"apiKey": "<clef>","f":"{'_id': 0}"}
headers = {"Content-Type": "application/json"}



