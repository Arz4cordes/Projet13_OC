## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## Conteneurisation et déploiement

### Description du pipeline
- Circle CI est utilisé comme pipeline, les différents jobs sont décrits dans le fichier config.yml du dossier .circleci
- 1) L'application est testée à chaque commit sur une branche (commande pytest puis linting avec flake8)
- 2) L'application est envoyée sur DockerHub à chaque push sur github de la branche master , à condition que les tests passent.
  L'image Docker est construite à l'aide du fichier Dockerfile:
  le conteneur permet d'installer Python, de copier les différents du projet,
  d'installer les différentes bibliothèques Python listées dans le fichier requirements.txt du projet,
  et de lancer l'application à l'aide d'une commande utilisant gunicorn
- 3) L'image Docker est déployée et lancée sur Heroku à chaque push sur github de la branche master, à condition que les tests passent
  et que l'envoi sur le Dockerhub ait été réalisé sans problème:
  Heroku cli est installé, la connexion à Heroku se fait avec un Token,
  et enfin le conteneur est poussé puis lancé dans l'espace web préalablement crée (application Heroku ic-lettings-site-1974)

### Démarche pour effectuer le déploiement:
- Un déploiement est tenté à chaque push sur github de la branche master (3e job décrit dans le workflow de circleci):
le déploiemement se fait sur un serveur Heroku dans un conteneur de l'application nommée oc-lettings-site-1974.
- 1) Si l'application oc-lettings-site-1974 existe bien sur Heroku et est déjà correctement configurée, passez à l'étape 2 suivante.
  Si l'application a été supprimée ou que les variables d'environnement ENV, SECRET_KEY ou SENTRY_SDK sont invalides, exécutez les actions suivantes:
    a) Connectez vous à Heroku et créer à nouveau l'application oc-lettings-site-1974
    b) Allez dans les réglages de l'application oc-lettings-site-1974 nouvellement crée sur Heroku et configurez les variables d'environnement suivantes:
        ENV=PRODUCTION
        SECRET_KEY=votre_nouvelle_secret_key
        SENTRY_SDK=https://ddcaa9424a664d729b027d1aa7a3d1e2@o1232307.ingest.sentry.io/6380304
    c) Récupérez la clé pour se connecter à Heroku, connectez vous à circleci et configurez dans circleci la variable d'environnement suivante pour le projet suivi;
        HEROKU_TOKEN: votre_heroku_api_key
    Tout est maintenant prêt pour lancer le déploiement via le pipeline circleci
  - 2) Nouveau déploiement:
  Après avoir fait un commit sur la branche master du projet en local, tapez la commande git push OCP13 master pour envoyer sur le dépot distant github
  le projet mis à jour: cette action va déclencher une nouvelle série de tests, un envoi d'une image Docker sur Dockerhub, et un déploiement sur Heroku
  de l'application mise à jour.
  Pour suivre le bon déroulement des 3 actions précédentes, connectez vous à circleci, et sélectionnez le projet qui est lié au dépot github de ce projet:
  les 3 jobs appaissent, et vous pouvez cliquer dessus pour voir le détail de chaque job. Si tout se passe bien, une pastille verte apparait
  devant le job correctement réalisé. Sinon, en cas de problème, cliquez sur le job associé à une pastille rouge
  et vous aurez l'affichage des logs pour identifier un problème.
  - 3) suite...