#!/usr/bin/env python3
"""
Script de visualisation des résultats du benchmark N-Queens
Génère des graphiques pour analyser les performances
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

def load_results(csv_file):
    """Charge les résultats depuis un fichier CSV"""
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def plot_time_comparison(results, output_dir):
    """Graphique comparatif des temps d'exécution"""
    # Organiser les données par modèle
    models = {}
    for row in results:
        if row['Status'] == 'SAT' and row['Time(s)']:
            model = row['Description']
            n = int(row['N'])
            time = float(row['Time(s)'])
            
            if model not in models:
                models[model] = {'N': [], 'Time': []}
            models[model]['N'].append(n)
            models[model]['Time'].append(time)
    
    # Créer le graphique
    plt.figure(figsize=(14, 8))
    
    for model, data in sorted(models.items()):
        # Trier par N
        sorted_indices = np.argsort(data['N'])
        n_values = np.array(data['N'])[sorted_indices]
        times = np.array(data['Time'])[sorted_indices]
        
        plt.plot(n_values, times, marker='o', label=model, linewidth=2, markersize=6)
    
    plt.xlabel('Taille N', fontsize=12)
    plt.ylabel('Temps (secondes)', fontsize=12)
    plt.title('Comparaison des temps d\'exécution - N-Queens', fontsize=14, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.tight_layout()
    
    output_file = output_dir / 'time_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Graphique sauvegardé: {output_file}")
    plt.close()

def plot_nodes_comparison(results, output_dir):
    """Graphique comparatif du nombre de nœuds explorés"""
    models = {}
    for row in results:
        if row['Status'] == 'SAT' and row['Nodes']:
            model = row['Description']
            n = int(row['N'])
            nodes = int(row['Nodes'])
            
            if model not in models:
                models[model] = {'N': [], 'Nodes': []}
            models[model]['N'].append(n)
            models[model]['Nodes'].append(nodes)
    
    plt.figure(figsize=(14, 8))
    
    for model, data in sorted(models.items()):
        sorted_indices = np.argsort(data['N'])
        n_values = np.array(data['N'])[sorted_indices]
        nodes = np.array(data['Nodes'])[sorted_indices]
        
        plt.plot(n_values, nodes, marker='s', label=model, linewidth=2, markersize=6)
    
    plt.xlabel('Taille N', fontsize=12)
    plt.ylabel('Nombre de nœuds explorés', fontsize=12)
    plt.title('Comparaison du nombre de nœuds - N-Queens', fontsize=14, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.tight_layout()
    
    output_file = output_dir / 'nodes_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Graphique sauvegardé: {output_file}")
    plt.close()

def plot_best_per_size(results, output_dir):
    """Graphique montrant le meilleur modèle pour chaque taille"""
    n_values = sorted(set(int(r['N']) for r in results))
    
    best_models = []
    best_times = []
    
    for n in n_values:
        n_results = [r for r in results if int(r['N']) == n and r['Status'] == 'SAT' and r['Time(s)']]
        if n_results:
            best = min(n_results, key=lambda x: float(x['Time(s)']))
            best_models.append(best['Description'][:20])  # Tronquer pour lisibilité
            best_times.append(float(best['Time(s)']))
        else:
            best_models.append('Aucun')
            best_times.append(0)
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(n_values)), best_times, color='steelblue', edgecolor='black')
    
    # Ajouter les noms des modèles sur les barres
    for i, (bar, model) in enumerate(zip(bars, best_models)):
        height = bar.get_height()
        if height > 0:
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    model, ha='center', va='bottom', rotation=45, fontsize=8)
    
    plt.xlabel('Taille N', fontsize=12)
    plt.ylabel('Temps (secondes)', fontsize=12)
    plt.title('Meilleur modèle par taille - N-Queens', fontsize=14, fontweight='bold')
    plt.xticks(range(len(n_values)), [f'N={n}' for n in n_values])
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    output_file = output_dir / 'best_per_size.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Graphique sauvegardé: {output_file}")
    plt.close()

def plot_success_rate(results, output_dir):
    """Graphique du taux de réussite par modèle"""
    models_stats = {}
    
    for row in results:
        model = row['Description']
        if model not in models_stats:
            models_stats[model] = {'total': 0, 'solved': 0}
        
        models_stats[model]['total'] += 1
        if row['Status'] == 'SAT':
            models_stats[model]['solved'] += 1
    
    # Calculer les taux
    models = []
    success_rates = []
    
    for model, stats in sorted(models_stats.items(), key=lambda x: x[1]['solved']/x[1]['total'], reverse=True):
        models.append(model[:25])  # Tronquer
        success_rates.append(100 * stats['solved'] / stats['total'])
    
    plt.figure(figsize=(12, 8))
    bars = plt.barh(range(len(models)), success_rates, color='forestgreen', edgecolor='black')
    
    # Ajouter les pourcentages
    for i, (bar, rate) in enumerate(zip(bars, success_rates)):
        plt.text(rate + 1, bar.get_y() + bar.get_height()/2,
                f'{rate:.1f}%', va='center', fontsize=9)
    
    plt.yticks(range(len(models)), models, fontsize=9)
    plt.xlabel('Taux de réussite (%)', fontsize=12)
    plt.title('Taux de réussite par modèle - N-Queens', fontsize=14, fontweight='bold')
    plt.xlim(0, 110)
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    
    output_file = output_dir / 'success_rate.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Graphique sauvegardé: {output_file}")
    plt.close()

