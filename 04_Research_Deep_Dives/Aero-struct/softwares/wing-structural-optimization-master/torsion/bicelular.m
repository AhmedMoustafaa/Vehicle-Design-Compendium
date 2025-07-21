function [phi1, phi2] = bicelular(torque, area, rel_q, t, s)
%BICELULAR Summary of this function goes here
%   Detailed explanation goes here
int = zeros(1,3);
for i = 1:3
    int(i) = integral_linha_media(t{i}, s{i});
end
A = [                      rel_q                              ; ...
      2*area(1)          2*area(2)               0            ; ...
      int(1)/area(1)  -int(2)/area(2)  2*int(3)*(sum(1./area))];
B = [0 sum(torque) 0]';
flux = linsolve(A,B);
end

