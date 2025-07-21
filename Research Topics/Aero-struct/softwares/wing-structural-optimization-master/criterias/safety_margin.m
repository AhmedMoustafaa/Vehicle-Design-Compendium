function [ min_ms ] = safety_margin( panel, load, i, prop )
%MARGEM_SEGURANCA Summary of this function goes here
%   Detailed explanation goes here
t_ref = panel.t_refor;
t_caixao = panel.t_caixao;

%% propriedades da secao
cent = prop.centroide;
width = prop.width_med;
height = prop.height_med;
Iz0 = prop.Iz0;
A = prop.area;
Am = prop.area_media;
x_cent = cent(1);
x_alma1 = panel.limits(1)*panel.chord - panel.chord/4;
x_alma2 = panel.limits(2)*panel.chord - panel.chord/4;

%% verifica hipotese das paredes finas
%t_s = mean([t_alma t_mt t_mc])/prop.foil_med.perimeter;
%if t_s > .1
%    fprintf('\nHipotese de paredes finas falhou\n');
%end
%% solicitacoes
V = load.V(i);
Mf = load.M(i);
F = load.F(i);
Mt = load.Mt(i);

%% linha neutra
Mf_z0 = Mf;

% perimetro da secao rotacionada e transladada
z0 = prop.vertices(:,1) - cent(1);
y0 = prop.vertices(:,2) - cent(2);

% equacao da linha neutra (0 = c + b*z - a*y)
a = Mf_z0/Iz0; c = F/A;
ln = @(z) 0*z + c/a;

% separa pontos acima e abaixo da L.N.
P = horzcat(z0,y0);
RRow = P(:,2) >= ln(P(:,1));
P_comp = P(RRow,:);
P_trac = P(~RRow,:);

% distancias dos pontos a L.N.
d_comp = abs((-a)*P_comp(:,2) + c)/abs(a);
d_trac = abs((-a)*P_trac(:,2) + c)/abs(a);

% distancias maximas
[~,i_comp] = max(d_comp);
[~,i_trac] = max(d_trac);
p_max_comp = P_comp(i_comp,:);
p_max_trac = P_trac(i_trac,:);

y_comp = p_max_comp(2);
y_trac = p_max_trac(2);

%% idealizacao da estrutura

B = zeros(4,1);
% areas dos booms
B(1) = 0;
B(2) = t_ref^2;% + t_caixao*height*(2+y_comp/y_trac)/6 + t_caixao*width/2;
B(3) = t_ref^2;% + t_caixao*height*(2+y_trac/y_comp)/6 + t_caixao*width/2;
B(4) = 0;

% centroide
y_cent = sum(B([1 2]))*height/sum(B);

% momentos de inercia
Ixx(1) = B(1)*(height-y_cent)^2;
Ixx(2) = B(2)*(height-y_cent)^2;
Ixx(3) = B(3)*(-y_cent)^2;
Ixx(4) = B(4)*(-y_cent)^2;

Ixx_total = sum(Ixx);

% tensoes normais
sigma_x = -Mf_z0*[y_comp y_comp y_trac y_trac]./Ixx_total;

%%
B_s = zeros(4,1);
% areas dos booms
B_s(1) = t_caixao*height*(2+y_comp/y_trac)/6 + t_caixao*width/2;
B_s(2) = t_caixao*height*(2+y_comp/y_trac)/6 + t_caixao*width/2;
B_s(3) = t_caixao*height*(2+y_trac/y_comp)/6 + t_caixao*width/2;
B_s(4) = t_caixao*height*(2+y_trac/y_comp)/6 + t_caixao*width/2;

% centroide
y_cent = sum(B_s([1 2]))*height/sum(B_s);

% momentos de inercia
Ixx(1) = B_s(1)*(height-y_cent)^2;
Ixx(2) = B_s(2)*(height-y_cent)^2;
Ixx(3) = B_s(3)*(-y_cent)^2;
Ixx(4) = B_s(4)*(-y_cent)^2;

Ixx_total = sum(Ixx);

% fluxos de cisalhamento (corte na sacao 1-2)
qb12 = 0;
qb23 = -(V/Ixx_total)*(B(2)*y_comp);
qb34 = qb23 - (V/Ixx_total)*(B(3)*y_trac);
qb41 = qb34 - (V/Ixx_total)*(B(4)*y_trac);

A23 = (x_cent - x_alma1)*height/4;
A34 = height*width/4;
A41 = (x_alma2 - x_cent)*height/4;

qs_0 = -2*(A23*qb23 + A34*qb34 + A41*qb41)/(2*width*height);

q_t = Mt/(2*width*height);

q12 = qs_0 + qb12 + q_t;
q23 = qs_0 + qb23 + q_t;
q34 = qs_0 + qb34 + q_t;
q41 = qs_0 + qb41 + q_t;

sigma_xy = [q12 q23 q34 q41]/t_caixao;

%% criterios de falha

% estados planos de tensao (placas)

% tensores nos booms
sigma_boom = zeros(3,3,4);
sigma_boom(1,1,:) = sigma_x;

% tensores nos revestimentos
sigma_rev = zeros(3,3,4);
sigma_rev(2,1,:) = sigma_xy;
sigma_rev(1,2,:) = sigma_xy;
               
% tensor tensao na borda da mesa de compressao
% sigma11 = sigma_x_comp;
% sigma12 = tau_xy + tau_xy_cort_aba_cima;
% sigma_mc = [    sigma11      sigma12     0; ...
%                 sigma12         0        0; ...
%                    0            0        0];

% tensor tensao na borda da mesa de compressao
% sigma11 = sigma_x_trac;
% sigma12 = tau_xy + tau_xy_cort_aba_baixo;
% sigma_mt = [    sigma11      sigma12     0; ...
%                 sigma12         0        0; ...
%                    0            0        0];

% propriedades do material
alma_mat = material_long('balsa');
mesa_mat = material_long('freijo');

fail = zeros(4,2);

% criterios de falha
fail(1,1) = max_tension_criteria(sigma_boom(:,:,2), mesa_mat, 'axial');
fail(2,1) = max_tension_criteria(sigma_boom(:,:,3), mesa_mat, 'axial');
fail(3,1) = max_tension_criteria(sigma_rev(:,:,2), alma_mat, 'axial');
fail(4,1) = max_tension_criteria(sigma_rev(:,:,4), alma_mat, 'axial');
fail(5,1) = max_tension_criteria(sigma_rev(:,:,1), alma_mat, 'trans');
fail(6,1) = max_tension_criteria(sigma_rev(:,:,3), alma_mat, 'trans');

fail(1,2) = tsai_wu_criteria(sigma_boom(:,:,2), mesa_mat, 'axial');
fail(2,2) = tsai_wu_criteria(sigma_boom(:,:,3), mesa_mat, 'axial');
fail(3,2) = tsai_wu_criteria(sigma_rev(:,:,2), alma_mat, 'axial');
fail(4,2) = tsai_wu_criteria(sigma_rev(:,:,4), alma_mat, 'axial');
fail(5,2) = tsai_wu_criteria(sigma_rev(:,:,1), alma_mat, 'trans');
fail(6,2) = tsai_wu_criteria(sigma_rev(:,:,3), alma_mat, 'trans');


min_ms = min(min(fail));
if(min_ms < 0)
    t = 1;
end
%% deslocamentos
% torcao
% [~, dphidx] = ang_torcao_parede_fina(Mt, {t_mt t_alma t_mc t_alma},...
%     {prop.foil.intra_length prop.foil.front_length prop.foil.extra_length prop.foil.back_length},...
%     Am, G, 0);

end

