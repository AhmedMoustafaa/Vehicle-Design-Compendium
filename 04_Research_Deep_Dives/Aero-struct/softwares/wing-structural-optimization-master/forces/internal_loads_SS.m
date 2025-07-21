function [ internal_loads ] = internal_loads_SS(load, prop, wing, panels)
%ESFORCOS_BIPLANO Calcula os esforcos nas longarinas do biplano
%   Detailed explanation goes here
%
%                              d
%                       |-------------| 
%        ==============================================
%        |              \             /               |
%        |               \           /                |
%        |--------------------------------------------| 
%                              b
%
%
%% wing configuration
b = wing.full_span; % span
d = wing.d; % supports distance
theta = wing.theta; % supports internal angle

%% integration variable (span-wise)
s = load.x; % each load force is applied in the center of each panel
s = [-b/2 s b/2];
s_0 = s + b/2; % deslocamento para ponta de asa

% centroid position in relative to 0.25 chord (trailing edge positive)
xl = [prop.centroid];
xl_b2 = xl(1:2:end);
xl = [flip(xl_b2) xl_b2];
xl = [xl(1) xl xl(1)];

%% loads

safety_factor = 1.5;
incertety_factor = 1.15;

w = load.dLdb*safety_factor*incertety_factor; % Aerodynamic Lift loads
w = [0 w 0];

wt = load.dMadb*safety_factor*incertety_factor; % Aerodynamic Torsion Moment loads
wt = [0 wt 0];

%% descontinous points (closest station from the supports)
[~, i1] = min(abs(s_0-(b-d)/2));
[~, i2] = min(abs(s_0-(b+d)/2));

%% cummulative integrals
int_w = cumtrapz(s_0, w);
int_ws = cumtrapz(s_0, w.*s);
int_wt_1 = cumtrapz(s_0(1:i1),wt(1:i1) + xl(1:i1).*w(1:i1));
int_wt_2 = cumtrapz(s_0(i1:i2),wt(i1:i2) + xl(i1:i2).*w(i1:i2));
int_wt_3 = cumtrapz(s_0(i2:end),wt(i2:end) + xl(i2:end).*w(i2:end));

%% reaction forces
A = [sin(theta) sin(theta); cos(theta)*(b-d)/2 cos(theta)*((b+d)/2)];
B = [int_w(end) int_ws(end)]';
X = linsolve(A,B);
Ra = X(1);
Rb = X(2);

%% internal loads
% first section
V1 = int_w;
M1 = s_0.*V1 - int_ws;
Mt1 = int_wt_1;
N1 = zeros(1,i1-1);

% second section (middle)
V2 = int_w - Ra;
M2 = s_0.*(V2 + Ra) - int_ws - Ra*(s_0-(b-d)/2);
x = trapz(s_0(i1:i2),wt(i1:i2).*s_0(i1:i2))/trapz(s_0(i1:i2),wt(i1:i2));
Mt2 = -int_wt_2 + int_wt_2(end)*((b+d)/2 - x)/d;
N2 = linspace(Ra*cos(theta), Rb*cos(theta), i2-i1+1); % TODO: check this

% third section
V3 = int_w - Ra - Rb;
M3 = s_0.*(V3 + Ra + Rb) - int_ws - Ra*(s_0-(b-d)/2) - Rb*(s_0-(b+d)/2);
Mt3 = int_wt_3 - int_wt_3(end);
N3 = zeros(1,length(s_0)-i2);

%% union
loads.s = s;
loads.V = [V1(1:i1-1) abs(V1(i1)-V2(i1)) V2(i1+1:i2-1) -abs(V2(i2)-V3(i2)) V3(i2+1:end)];
loads.M = [M1(1:i1-1) max([M1(i1) M2(i1)]) M2(i1+1:i2-1) max([M2(i2) M3(i2)]) M3(i2+1:end)];
loads.Mt = [Mt1(1:end-1) abs(Mt1(end))*max(abs([Mt1(end) Mt2(1)]))/Mt1(end) Mt2(2:end-1) abs(Mt3(1))*max(abs([Mt2(end) Mt3(1)]))/Mt3(1) Mt3(2:end)];
loads.F = [N1(1:i1-1)  N2(i1:i2) N3(i2+1:end)];
loads.i1 = i1;
loads.i2 = i2;
loads.x =  loads.Mt ./ loads.V; % position of a force in an equivalent static system

right.i = i2 - (length(loads.s)/2+1);
left.i = length(loads.s)/2 - i1;

% remove tips
loads.s([1,end]) = [];
loads.V([1,end]) = [];
loads.M([1,end]) = [];
loads.Mt([1,end]) = [];
loads.F([1,end]) = [];

% separete left and right
right.s = loads.s(end/2+1:end);
right.V = loads.V(end/2+1:end);
right.M = loads.M(end/2+1:end);
right.Mt = loads.Mt(end/2+1:end);
right.F = loads.F(end/2+1:end);

left.s = flip(-loads.s(1:end/2));
left.V = flip(-loads.V(1:end/2));
left.M = flip(loads.M(1:end/2));
left.Mt = -flip(loads.Mt(1:end/2));
left.F = flip(loads.F(1:end/2));

internal_loads.L = left;
internal_loads.R = right;
internal_loads.B = loads;
end

