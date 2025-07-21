function [ esforcos ] = internal_loads_FX(load_high_tip, load_high_mid, load_low, prop)
%ESFORCOS_BIPLANO Calcula os esforcos nas longarinas do biplano
%   Detailed explanation goes here

%% configuracao
b = 2.5; % envergadura asa de cima
b2 = 2.5; % envergadura asa de baixo
f = 0.5; % distancia da fuselagem
stagger = 0; % stagger (positivo -> asa de cima pra frente)
h = 0.6; % gap entre as asas
c_cima = 0.4; % corda na secao do engaste da asa de cima
c_baixo = 0.4; % corda na secao do engaste da asa de baixo

% posicoes das rotulas em relacao ao meio da corda (positivo em direcao ao bordo de fuga
a_cima = -0.5; % posicao da rotula frontal da asa de cima em percent de meia corda
b_cima = 0.5; % posicao da rotula traseira da asa de cima em percet de meia corda
a_baixo = -0.5; % posicao da rotula frontal da asa de baixo
b_baixo = 0.5; % posicao da rotula traseira da asa de baixo

d = 1; % distancia entre as fixacoes asa de cima
d2 = 1; % distancia das fixacoes asa de baixo

%% vetores de posicao
s_tip = load_high_tip.x; % vetor de posicao central dos paineis
s_0_tip = s + b/2; % deslocamento para ponta de asa

s2 = load_low.x; % vetor de posicao central dos paineis
s2_0 = s2 + b2/2; % deslocamento para ponta de asa

% posicao do centroide em relacao a 1/4 de corda (bdf positivo)
xl = [prop.centroide];
xl = xl(1:2:end);
xl = [flip(xl) xl];

%% carregamentos
w = load_high.dLdb; % vetor de carregamento (sustentacao)
wt = load_high.dMadb; % vetor de carregamento (momento torsor)
ws = w.*s_0; % vetor de momento fletor

w2 = load_low.dLdb;
wt2 = load_low.dMadb;

%% posicoes/indices de descontinuidade
[~, i1] = min(abs(s_0-(b-d)/2)); % indices das posicoes dos apoios da asa de cima
[~, i2] = min(abs(s_0-(b+d)/2));

[~, i12] = min(abs(s_0-(b2-d2)/2)); % indices das posicoes dos apoios da asa de baixo
[~, i22] = min(abs(s_0-(b2+d2)/2));

[~, i12f] = min(abs(s_0-(b2-f)/2)); % indicies das posicoes da fuselagem na asa de baixo
[~, i22f] = min(abs(s_0-(b2+f)/2));

%% integrais cumulativas
int_w_s1 = cumtrapz(s_0(,w);
int_ws = cumtrapz(s_0,ws);
int_wt = cumtrapz(s_0,wt+xl.*w);

% zera paineis da fuselagem na asa de baixo
w2 = horzcat(w2(1:i12f), zeros(1,i22f - i12f - 1), w2(i22f:end));
ws2 = w2.*s2_0;
wt2 = horzcat(wt2(1:i12f), zeros(1,i22f - i12f - 1), wt2(i22f:end));

int_w2 = cumtrapz(s2_0, w2);
int_ws2 = cumtrapz(s2_0, ws2);
int_wt2 = cumtrapz(s2_0, wt2+xl.*w2);

%% reacoes de apoio asa de cima (vista lateral)
% sec 1


%% solucao das hastes de fixacao (vista lateral)
% bases do trapezoide
a_t = (b_cima-a_cima)*c_cima/2;
b_t = (b_baixo-a_baixo)*c_baixo/2;

% posicoes das rotulas e stagger relativo
a_p_cima = (a_cima+1)*c_cima/2;
a_p_baixo = (a_baixo+1)*c_baixo/2;
s_rel = stagger+a_p_baixo-a_p_cima;

% angulos do trapezoide e diagonais
theta_1 = atan(s_rel/h);
theta_2 = atan((s_rel+b_t)/h);
theta_3 = atan((s_rel+b_t-a_t)/h);
theta_4 = atan((a_t-s_rel)/h);

% sistema linear da estrutura trelicada isoestatica
A = [0 0 0 0 0 cos(theta_1) 0 cos(theta_2); ...
     0 0 0 0 1 sin(theta_1) 0 sin(theta_2); ...
	 0 0 0 0 0 0 cos(theta_3) 0; ...
	 0 0 0 0 -1 0 sin(theta_3) 0; ...
	-1 0 0 0 0 cos(theta_1) 0 0; ...
	 0 0 1 0 0 sin(theta_1) 0 0; ...
	 0 -1 0 0 0 0 cos(theta_3) cos(theta_2); ...
	 0 0 0 -1 0 0 sin(theta_3) sin(theta_2)];
B = [Ra 0 Rb 0 0 0 0 0]';
X = linsolve(A,B); % [R_cy R_dy Rcx Rdx Fab Fac Fbd F_tirante]
if X(end) < 0 % caso o tirante estiver em compressao faz o sistema com equivalente com o outro tirante
    A(:,end) = [0 0 cos(theta_4) -sin(theta_4) cos(theta_4) -sin(theta_4) 0 0]';
    X = linsolve(A,B); % [R_cy R_dy R_cx R_dx F_ab F_ac F_bd F_tirante]
end
% momento concentrado resultante
% Fac = X(6);
% Fbd = X(7);
M_t = -(X(1)*(a_baixo*c_baixo/2-(-c_baixo/4)) + X(2)*(b_baixo*c_baixo/2-(-c_baixo/4)));

%% reacoes de apoio da asa de cima (vista frontal)
A = [1 1; (b-d)/2 ((b+d)/2)];
B = [int_w(end) int_ws(end)]';
X = linsolve(A,B);
Ra = X(1);
Rb = X(2);

%% calculo das hastes de fixacao (vista frontal)
theta = atan((d-d2)/(2*h));
phi = atan((d+d2)/(2*h));
A = [0 0 0 0 cos(theta) 0 0 cos(phi);...
     0 0 0 0 sin(theta) 0 1 sin(phi);...
     0 0 0 0 0 cos(theta) 0 0;...
     0 0 0 0 0 sin(theta) 1 0;...
     1 0 0 0 -cos(theta) 0 0 0;...
     0 0 1 0 sin(theta) 0 0 0;...
     0 1 0 0 0 -cos(theta) 0 -cos(phi);...
     0 0 0 1 0 sin(theta) 0 -sin(phi)];
B = [Ra 0 Rb 0 0 0 0 0]';
X = linsolve(A,B); % [R_cy R_dy R_cx R_dx F_ac F_bd F_ab F_tirante]
if X(end) < 0
    A(:,end) = [0 0 cos(phi) sin(phi) -cos(phi) -sin(phi) 0 0]';
    X = linsolve(A,B); % [R_cy R_dy R_cx R_dx F_ac F_bd F_ab F_tirante]
end
% Fcd = X(5);
% Fab = X(6);
% forcas concentradas
F1y = X(1);
F1x = X(3);
F2y = X(2);
F2x = X(4);
F_axial = X(7);

%% tensoes nas hastes
% A = [1 0 1 0;...
%      0 1 0 1;...
%      0 0 1 1;...
%      1 1 0 0];
% B = [Fac Fbd Fcd Fab]';
% X = linsolve(A,B);
% hastes.frontal.direita = X(1);
% hastes.traseira.direita = X(2);
% hastes.frontal.esquerda = X(3);
% hastes.traseira.esquerda = X(4);

%% reacoes de apoio da asa de baixo
A = [1 1; (b2-f)/2 (b2+f)/2];
B = [int_w2(end)+F1y+F2y int_ws2(end)+F1y*(b2-d2)/2+F2y*(b2+d2)/2]';
X = linsolve(A,B);
Ra2 = X(1);
Rb2 = X(2);

%% esforcos na asa de cima
% primeira secao
V1 = int_w;
M1 = s_0.*V1 - int_ws;
Mt1 = int_wt(1:i1);

% segunda secao
V2 = int_w - Ra;
M2 = s_0.*(V2 + Ra) - int_ws - Ra*(s_0-(b-d)/2);
x = trapz(s_0(i1:i2),wt(i1:i2).*s_0(i1:i2))/trapz(s_0(i1:i2),wt(i1:i2));
Mt2 = -cumtrapz(s_0(i1:i2),wt(i1:i2)) + trapz(s_0(i1:i2),wt(i1:i2))*((b+d)/2 - x)/d;

% terceira secao
V3 = int_w - Ra - Rb;
M3 = s_0.*(V3 + Ra + Rb) - int_ws - Ra*(s_0-(b-d)/2) - Rb*(s_0-(b+d)/2);
Mt3 = cumtrapz(s_0(i2:end),wt(i2:end)) - trapz(s_0(i2:end),wt(i2:end));

% esforco normal
N = horzcat(zeros(1,i1), ...
    F_axial*ones(1,i2-i1+1), ...
    zeros(1,length(s_0)-i2+1));

%% esforcos na asa de baixo
% primeira secao
V12 = int_w2;
M12 = s2_0.*V12 - int_ws2;
Mt12 = int_wt2(1:i12f);

% segunda secao
V22 = int_w2 + F1y;
M22 = s2_0.*int_w2 - int_ws2 + ...
      F1y*(s2_0-(b2-d2)/2);
Mt22 = int_wt2(1:i12f) - M_t*(F1y/(F1y+F2y));

% terceira secao
V32 = int_w2 + F1y - Ra2;
M32 = s2_0.*int_w2 - int_ws2 + ...
      F1y*(s2_0-(b2-d2)/2) - Ra2*(s2_0-(b2-f)/2);
Mt32 = int_wt2(i12f:i22f).*0;
  
% quarta secao
V42 = int_w2 + F1y - Ra2 - Rb2;
M42 = s2_0.*int_w2 - int_ws2 + ...
      F1y*(s2_0-(b2-d2)/2) - Ra2*(s2_0-(b2-f)/2) - ...
      Rb2*(s2_0-(b2+f)/2);
Mt42 = cumtrapz(s2_0(i22f:i22),wt2(i22f:i22)) -trapz(s2_0(i22f:end), wt2(i22f:end)) + M_t*(F2y/(F1y+F2y));

% quinta secao
V52 = int_w2 + F1y - Ra2 - Rb2 + F2y;
M52 = s2_0.*int_w2 - int_ws2 + ...
      F1y*(s2_0-(b2-d2)/2) - Ra2*(s2_0-(b2-f)/2) - ...
      Rb2*(s2_0-(b2+f)/2) + F2y*(s2_0-(b2+d2)/2);
Mt52 = cumtrapz(s2_0(i22f:end),wt2(i22f:end)) - trapz(s2_0(i22f:end), wt2(i22f:end));

% esforco normal
N2 = horzcat(zeros(1,i12), ...
    -F1x*ones(1,i12f - i12+1), ...
    zeros(1,i22f - i12f+1), ...
    -F2x*ones(1,i22 - i22f+1), ...
    zeros(1,length(s2_0)-i22+1));

%% vetores
high.s = [s(1:i1) s(i1:i2) s(i2:end)];
high.V = [V1(1:i1) V2(i1:i2) V3(i2:end)];
high.M = [M1(1:i1) M2(i1:i2) M3(i2:end)];
high.Mt = [Mt1 Mt2 Mt3];
high.F = N;

high.s = high.s(end/2:end);
high.V = high.V(end/2:end);
high.M = high.M(end/2:end);
high.Mt = high.Mt(end/2:end);
high.F = high.F(end/2:end);

low.s = [s2(1:i12) s2(i12:i12f) s2(i12f:i22f) s2(i22f:i22) s2(i22:end)];
low.V = [V12(1:i12) V22(i12:i12f) V32(i12f:i22f) V42(i22f:i22) V52(i22:end)];
low.M = [M12(1:i12) M22(i12:i12f) M32(i12f:i22f) M42(i22f:i22) M52(i22:end)];
low.Mt = [Mt12(1:i12) Mt22(i12:end) Mt32(1:end) Mt42(1:i22-i22f+1) Mt52(i22-i22f+1:end)];
low.F = N2;

low.s = low.s(end/2:end);
low.V = low.V(end/2:end);
low.M = low.M(end/2:end);
low.Mt = low.Mt(end/2:end);
low.F = low.F(end/2:end);

esforcos.asa_cima = high;
esforcos.asa_baixo = low;
% esforcos.hastes = hastes;
end

