% Heuristique avec sélection aléatoire des valeurs
% Utile pour comparer avec les approches déterministes
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

constraint all_different(Q);
constraint all_different([Q[i] + i | i in 1..N]);
constraint all_different([Q[i] - i | i in 1..N]);

solve :: int_search(Q, first_fail, indomain_random) satisfy; %Choisit valeur au hasard

output ["Q = ", show(Q)];
