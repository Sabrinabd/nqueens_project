% Contraintes redondantes pour améliorer la propagation
% Ajoute des contraintes implicites qui renforcent la détection de conflits
include "globals.mzn";

int: N;
array[1..N] of var 1..N: Q;

% Contraintes principales
constraint all_different(Q);
constraint all_different([Q[i] + i | i in 1..N]);
constraint all_different([Q[i] - i | i in 1..N]);

% Contraintes redondantes : pas deux reines sur même ligne (déjà implicite)
% Mais renforce la propagation
constraint forall(i in 1..N) (  %Pour chaque colonne i :exactement une reine doit être dans cette colonne.
    sum(j in 1..N) (bool2int(Q[j] == i)) == 1
);

solve :: int_search(Q, first_fail, indomain_min) satisfy;

output ["Q = ", show(Q)];
