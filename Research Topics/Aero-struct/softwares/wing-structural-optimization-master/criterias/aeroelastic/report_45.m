function [ report ] = report_45( panel, prop, wing )
%REPORT_45 Summary of this function goes here
%   Wing Flexibility Factor
%   F = integral ( QiCi^2ds, [aileron tip])
%   F <= 200/V_d^2
%
%   Qi = Wing Twist per unit Torsional Moment applied (rad/(ft-lb))
%   Qi = Theta_i/Moment
%   Ci = Wing Chord (ft)
%   ds = increment of span (ft)
%   V_d = Design dive speed (IAS) (mph)


M = 1; % 1 Nm
M_imp = M*0.73756; % ft-lb

Vd = wing.V_d*2.23694; % mph

load.Mt = ones(1,length(panel))*M; % Moment applied on wing tip
load.i = 1;

theta = torcao_asa(panel,prop,load,material_long('balsa')); % rad

span = [panel.span];
[~,i] = min(abs(span - wing.spans(2)));
s = span(i:end);
s_b = s - [diff(s)/2 diff([s(end) wing.spans(3)])];
s_b = [s_b wing.spans(3)];

C = [panel.chord];
C = C(i:end)*3.28084; % ft

delta_s = diff(s_b)*3.28084; % ft

X = theta(i:end)./M_imp;

Y = X.*C.^2.*delta_s;
F = sum(Y);

report = F/(200/(Vd^2));

end

