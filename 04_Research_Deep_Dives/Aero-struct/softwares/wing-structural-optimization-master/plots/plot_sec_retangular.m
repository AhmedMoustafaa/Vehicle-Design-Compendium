function [] = plot_sec_retangular(panel, prop)

chord = panel.chord;
mc_thick = panel.t_mc;
mt_thick = panel.t_mt;
alma_thick = panel.t_alma;
vert = prop.vertices;

% plot
figure;
hold on; axis equal; grid on;

% perfil
f = get_foil_prop(foil_name, chord, inc, p_inc, 0, [0 1], [0 0]);
plot(f.ex(:,1), f.ex(:,2), f.in(:,1), f.in(:,2), 'blue');

% longarina
X = vert(:,1)';
Y = vert(:,2)';
X_i = X + [1 -1 -1 1 1]*alma_thick;
Y_i = Y + horzcat(mc_thick*[-1 -1], mt_thick*[1 1], -mc_thick);
plot(X,Y, 'black');
plot(X_i,Y_i, 'black');

end