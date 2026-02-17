# Projet N-Queens - Programmation par Contraintes

Projet de comparaison de différentes techniques de modélisation et de recherche pour le problème des N-Reines.

## Structure du projet

```
nqueens_project/
├── models/          # 15 modèles MiniZinc différents
├── data/            # Fichiers .dzn pour N=8,10,12,15,20,25,30,40
├── results/         # Résultats des benchmarks (CSV + visualisations)
├── benchmark.py     # Script automatique de benchmark
├── visualize.py     # Script de visualisation des résultats
└── README.md        
```

## Modèles testés

### Modélisations de base

1. **01_naive.mzn** - Contraintes binaires explicites (baseline)
2. **02_global.mzn** - Contraintes globales `all_different`

### Heuristiques de sélection de variables

3. **03_ff_min.mzn** - First-Fail + indomain_min
4. **04_ff_max.mzn** - First-Fail + indomain_max
5. **05_ff_split.mzn** - First-Fail + indomain_split
6. **06_input_order.mzn** - Input order (ordre naturel)
7. **07_smallest.mzn** - Smallest (plus petit domaine)
8. **08_dom_w_deg.mzn** - Domain/Weighted-Degree
9. **15_max_regret.mzn** - Max Regret

### Techniques avancées

10. **09_symmetry_basic.mzn** - Bris de symétrie simple (Q[1] < Q[N])
11. **10_symmetry_advanced.mzn** - Bris de symétrie multiple
12. **11_redundant.mzn** - Contraintes redondantes
13. **12_bounds.mzn** - Propagation bounds vs domain
14. **13_random.mzn** - Sélection aléatoire des valeurs
15. **14_combined_optimal.mzn** - Combinaison des meilleures techniques

## Utilisation

### Prérequis

```bash
# Installer MiniZinc
# Télécharger depuis: https://www.minizinc.org/

# Installer les dépendances Python
pip install matplotlib numpy
```

### Lancer le benchmark complet

```bash
cd nqueens_project
python benchmark.py
```

### Visualiser les résultats

```bash
python visualize.py results/benchmark_XXXXXXXX_XXXXXX.csv
```

### Tester un modèle spécifique

```bash
minizinc --solver gecode --statistics models/08_dom_w_deg.mzn data/n20.dzn
```
