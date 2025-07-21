%% Change of loads due to wing twist
% dL/dy = dL_0/dy + y*((q*a_w)/(H*s - q*a_w*K_2))*(P*c + (dL_0/dy)*K_1)
%
% K_1 = integral e*c^2*y dy [0 s]
% K_2 = integral e*c^2*y^2 dy [0 s]
% P = integral y*(dM/dy) dy [0 s]
% H = integral G*J dy [0 s]
%
%% 
J = zeros(1,length(prop));
for i=1:length(prop)
    J(i) = sum(diag(prop(i).I_max));
end
GJ = mat.G*J;

c = [panels.chord];
y = [panels.span];

v = carga.V_ref;
rho = 1.225;
q = .5*rho*v^2;

aw = wing.aw;

K_1 = trapz(y,xl_b2.*c.*y); % integral ec^2ydy [0,b/2] symetric in XZ
K_2 = trapz(y,xl_b2.*c.*(y.^2)); % integral ec^2y^2dy [0,b/2] symetric in XZ
H = trapz(y, GJ); % integral GJdy [0,b/2] symetric in XZ
P_R = trapz(y,y.*carga.dMadb(end/2+1:end)); % integral y(dM/dy)dy [0,b/2] nonsymetric
P_L = trapz(y,y.*flip(carga.dMadb(1:end/2)));

dLdb_R = carga.dLdb(end/2+1:end);
delta_R = y*q*aw.*(P_R*c + dLdb_R*K_1)./(H*b/2 - q*aw*K_2);
if mean(delta_R) > 0
    dLdb_R = dLdb_R + delta_R;
end

dLdb_L = flip(carga.dLdb(1:end/2));
delta_L = y*q*aw.*(P_R*c + dLdb_L*K_1)./(H*b/2 - q*aw*K_2);
if mean(delta_L) > 0
    dLdb_L = dLdb_L + delta_L;
end

dLdb = [flip(dLdb_L) dLdb_R];