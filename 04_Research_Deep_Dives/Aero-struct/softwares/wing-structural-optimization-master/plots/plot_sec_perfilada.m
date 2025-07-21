function [fig] = plot_sec_perfilada(panel)

chord = panel.chord;
mc_thick = panel.t_mc;
mt_thick = panel.t_mt;
alma_thick = panel.t_alma;
limits = panel.limits;

fig = figure;
%set(gca, 'xdir', 'reverse');
hold on;

foil = get_foil_prop(chord, 0, [0 1], [0 0]);
f_ext = get_foil_prop(chord, 0, limits, [0 0]);
f_int = get_foil_prop(chord, 0, reshape(limits,1,[]) + [alma_thick -alma_thick]./chord, [mc_thick mt_thick]);
% f_mid = get_foil_prop(foil_name, chord, inc, p_inc, limits + [almas_thick -almas_thick]./(2*chord), [mc_thick mt_thick]/2);

% perfil
plot(foil.ex(:,1), foil.ex(:,2), 'blue', foil.in(:,1), foil.in(:,2), 'blue');

% mesas
plot(f_ext.ex(:,1), f_ext.ex(:,2), 'black', f_ext.in(:,1), f_ext.in(:,2), 'black');
plot(f_int.ex(:,1), f_int.ex(:,2), 'black', f_int.in(:,1), f_int.in(:,2), 'black');
% plot(f_mid.ex(:,1), f_mid.ex(:,2), '--black', f_mid.in(:,1), f_mid.in(:,2), '--black');

% almas
plot([f_ext.ex(1,1) f_ext.in(1,1)], [f_ext.ex(1,2) f_ext.in(1,2)], 'black');
plot([f_ext.ex(end,1) f_ext.in(end,1)], [f_ext.ex(end,2) f_ext.in(end,2)], 'black');

plot([f_int.ex(1,1) f_int.in(1,1)], [f_int.ex(1,2) f_int.in(1,2)], 'black');
plot([f_int.ex(end,1) f_int.in(end,1)], [f_int.ex(end,2) f_int.in(end,2)], 'black');

% plot([f_mid.ex(1,1) f_mid.in(1,1)], [f_mid.ex(1,2) f_mid.in(1,2)], '--black');
% plot([f_mid.ex(end,1) f_mid.in(end,1)], [f_mid.ex(end,2) f_mid.in(end,2)], '--black');

% centroides
% scatter(cent(1), cent(2), 'blue');
% scatter(c(:,1), c(:,2));

% inercias principais
% plot([cent(1) cent(1)], [cent(2) cent(2)+30], 'black', 'LineWidth', 1.1);
% plot([cent(1) cent(1)+30], [cent(2) cent(2)], 'black', 'LineWidth', 1.1);
% [delta_x, delta_y] = pol2cart(theta,30);
% plot([cent(1) cent(1)+delta_x], [cent(2) cent(2)+delta_y], 'r', 'LineWidth', 1.1);
% [delta_x, delta_y] = pol2cart(theta+pi/2,30);
% plot([cent(1) cent(1)+delta_x], [cent(2) cent(2)+delta_y], 'r', 'LineWidth', 1.1);

axis equal; grid on;
end