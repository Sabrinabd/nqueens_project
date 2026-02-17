% Bris de symétrie : Q[1] < Q[N]
% Élimine les solutions miroir (symétrie horizontale)
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

constraint all_different(Q);
constraint all_different([Q[i] + i | i in 1..N]);
constraint all_different([Q[i] - i | i in 1..N]);

% Bris de symétrie
constraint Q[1] < Q[N];%Supprime les solutions miroir gauche ↔ droite

solve :: int_search(Q, first_fail, indomain_min) satisfy;

output ["Q = ", show(Q)];
