% Heuristique input_order : sélectionne les variables dans l'ordre
% Moins efficace mais utile comme baseline
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

constraint all_different(Q);
constraint all_different([Q[i] + i | i in 1..N]);
constraint all_different([Q[i] - i | i in 1..N]);

solve :: int_search(Q, input_order, indomain_min) satisfy;%Choisit Q[1], puis Q[2], puis Q[3]…

output ["Q = ", show(Q)];
