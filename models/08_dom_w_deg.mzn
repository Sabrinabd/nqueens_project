% Heuristique dom_w_deg : domaine divisé par le nombre de contraintes
% Très efficace en pratique car adaptatif
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

constraint all_different(Q);
constraint all_different([Q[i] + i | i in 1..N]);
constraint all_different([Q[i] - i | i in 1..N]);

solve :: int_search(Q, dom_w_deg, indomain_min) satisfy;%Choisit la variable avec taille domaine / nombre de contraintes actives.

output ["Q = ", show(Q)];
