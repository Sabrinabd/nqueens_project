% Modèle avec contraintes globales all_different
% Propagation plus efficace que le modèle naïf
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

constraint all_different(Q); %Aucune reine ne peut être dans la même colonne
constraint all_different([Q[i] + i | i in 1..N]);%On empêche les conflits sur les diagonales descendente 
constraint all_different([Q[i] - i | i in 1..N]);%On empêche les conflits sur les diagonales ascendente

solve satisfy;

output ["Q = ", show(Q)];
