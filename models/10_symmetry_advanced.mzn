% Bris de symétrie avancé
% Élimine plusieurs symétries en même temps
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

constraint all_different(Q);
constraint all_different([Q[i] + i | i in 1..N]);
constraint all_different([Q[i] - i | i in 1..N]);

% Bris de symétrie multiple
constraint Q[1] < Q[N];           % Élimine symétrie horizontale.
constraint Q[1] < N div 2 + 1;    % Force la première reine dans la moitié gauche.
constraint Q[1] < Q[2];           % Impose un ordre partiel entre les deux premières reines

solve :: int_search(Q, first_fail, indomain_min) satisfy;

output ["Q = ", show(Q)];
