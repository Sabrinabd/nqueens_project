% Heuristique first_fail avec indomain_max
% Teste la plus grande valeur d'abord
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

constraint all_different(Q);
constraint all_different([Q[i] + i | i in 1..N]);
constraint all_different([Q[i] - i | i in 1..N]);

solve :: int_search(Q, first_fail, indomain_max) satisfy;%choisit la variable la plus contrainte (petit domaine),mais teste la plus grande variable d'abord 

output ["Q = ", show(Q)];
