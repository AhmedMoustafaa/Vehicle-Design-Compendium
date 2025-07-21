function [mass, dm] = beam_mass(panel, prop, long_geo, mat_refor, mat_caixao)
% LONG_MASS Calcula a massa da longarina
%   Cavalieri's Principle
panel_c.limits = long_geo.limits(:,1)';
panel_c.t_caixao = long_geo.t_caixao(1);
panel_c.t_refor = long_geo.t_refor(1);
panel_c.span = long_geo.spans(1);
panel_c.chord = long_geo.chords(1);
prop_c = sec_caixao_reforcada(panel_c);

panel_t.limits = long_geo.limits(:,2)';
panel_t.t_caixao = long_geo.t_caixao(2);
panel_t.t_refor = long_geo.t_refor(2);
panel_t.span = long_geo.spans(2);
panel_t.chord = long_geo.chords(2);
prop_t = sec_caixao_reforcada(panel_t);

mc_l = [prop_c.width [prop.width] prop_t.width];
mt_l = [prop_c.width [prop.width] prop_t.width];
a1_l = [prop_c.height [prop.height] prop_t.height];
a2_l = [prop_c.height [prop.height] prop_t.height];
caixao_t = [panel_c.t_caixao [panel.t_caixao] panel_t.t_caixao];

mc_A = mc_l.*caixao_t;
mt_A = mt_l.*caixao_t;
a1_A = a1_l.*caixao_t;
a2_A = a2_l.*caixao_t;

ref_A = 2*[panel_c.t_refor [panel.t_refor] panel_t.t_refor].^2;

dist = [long_geo.spans(1) [panel.span] long_geo.spans(2)];

V_mc = .5*diff(dist).*(mc_A(2:end)+mc_A(1:end-1));
V_mt = .5*diff(dist).*(mt_A(2:end)+mt_A(1:end-1));
V_a1 = .5*diff(dist).*(a1_A(2:end)+a1_A(1:end-1));
V_a2 = .5*diff(dist).*(a2_A(2:end)+a2_A(1:end-1));
V_ref = .5*diff(dist).*(ref_A(2:end)+ref_A(1:end-1));

dm = (V_mc + V_mt + V_a1 + V_a2)*mat_caixao.dens + V_ref*mat_refor.dens;

mass = sum(dm);
end