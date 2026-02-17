% Heuristique max_regret : maximise le regret
% Choisit la variable où la différence entre meilleure et 2e meilleure valeur est maximale
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

constraint all_different(Q);
constraint all_different([Q[i] + i | i in 1..N]);
constraint all_different([Q[i] - i | i in 1..N]);

solve :: int_search(Q, max_regret, indomain_min) satisfy;

output ["Q = ", show(Q)];
