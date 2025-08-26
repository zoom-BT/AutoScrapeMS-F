# AutoScrapeBot - Guide de Lancement et Dépannage

## 1. Description Détaillée

**AutoScrapeBot** est une application web développée avec le framework **Django**, conçue pour automatiser le processus de collecte de données (web scraping). Elle fournit une interface utilisateur simple permettant de lancer des tâches de scraping complexes qui s'exécutent en arrière-plan, sans bloquer l'utilisateur.

Le cœur de l'application repose sur la bibliothèque **Playwright** pour piloter un navigateur web, ce qui lui permet d'extraire des informations de sites web modernes et dynamiques (rendus en JavaScript). Les données collectées sont ensuite stockées dans une base de données **MongoDB** pour une flexibilité maximale.

L'objectif principal de ce projet est de fournir un outil stable et réutilisable pour le scraping, tout en y ajoutant une fonctionnalité innovante de **relance automatique contrôlée par le client**. L'utilisateur peut initier une session de scraping qui se répétera ensuite automatiquement à un intervalle défini, sans nécessiter de configuration complexe côté serveur.

---

## 2. Fonctionnalités Clés

* **Scraping Manuel :** Lancez une session de scraping à la demande en fournissant une ou plusieurs URLs.
* **Relance Automatique Côté Client :** Après le premier lancement, un minuteur JavaScript (`setTimeout`) prend le relais pour relancer le scraping à intervalles réguliers, tant que l'onglet reste ouvert.
* **Persistance de Session :** Le script utilise le `sessionStorage` du navigateur pour se souvenir des URLs et de l'état de la relance, même après le rechargement de la page.
* **Interface Utilisateur Réactive :** Le formulaire informe l'utilisateur du statut du scraping (en cours, en attente, terminé) grâce à des indicateurs visuels (spinner) et des messages de statut.
* **Stockage NoSQL :** Toutes les données extraites sont sauvegardées dans une base de données MongoDB, gérée via le connecteur `djongo`.

---

## 3. Prérequis

Avant de lancer l'application, assurez-vous d'avoir les logiciels suivants installés sur votre machine :

* **Python** (version 3.10 ou supérieure)
* **MongoDB** (la base de données NoSQL)
* **MongoDB Compass** (outil graphique pour visualiser les données, recommandé)

---

## 4. Processus de Lancement (depuis un fichier Zip)

Suivez ces étapes dans l'ordre pour une installation propre et fonctionnelle.

#### Étape 1 : Dézipper le fichier

Décompressez le fichier `.zip` du projet dans le dossier de votre choix.

#### Étape 2 : Préparer l'environnement

Ouvrez un terminal (PowerShell ou CMD sur Windows) et naviguez jusqu'au dossier racine du projet (celui qui contient `manage.py`).
```powershell
# Exemple de navigation
cd C:\Chemin\Vers\Votre\Projet\ScrapeBot
````

#### Étape 3 : Créer et Activer l'Environnement Virtuel

Il est crucial de travailler dans un environnement isolé.

```powershell
# Créer l'environnement
python -m venv .venv

# Activer l'environnement
.\.venv\Scripts\Activate.ps1
```

Votre terminal doit maintenant afficher `(.venv)` au début de la ligne.

#### Étape 4 : Installer les Dépendances

Le projet est fourni avec un fichier `requirements.txt` qui liste toutes les librairies nécessaires.

```powershell
pip install -r requirements.txt
```

#### Étape 5 : Installer les Navigateurs pour Playwright

Playwright a besoin de télécharger les navigateurs qu'il contrôle.

```powershell
# Installe le navigateur nécessaire (ex: Firefox)
playwright install firefox
```

#### Étape 6 : Lancer l'Application

Une fois toutes les dépendances installées, lancez le serveur de développement Django.

```powershell
python manage.py runserver
```

L'application sera accessible à l'adresse **http://127.0.0.1:8000/**.

-----

## 5\. Erreurs à Éviter et Corrections

  * **Erreur :** `ModuleNotFoundError: No module named 'django'` (ou autre)

      * **Cause :** Vous avez oublié d'activer l'environnement virtuel (`.venv`).
      * **Solution :** Arrêtez le serveur (`CTRL+C`), lancez `.\.venv\Scripts\Activate.ps1`, puis relancez le serveur.

  * **Erreur :** `Executable doesn't exist at ...` lors du scraping

      * **Cause :** Les navigateurs de Playwright ne sont pas installés.
      * **Solution :** Arrêtez le serveur et lancez la commande `playwright install`.

  * **Erreur :** `djongo ... requires sqlparse==0.2.4, but you have ...` (Conflit de versions)

      * **Cause :** Une installation a mis à jour un paquet, créant une incompatibilité.
      * **Solution :** Supprimez le dossier `.venv`, recréez-le et réinstallez les dépendances avec `pip install -r requirements.txt`.

  * **Erreur :** `NotImplementedError: Database objects do not implement truth value testing...`

      * **Cause :** La version de `pymongo` est trop récente pour `djongo`.
      * **Solution :** Forcez l'installation d'une version compatible : `pip install pymongo==3.12.3`.

-----

**Balbino Tchoutzine** *Stagiaire Développeur, Megasoft*

