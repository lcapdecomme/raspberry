# Scripts temperatures


## listTemperature.py 

Ce script se connecte à la bd mongo sur mLab et parcours tous les enregistrements pour retrouver les températures courantes, mini. et maxi. pour une sonde.


## voirTemperature.py

Ce script python interroge les sondes connectées au raspeberryPi et affiche les températures instantannées.


## sauveTemperature.py

Ce script ajoute les relevés des sondes en base puis calcule le bilan et les statistiques par sonde. Ce script va donc : 

1. Ajouter un enregistrement contenant les relevés des sondes dans la collection **MONGODB_COLLECTION**

2. Insérer un enregistrement bilan par sonde dans la collection **MONGODB_COLLECTION_BILAN** après l'avoir vider

3. Insérer un enregistrement statistique par sonde dans la collection **MONGODB_COLLECTION_STAT** après l'avoir vider

