function [flecha] = wing_displacement(panel,long_geo,load,mat, prop)
s = [panel.span];
h = abs(diff(s(1:2)));
M_R = [load.R.M];
M_L = [load.L.M];
E = ones(1,length(s))*mat.axial_E;
I = [prop.Iz0];
K_R = -h.^2.*M_R./(E.*I);
K_L = -h.^2.*M_L./(E.*I);

A = zeros(length(s));

A(1,2) = 2;
A(2,2:3) = [-2 1];  
for i=3:length(s)-1
    A(i,i-1:i+1) = [1 -2 1];
end
A(1,:) = [];
A(:,1) = [];
K_R(1) = [];
K_L(1) = [];
A(end,:) = [];
A(:,end) = [];
K_R(end) = [];
K_L(end) = [];

w_l = linsolve(A,K_L');
w_r = linsolve(A,K_R');
flecha.R = cumsum([0 w_r' 0]);
flecha.L = cumsum([0 w_l' 0]);

end