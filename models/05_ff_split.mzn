% Heuristique first_fail avec indomain_split
% Divise le domaine en deux et teste la moitié inférieure d'abord
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

constraint all_different(Q);
constraint all_different([Q[i] + i | i in 1..N]);
constraint all_different([Q[i] - i | i in 1..N]);

solve :: int_search(Q, first_fail, indomain_split) satisfy;%Coupe le domaine en deux et Teste d’abord la moitié basse

output ["Q = ", show(Q)];
