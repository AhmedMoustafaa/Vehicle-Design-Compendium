function [p] = section_centroid(len)
%CENTROID Summary of this function goes here
%   Detailed explanation goes here

% x = 1/A * integral(x dA) ==> x = 1/A * thick integral(x dl)
dx = diff(len(:,1));
dy = diff(len(:,2));
dl = sqrt(dx.^2 + dy.^2);
len(end,:) = [];
x = len(:,1) + dx/2;
y = len(:,2) + dy/2;
L = sum(dl);
x_m = (1/L)*trapz(x.*dl);
y_m = (1/L)*trapz(y.*dl);
p = [x_m y_m];
end