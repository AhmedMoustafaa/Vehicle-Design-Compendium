function [int] = integral_linha_media(t_cell, s_cell)
%INTEGRAL_LINHA_MEDIA Summary of this function goes here
%   t_cell => expressoes para a espessura
%   s_cell => comprimento correspondente a espessura
int = 0;
s = [0 cumsum(cell2mat(s_cell))];
for i = 1:length(t_cell)
    int = int + t_cell{i}*(s(i+1)-s(i));
end
end

