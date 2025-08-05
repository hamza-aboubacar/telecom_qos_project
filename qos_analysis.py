# -*- coding: utf-8 -*-
"""
Script pour l'analyse des données de performance réseau (QoS).

Ce script charge les données générées, effectue une analyse exploratoire,
identifie les zones ou périodes problématiques et sauvegarde les résultats
d'analyse pour l'application Flask.
"""

import pandas as pd
import numpy as np
import logging
import os

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def perform_qos_analysis():
    """
    Charge les données QoS, effectue l'analyse et sauvegarde les résumés.
    """
    logging.info("Démarrage de l'analyse QoS...")

    data_file = 'qos_network_data.csv'
    if not os.path.exists(data_file):
        logging.error(f"Erreur : Le fichier de données '{data_file}' est introuvable.")
        logging.error("Veuillez d'abord exécuter le script 'qos-data-generation.py'.")
        return

    try:
        df = pd.read_csv(data_file)
        logging.info("Jeu de données QoS chargé avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors du chargement des données : {e}")
        return

    # --- Prétraitement des données ---
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    # Gérer les valeurs manquantes (imputation par la médiane pour cet exemple)
    for col in ['latency_ms', 'download_speed_mbps', 'upload_speed_mbps', 'call_drop_rate_percent', 'signal_strength_dbm']:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            logging.info(f"Valeurs manquantes dans '{col}' remplies avec la médiane : {median_val}")

    # --- Analyse des métriques clés ---

    # 1. Résumé global des métriques
    global_summary = df[['latency_ms', 'download_speed_mbps', 'upload_speed_mbps', 'call_drop_rate_percent', 'signal_strength_dbm']].mean().round(2)
    logging.info(f"Résumé global des métriques:\n{global_summary}")

    # 2. Analyse par Cell ID (identification des tours problématiques)
    # Calculer les métriques moyennes par tour cellulaire
    cell_qos_summary = df.groupby('cell_id').agg(
        avg_latency=('latency_ms', 'mean'),
        avg_download_speed=('download_speed_mbps', 'mean'),
        avg_upload_speed=('upload_speed_mbps', 'mean'),
        avg_call_drop_rate=('call_drop_rate_percent', 'mean'),
        avg_signal_strength=('signal_strength_dbm', 'mean'),
        num_records=('cell_id', 'count')
    ).round(2)

    # Identifier les cellules problématiques (ex: latence élevée, faible débit, taux de chute élevé)
    # Définir des seuils simples pour l'exemple
    problem_thresholds = {
        'avg_latency': 100, # ms
        'avg_download_speed': 20, # Mbps
        'avg_call_drop_rate': 3 # %
    }

    problematic_cells = cell_qos_summary[
        (cell_qos_summary['avg_latency'] > problem_thresholds['avg_latency']) |
        (cell_qos_summary['avg_download_speed'] < problem_thresholds['avg_download_speed']) |
        (cell_qos_summary['avg_call_drop_rate'] > problem_thresholds['avg_call_drop_rate'])
    ].sort_values(by='avg_call_drop_rate', ascending=False) # Trier par le taux de chute pour voir les pires

    logging.info(f"Cellules problématiques identifiées ({len(problematic_cells)}):\n{problematic_cells.head()}")

    # 3. Analyse temporelle (ex: moyenne horaire)
    hourly_avg_qos = df.resample('H').mean(numeric_only=True).round(2)
    # Calculer la moyenne par heure de la journée pour identifier les pics
    qos_by_hour_of_day = df.groupby(df.index.hour).mean(numeric_only=True).round(2)
    qos_by_hour_of_day.index.name = 'hour_of_day'
    logging.info(f"QoS moyenne par heure de la journée:\n{qos_by_hour_of_day.head()}")

    # --- Sauvegarde des résultats d'analyse ---
    # Sauvegarder les résumés pour l'application Flask
    global_summary.to_json('qos_global_summary.json')
    problematic_cells.to_csv('qos_problematic_cells.csv')
    qos_by_hour_of_day.to_csv('qos_hourly_trends.csv')

    logging.info("Analyse QoS terminée. Résultats sauvegardés.")

if __name__ == '__main__':
    perform_qos_analysis()
