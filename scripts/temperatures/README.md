# Scripts temperatures


## listTemperature.py 

Ce script se connecte � la bd mongo sur mLab et parcours tous les enregistrements pour retrouver les temp�ratures courantes, mini. et maxi. pour une sonde.


## voirTemperature.py

Ce script python interroge les sondes connect�es au raspeberryPi et affiche les temp�ratures instantann�es.


## sauveTemperature.py

Ce script ajoute les relev�s des sondes en base puis calcule le bilan et les statistiques par sonde. Ce script va donc : 

1. Ajouter un enregistrement contenant les relev�s des sondes dans la collection **MONGODB_COLLECTION**

2. Ins�rer un enregistrement bilan par sonde dans la collection **MONGODB_COLLECTION_BILAN** apr�s l'avoir vider

3. Ins�rer un enregistrement statistique par sonde dans la collection **MONGODB_COLLECTION_STAT** apr�s l'avoir vider

