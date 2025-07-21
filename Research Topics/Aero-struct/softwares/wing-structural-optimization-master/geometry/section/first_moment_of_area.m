function [Qx, Qy] = first_moment_of_area(len, thick)
%PRIMEIRO_MOMENTO_DE_AREA Summary of this function goes here
%   dQx = y*dA
%   dQy = x*dA
dx = diff(len(:,1));
dy = diff(len(:,2));
dl = sqrt(dx.^2 + dy.^2);
dA = dl*thick;
len(end,:) = [];
x = len(:,1) + dx/2;
y = len(:,2) + dy/2;
Qx = trapz(x.*dA);
Qy = trapz(y.*dA);
end

