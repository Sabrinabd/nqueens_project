% Modèle combiné : meilleures techniques ensemble
% Contraintes globales + bris de symétrie + bonne heuristique
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

constraint all_different(Q);
constraint all_different([Q[i] + i | i in 1..N]);
constraint all_different([Q[i] - i | i in 1..N]);

% Bris de symétrie
constraint Q[1] < Q[N];

solve :: int_search(Q, dom_w_deg, indomain_min) satisfy;

output ["Q = ", show(Q)];