def generate_summary_table(results, output_dir):
    """Génère un tableau récapitulatif en format texte"""
    output_file = output_dir / 'summary.txt'
    
    with open(output_file, 'w') as f:
        f.write("=" * 100 + "\n")
        f.write("RÉSUMÉ DES RÉSULTATS - PROJET N-QUEENS\n")
        f.write("=" * 100 + "\n\n")
        
        # Tableau par modèle
        f.write("PERFORMANCE MOYENNE PAR MODÈLE:\n")
        f.write("-" * 100 + "\n")
        f.write(f"{'Modèle':<35} {'Temps moy':<12} {'Nœuds moy':<15} {'Réussis/Total':<15} {'Taux':<10}\n")
        f.write("-" * 100 + "\n")
        
        models_data = {}
        for row in results:
            model = row['Description']
            if model not in models_data:
                models_data[model] = {'times': [], 'nodes': [], 'total': 0, 'solved': 0}
            
            models_data[model]['total'] += 1
            if row['Status'] == 'SAT':
                models_data[model]['solved'] += 1
                if row['Time(s)']:
                    models_data[model]['times'].append(float(row['Time(s)']))
                if row['Nodes']:
                    models_data[model]['nodes'].append(int(row['Nodes']))
        
        # Trier par temps moyen
        sorted_models = sorted(models_data.items(), 
                             key=lambda x: np.mean(x[1]['times']) if x[1]['times'] else float('inf'))
        
        for model, data in sorted_models:
            avg_time = np.mean(data['times']) if data['times'] else 0
            avg_nodes = np.mean(data['nodes']) if data['nodes'] else 0
            rate = 100 * data['solved'] / data['total']
            
            f.write(f"{model:<35} {avg_time:>10.3f}s {avg_nodes:>14,.0f} "
                   f"{data['solved']:>6}/{data['total']:<6} {rate:>8.1f}%\n")
        
        f.write("\n" + "=" * 100 + "\n\n")
        
        # Meilleur par taille
        f.write("MEILLEUR MODÈLE PAR TAILLE:\n")
        f.write("-" * 100 + "\n")
        f.write(f"{'N':<6} {'Modèle':<35} {'Temps':<12} {'Nœuds':<15}\n")
        f.write("-" * 100 + "\n")
        
        n_values = sorted(set(int(r['N']) for r in results))
        for n in n_values:
            n_results = [r for r in results if int(r['N']) == n and r['Status'] == 'SAT' and r['Time(s)']]
            if n_results:
                best = min(n_results, key=lambda x: float(x['Time(s)']))
                nodes = int(best['Nodes']) if best['Nodes'] else 0
                f.write(f"{n:<6} {best['Description']:<35} {float(best['Time(s)']):>10.3f}s {nodes:>14,}\n")
            else:
                f.write(f"{n:<6} {'Aucune solution':<35}\n")
        
        f.write("\n" + "=" * 100 + "\n")
    
    print(f"✓ Résumé textuel sauvegardé: {output_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python visualize.py <fichier_resultats.csv>")
        print("\nExemple: python visualize.py results/benchmark_20240115_143022.csv")
        return
    
    csv_file = Path(sys.argv[1])
    
    if not csv_file.exists():
        print(f"Erreur: fichier {csv_file} introuvable")
        return
    
    print("=" * 80)
    print("GÉNÉRATION DES VISUALISATIONS - N-QUEENS")
    print("=" * 80)
    print(f"\nFichier source: {csv_file}")
    print()
    
    # Charger les résultats
    results = load_results(csv_file)
    print(f"✓ {len(results)} résultats chargés")
    
    # Créer le dossier de sortie
    output_dir = csv_file.parent / 'visualizations'
    output_dir.mkdir(exist_ok=True)
    print(f"✓ Dossier de sortie: {output_dir}\n")
    
    # Générer les graphiques
    print("Génération des graphiques...")
    plot_time_comparison(results, output_dir)
    plot_nodes_comparison(results, output_dir)
    plot_best_per_size(results, output_dir)
    plot_success_rate(results, output_dir)
    
    print("\nGénération du résumé textuel...")
    generate_summary_table(results, output_dir)
    
    print("\n" + "=" * 80)
    print("VISUALISATIONS TERMINÉES!")
    print(f"Fichiers disponibles dans: {output_dir}")
    print("=" * 80)

if __name__ == "__main__":
    main()
