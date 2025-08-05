# -*- coding: utf-8 -*-
"""
Script pour générer un jeu de données synthétique de performance réseau (QoS).

Ce script crée un fichier CSV avec des métriques typiques de qualité de service réseau,
incluant des données temporelles et géographiques.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import logging

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_qos_data(num_records=10000):
    """
    Génère un DataFrame de données de performance réseau et l'enregistre en CSV.

    Args:
        num_records (int): Le nombre d'enregistrements (points de données) à générer.
    """
    logging.info(f"Début de la génération de données QoS pour {num_records} enregistrements...")

    # Plage de temps pour les données
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    time_stamps = [start_time + timedelta(minutes=i) for i in range(num_records)]

    # Cell IDs (identifiants de tours cellulaires)
    cell_ids = [f'CELL_{i:03d}' for i in range(1, 51)] # 50 tours différentes

    # Localisations des tours (simulées pour la diversité géographique)
    cell_locations = {
        f'CELL_{i:03d}': (random.uniform(48.5, 49.5), random.uniform(2.0, 3.0)) # Région de Paris
        for i in range(1, 26)
    }
    cell_locations.update({
        f'CELL_{i:03d}': (random.uniform(43.0, 44.0), random.uniform(5.0, 6.0)) # Région de Marseille
        for i in range(26, 51)
    })

    # Générer des métriques de performance
    data = []
    for i in range(num_records):
        cell_id = random.choice(cell_ids)
        lat, lon = cell_locations[cell_id]

        # Métriques de base (avec un peu de bruit)
        latency = max(10, np.random.normal(50, 20)) # ms
        download_speed = max(1, np.random.normal(50, 15)) # Mbps
        upload_speed = max(1, np.random.normal(15, 5)) # Mbps
        call_drop_rate = max(0, min(10, np.random.normal(1, 2))) # %
        signal_strength = max(-110, np.random.normal(-70, 10)) # dBm

        # Introduire des "problèmes" aléatoires pour simuler des anomalies
        if random.random() < 0.05: # 5% de chance d'avoir une anomalie
            problem_type = random.choice(['High Latency', 'Low Speed', 'Call Drops'])
            if problem_type == 'High Latency':
                latency = max(100, np.random.normal(200, 50))
            elif problem_type == 'Low Speed':
                download_speed = max(0.5, np.random.normal(5, 2))
                upload_speed = max(0.2, np.random.normal(1, 0.5))
            elif problem_type == 'Call Drops':
                call_drop_rate = max(5, np.random.normal(15, 5))
            
            # Rendre le signal plus faible dans les zones à problèmes simulées
            if random.random() < 0.3: # 30% de chance que l'anomalie soit liée à un signal faible
                signal_strength = max(-120, np.random.normal(-95, 10))
            
            is_anomaly = 1
        else:
            is_anomaly = 0
            problem_type = 'Normal'

        # data.append({
        #     'timestamp': time_stamps[i],
        #     'cell_id': cell_id,
        #     'latitude': lat + random.uniform(-0.01, 0.01), # Petit bruit pour la variation
        #     'longitude': lon + random.uniform(-0.01, 0.01),
        #     'latency_ms': latency.round(2),
        #     'download_speed_mbps': download_speed.round(2),
        #     'upload_speed_mbps': upload_speed.round(2),
        #     'call_drop_rate_percent': call_drop_rate.round(2),
        #     'signal_strength_dbm': signal_strength.round(2),
        #     'is_anomaly': is_anomaly, # Pourrait être utilisé comme étiquette si on faisait de la classification
        #     'problem_type': problem_type # Type de problème simulé
        # })

        data.append({
    'timestamp': time_stamps[i],
    'cell_id': cell_id,
    'latitude': round(lat + random.uniform(-0.01, 0.01), 6),
    'longitude': round(lon + random.uniform(-0.01, 0.01), 6),
    'latency_ms': round(latency, 2),
    'download_speed_mbps': round(download_speed, 2),
    'upload_speed_mbps': round(upload_speed, 2),
    'call_drop_rate_percent': round(call_drop_rate, 2),
    'signal_strength_dbm': round(signal_strength, 2),
    'is_anomaly': is_anomaly,
    'problem_type': problem_type
})


    df = pd.DataFrame(data)

    # Introduire quelques valeurs nulles aléatoires pour tester la robustesse
    for col in ['latency_ms', 'download_speed_mbps', 'signal_strength_dbm']:
        num_nulls = int(num_records * 0.005) # 0.5% de nulls
        null_indices = np.random.choice(df.index, num_nulls, replace=False)
        df.loc[null_indices, col] = np.nan
        logging.info(f"Introduit {num_nulls} valeurs nulles dans '{col}'.")

    file_name = 'qos_network_data.csv'
    df.to_csv(file_name, index=False)
    logging.info(f"Fichier '{file_name}' généré avec succès. Il contient {len(df)} lignes.")
    logging.info("Utilisez ce fichier pour l'analyse QoS.")

if __name__ == '__main__':
    generate_qos_data()
