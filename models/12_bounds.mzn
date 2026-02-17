% Propagation bounds : moins forte mais plus rapide 
% Utile pour comparer avec la propagation domain (par défaut)
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

constraint all_different(Q) :: domain; %propagation complete
constraint all_different([Q[i] + i | i in 1..N]) :: bounds;%Propagation plus légère sur les bornes seulement
constraint all_different([Q[i] - i | i in 1..N]) :: bounds;

solve :: int_search(Q, first_fail, indomain_min) satisfy;

output ["Q = ", show(Q)];
