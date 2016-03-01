# WebApp temperatures

Cette webapp permet d'afficher les températures captées par le #raspberryPi et stockées dans une base mLab (anciennement mongoLab).

![Temperature1](https://github.com/lcapdecomme/raspberry/blob/master/img/temperature1.png)
![Temperature2](https://github.com/lcapdecomme/raspberry/blob/master/img/temperature2.png)


## Fonctionnement 

L'application est écrite en python et déployée sur Google AppEngine. Il est donc nécessaire de créer un compte sur cette plateforme.

Les données sont récupérées de la bd mongoDb sur mLab. Un compte est là aussi nécessaire pour le stockage et la restitution des données.

La base mongoLab contient trois collections :

1. **temperature** : relevés toutes les heures des températures pour l'ensemble des sondes

2. **temperature_bilan** : données de la page d'accueil. Ces données sont calculées par le batch sauveTemperature.py. On trouve donc uniquement un enrgistrement par sonde.

3. **temperature_stat** : données des pages statistiques. Ces données sont calculées également par le batch sauveTemperature.py. On trouve donc uniquement un enrgistrement par sonde.


## Paramétrage

Pour les deux pages WEB, il faut juste renseigner les informations pour se connecter à l'api Rest de mlab.
Les informations sont identiques sur les deux pages à l'exception du nom de la collection (cf ci-dessus)

```python
http_start = "https://api.mongolab.com/api/1/"
# Ces deux propriétés <nomDataBase> et <nomCollection> sont à personnaliser (fournies par mongolab) !!!!
http_type = "databases/<nomDataBase>/collections/<nomCollection>"
# Cette propriété <clef> est à personnaliser (fournie par mongolab) !!!!
api = {"apiKey": "<clef>","f":"{'_id': 0}"}
headers = {"Content-Type": "application/json"}



