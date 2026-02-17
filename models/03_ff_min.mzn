% Heuristique first_fail : choisit la variable avec le plus petit domaine
% Value ordering : indomain_min (plus petite valeur d'abord)
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

constraint all_different(Q);
constraint all_different([Q[i] + i | i in 1..N]);
constraint all_different([Q[i] - i | i in 1..N]);

solve :: int_search(Q, first_fail, indomain_min) satisfy; %choisit la variable la plus contrainte (petit domaine),teste la plus petite valeur en premier.

output ["Q = ", show(Q)];
