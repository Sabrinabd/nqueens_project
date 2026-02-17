#!/usr/bin/env python3
"""
Script de benchmark pour le projet N-Queens
Compare automatiquement toutes les variantes de modélisation
"""

import subprocess
import json
import csv
import time
import os
from pathlib import Path
from datetime import datetime

# Configuration
MODELS_DIR = Path("models")
DATA_DIR = Path("data")
RESULTS_DIR = Path("results")
TIMEOUT = 300  # 5 minutes max par instance

# Tailles de N à tester
N_VALUES = [8, 10, 12, 15, 20, 25, 30, 40, 50]

# Liste des modèles à tester
MODELS = [
    ("01_naive.mzn", "Naïf (contraintes binaires)"),
    ("02_global.mzn", "Contraintes globales"),
    ("03_ff_min.mzn", "First-Fail + Min"),
    ("04_ff_max.mzn", "First-Fail + Max"),
    ("05_ff_split.mzn", "First-Fail + Split"),
    ("06_input_order.mzn", "Input Order"),
    ("07_smallest.mzn", "Smallest"),
    ("08_dom_w_deg.mzn", "Dom/Wdeg"),
    ("09_symmetry_basic.mzn", "Symétrie basique"),
    ("10_symmetry_advanced.mzn", "Symétrie avancée"),
    ("11_redundant.mzn", "Contraintes redondantes"),
    ("12_bounds.mzn", "Propagation bounds"),
    ("13_random.mzn", "Random"),
    ("14_combined_optimal.mzn", "Combiné optimal"),
    ("15_max_regret.mzn", "Max Regret"),
]

def run_minizinc(model_path, data_path, timeout=TIMEOUT):
    """
    Lance MiniZinc et récupère les statistiques
    """
    cmd = [
        "minizinc",
        "--solver", "gecode",
        "--statistics",
        "--time-limit", str(timeout * 1000),  # en millisecondes
        str(model_path),
        str(data_path)
    ]
    
    try:
        start_time = time.time()
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        elapsed_time = time.time() - start_time
        
        # Parser la sortie pour extraire les statistiques
        stats = {
            'status': 'UNKNOWN',
            'time': elapsed_time,
            'nodes': None,
            'failures': None,
            'propagations': None,
            'solutions': 0
        }
        
        # Chercher les statistiques dans stderr (MiniZinc les met là)
        stderr_lines = result.stdout.split('\n')
        for line in stderr_lines:
            if 'nodes' in line.lower():
                try:
                    stats['nodes'] = int(line.split('=')[1].strip())
                except:
                    pass
            elif 'failures' in line.lower() or 'fails' in line.lower():
                try:
                    stats['failures'] = int(line.split('=')[1].strip())
                except:
                    pass
            elif 'propagations' in line.lower() or 'propagates' in line.lower():
                try:
                    stats['propagations'] = int(line.split('=')[1].strip())
                except:
                    pass
            elif 'solveTime' in line:
                try:
                    stats['time'] = float(line.split('=')[1].strip().replace('ms', '')) 
                except:
                    pass
        
        # Vérifier si une solution a été trouvée
        if result.returncode == 0 and 'Q = ' in result.stdout:
            stats['status'] = 'SAT'
            stats['solutions'] = result.stdout.count('Q = ')
        elif result.returncode == 0:
            stats['status'] = 'UNSAT'
        elif 'TIMEOUT' in result.stderr or elapsed_time >= timeout - 1:
            stats['status'] = 'TIMEOUT'
        else:
            stats['status'] = 'ERROR'
        
        return stats
        
    except subprocess.TimeoutExpired:
        return {
            'status': 'TIMEOUT',
            'time': timeout,
            'nodes': None,
            'failures': None,
            'propagations': None,
            'solutions': 0
        }
    except Exception as e:
        print(f"Erreur: {e}")
        return {
            'status': 'ERROR',
            'time': None,
            'nodes': None,
            'failures': None,
            'propagations': None,
            'solutions': 0
        }

