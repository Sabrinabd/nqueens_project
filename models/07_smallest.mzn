% Heuristique smallest : choisit la variable avec le plus petit domaine
% Similaire à first_fail mais avec tie-breaking différent
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

constraint all_different(Q);
constraint all_different([Q[i] + i | i in 1..N]);
constraint all_different([Q[i] - i | i in 1..N]);

solve :: int_search(Q, smallest, indomain_min) satisfy; %Choisit la variable avec plus petit domaine

output ["Q = ", show(Q)];
