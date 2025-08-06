Projet : Analyse de la Qualité de Service (QoS) Réseau Télécom et Optimisation
📝 Description du Projet
Ce projet complet se concentre sur l'analyse de la Qualité de Service (QoS) des réseaux de télécommunications. Il vise à identifier les zones géographiques et les périodes temporelles où la performance du réseau est dégradée, afin de permettre aux opérateurs de prendre des décisions éclairées pour l'optimisation et l'amélioration de l'expérience client.

Le projet inclut la génération de données synthétiques de performance réseau, un script d'analyse pour extraire des insights clés, et une application web Flask simple pour visualiser les résultats de l'analyse.

🎯 Problème Métier Addréssé
Les problèmes de qualité de service (latence élevée, débits faibles, coupures d'appels) sont une source majeure d'insatisfaction client et peuvent entraîner un désabonnement. Ce projet aide à répondre aux questions suivantes :

Où et quand la qualité de service est-elle la plus faible ?

Quelles sont les tours cellulaires (Cell IDs) qui rencontrent le plus de problèmes ?

Y a-t-il des tendances horaires dans la dégradation de la QoS ?

✨ Fonctionnalités
Génération de Données Synthétiques : Crée un jeu de données réaliste de métriques de performance réseau (latence, débits, taux de chute, force du signal) avec des variations temporelles et géographiques, incluant des anomalies simulées.

Analyse de la Qualité de Service (QoS) :

Calcul des métriques QoS globales moyennes.

Identification des tours cellulaires problématiques basées sur des seuils de performance.

Analyse des tendances QoS par heure de la journée.

Application Web Flask :

Tableau de Bord Récapitulatif : Affiche les KPIs QoS globaux.

Liste des Cellules Problématiques : Présente un aperçu des tours cellulaires sous-performantes.

Tendances Horaires : Visualise l'évolution des métriques QoS au cours d'une journée type.

💻 Technologies et Dépendances
Python 3.x

Framework Web : Flask

Data Science : pandas, numpy

Sérialisation : joblib (non utilisé directement dans app.py mais utile pour d'autres projets ML)

Serveur WSGI (pour le déploiement) : gunicorn

Frontend : HTML, CSS (avec Tailwind CSS via CDN)

Versionnement : Git, GitHub

📁 Structure du Projet
telecom_qos_project/
├── app.py                         # Application web Flask
├── qos-data-generation.py         # Script de génération de données QoS
├── qos_analysis.py                # Script d'analyse des données QoS
├── qos_network_data.csv           # Jeu de données QoS généré (sera créé)
├── qos_global_summary.json        # Résumé des métriques globales (sera créé)
├── qos_problematic_cells.csv      # Liste des cellules problématiques (sera créé)
├── qos_hourly_trends.csv          # Tendances horaires QoS (sera créé)
└── templates/                     # Dossier des templates HTML
    ├── qos_index.html
    └── qos_dashboard.html

🚀 Étapes de Réalisation du Projet (De A à Z)
Suivez ces étapes pour mettre en place et exécuter le projet sur votre machine locale.

1. Génération des Données de Qualité de Service
Ce script crée un jeu de données synthétique de performance réseau avec des métriques horodatées et géolocalisées.

Fichier : qos-data-generation.py

Objectif : Créer le fichier qos_network_data.csv.

Comment l'exécuter :

python qos-data-generation.py

Output attendu : Un fichier qos_network_data.csv sera généré à la racine de votre projet, contenant 10 000 lignes de données QoS fictives.

2. Analyse des Données de Qualité de Service
Ce script charge les données générées, effectue un prétraitement, calcule des métriques agrégées et identifie les zones/périodes problématiques.

Fichier : qos_analysis.py

Objectif :

Charger qos_network_data.csv.

Gérer les valeurs manquantes (imputation par la médiane).

Calculer les moyennes globales des métriques QoS.

Identifier les tours cellulaires problématiques basées sur des seuils prédéfinis.

Calculer les tendances horaires des métriques QoS.

Sauvegarder les résultats dans qos_global_summary.json, qos_problematic_cells.csv, et qos_hourly_trends.csv.

Comment l'exécuter :

python qos_analysis.py

Output attendu : Trois fichiers de résultats d'analyse (.json et .csv) seront créés à la racine de votre projet.

3. Lancement de l'Application Web Flask
Cette application web charge les résultats de l'analyse et les affiche via un tableau de bord interactif.

Fichier : app.py

Objectif :

Charger les fichiers de résultats générés par qos_analysis.py.

Servir les pages web pour le tableau de bord QoS.

Afficher les KPIs globaux, les tours problématiques et les tendances horaires.

Comment l'exécuter :

python app.py

Output attendu : L'application démarrera et sera accessible via votre navigateur web.

📊 Explication de l'Output (Résultats)
Le tableau de bord QoS (/dashboard) présente les insights clés de l'analyse :

1. Résumé Global des Métriques QoS
Description : Affiche les moyennes générales des indicateurs de performance clés (latence, débits, taux de chute d'appels, force du signal) sur l'ensemble des données.

Utilité : Fournit une vue d'ensemble rapide de la santé globale du réseau.

2. Tours Cellulaires Problématiques
Description : Présente un tableau des tours cellulaires qui affichent des performances inférieures aux seuils définis (ex: latence trop élevée, débit trop faible, taux de chute trop élevé). Les 10 premières sont affichées.

Utilité : Permet d'identifier rapidement les points chauds du réseau nécessitant une intervention ou une investigation plus approfondie.

3. Tendances QoS par Heure de la Journée
Description : Affiche les moyennes des métriques QoS (latence, débit de téléchargement, taux de chute) pour chaque heure de la journée.

Utilité : Révèle les périodes de la journée où le réseau est le plus sollicité ou rencontre le plus de problèmes, aidant à planifier les maintenances ou les renforcements de capacité.

🚀 Installation et Démarrage Local
Pour faire tourner ce projet sur votre machine :

Cloner le dépôt :

git clone https://github.com/votre-nom-utilisateur/telecom_qos_project.git
cd telecom_qos_project

Créer et activer un environnement virtuel (recommandé) :

python -m venv venv_qos_telecom
# Sur macOS/Linux:
source venv_qos_telecom/bin/activate
# Sur Windows:
venv_qos_telecom\Scripts\activate

Installer les dépendances :

pip install pandas numpy Flask gunicorn

Générer les données (Étape 1) :

python qos-data-generation.py

Effectuer l'analyse (Étape 2) :

python qos_analysis.py

Lancer l'application Flask (Étape 3) :

python app.py

L'application sera disponible à l'adresse http://127.0.0.1:5000.

☁️ Déploiement sur Heroku
Pour déployer votre application sur Heroku, suivez ces étapes (assurez-vous d'avoir installé le Heroku CLI et d'être connecté) :

Assurez-vous que requirements.txt et Procfile sont à jour :

requirements.txt doit contenir toutes les dépendances listées ci-dessus (généré par pip freeze).

Procfile (à la racine du projet, sans extension) doit contenir : web: gunicorn app:app.

Définir la clé secrète Flask sur Heroku :

heroku config:set SECRET_KEY='UNE_CHAINE_DE_CARACTERES_ALEATOIRE_ET_LONGUE'

Créer l'application Heroku :

heroku create votre-nom-app-qos-telecom

Déployer le code :

git push heroku main

Ouvrir l'application :

heroku open

Votre application sera accessible via l'URL Heroku générée.

✍️ Auteur
Aboubacar Halidou Hamza

Votre Profil GitHub

Votre Profil LinkedIn

📄 Licence
Ce projet est sous licence MIT.
