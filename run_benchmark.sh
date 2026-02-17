#!/bin/bash
# Script de lancement rapide du benchmark N-Queens

echo "=========================================="
echo "PROJET N-QUEENS - BENCHMARK AUTOMATIQUE"
echo "=========================================="
echo ""

# Vérifier que MiniZinc est installé
if ! command -v minizinc &> /dev/null
then
    echo "ERREUR: MiniZinc n'est pas installé"
    echo "Téléchargez-le depuis: https://www.minizinc.org/"
    exit 1
fi

echo "MiniZinc détecté: $(minizinc --version | head -n1)"
echo ""

# Vérifier les dépendances Python
echo "Vérification des dépendances Python..."
if ! python3 -c "import matplotlib, numpy" 2>/dev/null
then
    echo "Installation des dépendances Python..."
    pip install -r requirements.txt
fi

echo "Dépendances OK"
echo ""

# Lancer le benchmark
echo "Lancement du benchmark..."
echo " Durée estimée: 10-30 minutes"
echo ""

python3 benchmark.py

# Vérifier si le benchmark a réussi
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "BENCHMARK TERMINÉ AVEC SUCCÈS!"
    echo "=========================================="
    echo ""
    echo "Pour visualiser les résultats:"
    echo "  python3 visualize.py results/benchmark_*.csv"
    echo ""
else
    echo ""
    echo "Le benchmark a échoué"
    exit 1
fi
