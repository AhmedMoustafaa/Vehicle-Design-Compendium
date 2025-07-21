function [I] = area_inertia_tensor(thick, len)
% SEGUNDO MOMENTO DE AREA Calcula o momento de inercia
%   Detailed explanation goes here

% Ix = integral(y^2 dA) ==> Ix = thick integral(y^2 dl)
% Ix = thick*sum(y_medio_i^2 delta_l_i), i [1,N]
dx = diff(len(:,1));
dy = diff(len(:,2));
dl = sqrt(dx.^2 + dy.^2);
len(end,:) = [];
x = len(:,1) + dx/2;
y = len(:,2) + dy/2;
y2 = y.^2;
x2 = x.^2;
xy = y.*x;
Ix = trapz(y2.*dl);
Iy = trapz(x2.*dl);
Ixy = trapz(xy.*dl);
I = [Ix Ixy; Ixy Iy]*thick;
end