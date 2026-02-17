% Modèle naïf : contraintes binaires explicites
% Pas de contraintes globales, pas d'heuristiques
int: N;
array[1..N] of var 1..N: Q;

constraint
    forall(i, j in 1..N where i < j) ( % Pour chaque paire de colonnes (i, j) sans répétition
        Q[i] != Q[j] /\  % 1. Pas sur la même ligne (conflit horizontal)
        abs(Q[i] - Q[j]) != abs(i - j) % pas sur la meme diagonale
    );

solve satisfy;

output ["Q = ", show(Q)];