def main():
    """
    Fonction principale : lance tous les benchmarks
    """
    # Créer le dossier de résultats
    RESULTS_DIR.mkdir(exist_ok=True)
    
    # Nom du fichier de résultats avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = RESULTS_DIR / f"benchmark_{timestamp}.csv"
    
    print("=" * 80)
    print("BENCHMARK N-QUEENS - PROJET PROGRAMMATION PAR CONTRAINTES")
    print("=" * 80)
    print(f"\nNombre de modèles: {len(MODELS)}")
    print(f"Tailles testées: {N_VALUES}")
    print(f"Timeout par instance: {TIMEOUT}s")
    print(f"Total d'exécutions: {len(MODELS) * len(N_VALUES)}")
    print(f"\nRésultats sauvegardés dans: {results_file}")
    print("=" * 80)
    print()
    
    # Ouvrir le fichier CSV
    with open(results_file, 'w', newline='') as csvfile:
        fieldnames = [
            'Model', 'Description', 'N', 'Status', 
            'Time(s)', 'Nodes', 'Failures', 'Propagations', 'Solutions'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Compteur de progression
        total = len(MODELS) * len(N_VALUES)
        current = 0
        
        # Tester chaque combinaison
        for model_file, description in MODELS:
            model_path = MODELS_DIR / model_file
            
            if not model_path.exists():
                print(f"Modèle non trouvé: {model_file}")
                continue
            
            for n in N_VALUES:
                current += 1
                data_path = DATA_DIR / f"n{n}.dzn"
                
                if not data_path.exists():
                    print(f" Fichier de données non trouvé: n{n}.dzn")
                    continue
                
                print(f"[{current}/{total}] {model_file:30s} N={n:3d} ... ", end='', flush=True)
                
                # Lancer le benchmark
                stats = run_minizinc(model_path, data_path)
                
                # Afficher le résultat
                if stats['status'] == 'SAT':
                    time_str = f"{stats['time']:.8f}s" if stats['time'] else "N/A"
                    nodes_str = f"{stats['nodes']:,}" if stats['nodes'] else "N/A"
                    print(f"✓ {stats['status']:8s} {time_str:>10s} {nodes_str:>12s} nœuds")
                elif stats['status'] == 'TIMEOUT':
                    print(f"⏱  TIMEOUT (>{TIMEOUT}s)")
                else:
                    print(f"✗ {stats['status']}")
                
                # Écrire dans le CSV
                writer.writerow({
                    'Model': model_file,
                    'Description': description,
                    'N': n,
                    'Status': stats['status'],
                    'Time(s)': f"{stats['time']:.8f}" if stats['time'] is not None else '',
                    'Nodes': stats['nodes'] if stats['nodes'] is not None else '',
                    'Failures': stats['failures'] if stats['failures'] is not None else '',
                    'Propagations': stats['propagations'] if stats['propagations'] is not None else '',
                    'Solutions': stats['solutions']
                })
                
                # Flush pour voir les résultats en temps réel
                csvfile.flush()
    
    print()
    print("=" * 80)
    print("BENCHMARK TERMINÉ!")
    print(f"Résultats disponibles dans: {results_file}")
    print("=" * 80)
    
    # Générer un résumé
    print("\n RÉSUMÉ RAPIDE:\n")
    generate_summary(results_file)

def generate_summary(results_file):
    """
    Génère un résumé des résultats
    """
    # Lire le CSV
    with open(results_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    
    # Trouver le meilleur modèle pour chaque N
    print("Meilleurs modèles par taille:")
    print("-" * 60)
    
    for n in N_VALUES:
        n_rows = [r for r in rows if r['N'] == str(n) and r['Status'] == 'SAT' and r['Time(s)']]
        if n_rows:
            best = min(n_rows, key=lambda x: float(x['Time(s)']))
            print(f"N={n:3d}: {best['Description']:30s} ({best['Time(s)']:>8s}s)")
        else:
            print(f"N={n:3d}: Aucune solution trouvée")
    
    print()
    
    # Statistiques globales par modèle
    print("Performance moyenne par modèle:")
    print("-" * 60)
    
    model_stats = {}
    for model_file, description in MODELS:
        model_rows = [r for r in rows if r['Model'] == model_file and r['Status'] == 'SAT' and r['Time(s)']]
        if model_rows:
            avg_time = sum(float(r['Time(s)']) for r in model_rows) / len(model_rows)
            solved = len(model_rows)
            total = len([r for r in rows if r['Model'] == model_file])
            model_stats[description] = (avg_time, solved, total)
    
    # Trier par temps moyen
    sorted_models = sorted(model_stats.items(), key=lambda x: x[1][0])
    
    for desc, (avg_time, solved, total) in sorted_models:
        print(f"{desc:30s}: {avg_time:7.8f}s avg, {solved}/{total} résolus")

if __name__ == "__main__":
    main()
