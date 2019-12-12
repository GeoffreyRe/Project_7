# Projet-7 : Créez GrandPyBot, le papy robot
--------------------------------------------
Ce projet est le 7ème projet de ma formation de développeur d'application en python auprès de l'établissement formateur OpenClassrooms.

# 1 Informations générales
--------------------------
Créez GrandPyBot, le papy robot

## 1.1 Description du projet
-----------------------------

Le but du projet est de créer une page web avec le framework python "flask" 
où l'utilisateur pourrait discuter avec un robot, "GrandPy Bot" et lui demander des informations sur le lieu de son choix.
Ce robot doit alors lui retourner un ensemble d'informations à propos de ce lieu.
  
## 1.2 Description du parcours utilisateur
-------------------------------------------
L'utilisateur entre l'url de la page web correspondante au projet. Il arrive alors sur une page web contenant
une zone de chat et une zone où il peut écrire sa question. L'utilisateur introduit alors sa question et appuie sur le
bouton "envoyer". Il y a alors 3 possibilités:
- Le robot a compris la question et lui affiche les informations venant des différentes API utilisées.
- Le robot a compris la question mais les API ne renvoient pas les informations attendues. Le robot répond à l'utilisateur
  qu'il n'a rien trouvé sur le lieu en question
- Le robot n'a pas compris la question et demande à l'utilisateur d'être plus clair sur le lieu demandé


## 1.3 Fonctionnalités du projet
---------------------------------
- Interactions en AJAX : l'utilisateur envoie sa question en appuyant sur entrée et la réponse s'affiche directement dans l'écran,
  sans recharger la page.
- Utilisation de l'API de HERE et celle de Media Wiki.
- Rien n'est sauvegardé. Si l'utilisateur charge de nouveau la page, tout l'historique est perdu.

# 2 Prérequis pour l'utilisation du projet
-------------------------------------------

## 2.1 Langages utilisés
-------------------------
le langage de programmation utilisé dans ce projet est python.
Les langages pour la partie "web" sont le HTML, le CSS et le javascript   
Lien pour télécharger python : https://www.python.org/downloads/  
version de python lors du développement : 3.8


## 2.2 librairies utilisées:
-----------------------------
Vous pouvez retrouver l'ensemble des librairies utilisées pour ce projet dans le
fichier requirements.txt et tout installer directement via ce fichier grâce à une
commande pip.

## 2.3 Utilisation des clefs d'API
----------------------------------
Pour des raisons de sécurité, les clefs de l'API HERE doivent être stockées dans des
variables d'environnement appelé "HERE_ID" et "HERE_CODE". 
  
# 3 Structure du projet
-------------------------
Il est à noter que le code associé au projet respecte la PEP8  
Le projet est subdivisé de la façon suivante:
- dossier "app" : contient le code source du projet
- dossier "tests" : contient les tests liés au projet.
- fichier ".flaskenv" : permet de configurer une variable d'environnement nécessaire pour le bon fonctionnement de flask
- fichier ".gitignore" : permet à certains fichiers et dossiers de ne pas être "suivi" par git
- fichier "grandpy.py" : fichier contenant le point de départ de l'application
- fichier "README.md" : ce fichier
- fichier "requirements.txt" : contient les différentes librairies utilisées par le projet
- fichier "Procfile" : Ce fichier est nécessaire lors du lancement du serveur.
Analysons maintenant le dossier "app"

## 3.1 Dossier "app"
----------------------
Comme indiqué précédemment, ce dossier contient tout le code et ressources liés au projet.
Analysons chaque dossier ou fichier de ce dossier "app".

### 3.1.1 Dossier "static"
-------------------------
Celui-ci contient les fichiers css, les fichiers javascript ainsi que les images utilisées dans ce projet.
Il contient aussi le fichier json contenant les stopwords français.

### 3.1.2 Dossier templates
----------------
Celui-ci contient les différents templates du projet

### 3.1.3 Dossier utils
------------------------
Ce dossier contient les fichiers : apiuser.py et parser.py.
Analysons ces deux fichier.

#### 3.1.3.1 Fichier apiuser.py
-------------------------------
Ce fichier contient la classe "ApiUser". Cette classe a la responsabilité de recolter les informations de l'API
de media wiki ainsi que de l'API HERE.

#### 3.1.3.2 Fichier parser.py
------------------------------
Ce fichier contient la classe "Parser". Cette classe a la responsabilité d'analyser la question de l'utilisateur afin d'en
retirer les informations nécessaires.

### 3.1.4 Fichier grandpybot.py
-------------------------------
Ce fichier contient la classe "GrandpyBot". Cette classe a la responsabilité d'être "le chef d'orchestre" de l'analyse de la question et de la
collecte des données auprès des API.

### 3.1.5 Fichier routes.py
---------------------------
Ce fichier contient les différentes fonctions de vue de l'application

# 4 Informations complémentaires
----------------------------------

## 4.1. Acteurs
----------------
développeur = Geoffrey Remacle

## 4.2. Utilisation d'API
--------------------------
Le projet utilise l'API de géolocalisation "HERE"  
lien vers la documentation : https://developer.here.com/documentation 
Le projet utilise aussi l'API media wiki
lien vers la documentation : https://www.mediawiki.org/wiki/API:Main_page/fr

## 4.3. Langue du code
-----------------------
les noms de classes, fonctions, variables, les commentaires, les docstrings,... sont écrits en anglais.

## 4.4 Déploiement
------------------
L'application est déployé avec Heroku
vous pouvez retrouvé l'application à cette adresse : https://geoffrey-remacle-grandpybot.herokuapp.com/

## 4.4. Liens
--------------
Lien vers le repository github:  
https://github.com/GeoffreyRe/Project_7
  
Lien vers la page de la formation "Développeur d'Application python":  
https://openclassrooms.com/fr/paths/68-developpeur-dapplication-python   


