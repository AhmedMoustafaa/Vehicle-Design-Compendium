function [pos] = multielement_centroid(posicoes, areas)
%MULTI_ELEM_CENTROIDE Calcula a posicao do centroide em uma figura multielemento
%utilizando o metodo da decomposicao
% posicoes -> matriz N:2 com a 1a coluna como x e a 2a como y
% (posicoes dos centroides de cada elemento).
% area -> vetor coluna N:1 com os valores respectivos de cada area.

A = sum(areas);
Sx = sum(areas.*posicoes(:,1));
Sy = sum(areas.*posicoes(:,2));
pos = [Sx Sy]/A;

end

