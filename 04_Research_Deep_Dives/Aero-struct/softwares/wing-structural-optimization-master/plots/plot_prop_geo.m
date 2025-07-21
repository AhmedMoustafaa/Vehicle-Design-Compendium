function [] = plot_prop_geo( data, mat )
%PLOT_PROP_GEO Summary of this function goes here
%   Detailed explanation goes here

prop = data.props;
panel = data.panels;

s = [panel.span];
I = zeros(1,length(prop));
J = zeros(1,length(prop));
for i=1:length(prop)
    I(i) = prop(i).I_max(1,1);
    J(i) = I(i)+prop(i).I_max(2,2);
end
EI = mat.axial_E*I;
GJ = mat.G*J;

figure('Name', 'Rigidez');
yyaxis right
plot(s,EI);
ylabel('EI (Nm^2)');
yyaxis left
plot(s,GJ);
legend('GJ','EI');
ylabel('GJ (Nm^2)');
xlabel('semi-span (m)');
title('EI & GJ vs span');
end

