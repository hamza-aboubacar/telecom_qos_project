# -*- coding: utf-8 -*-
"""
Application Web Flask pour l'Analyse de la Qualité de Service Réseau (QoS).

Cette application permet de :
1. Afficher un tableau de bord récapitulatif des métriques QoS globales.
2. Identifier et lister les tours cellulaires (Cell IDs) problématiques.
3. Montrer les tendances QoS par heure de la journée.
"""

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import os
import logging
import json # Pour charger le JSON du résumé global

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'qos_telecom_app_secret_key')

# Fichiers de résultats d'analyse (générés par qos_analysis.py)
GLOBAL_SUMMARY_FILE = 'qos_global_summary.json'
PROBLEMATIC_CELLS_FILE = 'qos_problematic_cells.csv'
HOURLY_TRENDS_FILE = 'qos_hourly_trends.csv'

# --- Chargement des données d'analyse ---
global_qos_summary = {}
problematic_cells_df = pd.DataFrame()
hourly_trends_df = pd.DataFrame()

try:
    if os.path.exists(GLOBAL_SUMMARY_FILE):
        with open(GLOBAL_SUMMARY_FILE, 'r') as f:
            global_qos_summary = json.load(f)
        logging.info("Résumé global QoS chargé.")
    else:
        logging.warning(f"Fichier '{GLOBAL_SUMMARY_FILE}' non trouvé. Exécutez 'qos_analysis.py'.")

    if os.path.exists(PROBLEMATIC_CELLS_FILE):
        problematic_cells_df = pd.read_csv(PROBLEMATIC_CELLS_FILE)
        logging.info("Cellules problématiques chargées.")
    else:
        logging.warning(f"Fichier '{PROBLEMATIC_CELLS_FILE}' non trouvé. Exécutez 'qos_analysis.py'.")

    if os.path.exists(HOURLY_TRENDS_FILE):
        hourly_trends_df = pd.read_csv(HOURLY_TRENDS_FILE, index_col='hour_of_day')
        logging.info("Tendances horaires QoS chargées.")
    else:
        logging.warning(f"Fichier '{HOURLY_TRENDS_FILE}' non trouvé. Exécutez 'qos_analysis.py'.")

except Exception as e:
    logging.error(f"Erreur lors du chargement des fichiers d'analyse : {e}", exc_info=True)
    # L'application peut continuer à fonctionner avec des données vides, mais affichera un avertissement.

# --- Routes de l'application ---

@app.route('/')
def index():
    """
    Page d'accueil du projet QoS.
    """
    return render_template('qos_index.html')

@app.route('/dashboard')
def dashboard():
    """
    Affiche le tableau de bord QoS avec les métriques globales,
    les cellules problématiques et les tendances horaires.
    """
    # Préparer les données pour le rendu HTML
    global_summary_items = global_qos_summary.items() if global_qos_summary else []
    
    # Limiter l'affichage des cellules problématiques et les convertir en HTML
    problematic_cells_html = problematic_cells_df.head(10).to_html(classes='table-auto w-full text-left whitespace-no-wrap', index=True, float_format='%.2f')
    
    # CORRECTION ICI : Utiliser les noms de colonnes corrects du DataFrame hourly_trends_df
    # Les colonnes sont les noms des métriques originales après la moyenne par heure.
    # Assurez-vous que cette chaîne est complète et sur une seule ligne dans votre fichier.
    hourly_trends_html = hourly_trends_df[['latency_ms', 'download_speed_mbps', 'call_drop_rate_percent']].to_html(classes='table-auto w-full text-left whitespace-no-wrap', index=True, float_format='%.2f')

    return render_template('qos_dashboard.html',
                           global_summary=global_summary_items,
                           problematic_cells_table=problematic_cells_html,
                           hourly_trends_table=hourly_trends_html,
                           num_problematic_cells=len(problematic_cells_df))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
