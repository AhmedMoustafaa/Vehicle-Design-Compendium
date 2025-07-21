function prop = O_section(foil_name, chord, pos, offset, thick)
global silence
addpath prop_geo

% definicao da secao aerodinamica
% foil_name = 's1210.dat';
% chord = 600;
inc = 0; % negativo -> aumenta o angulo de ataque !!!NÃO MUDAR, ainda em desenvolvimento!!!
p_inc = 1; % ponto/eixo de torcao - (0) bordo de ataque - (1) bordo de fuga

% pos = 0.25;
% offset = 8;
% thick = 5;

% perfil
foil1 = get_foil_prop(foil_name, chord, inc, p_inc, 0, [0 pos], [0 0]);
foil2 = get_foil_prop(foil_name, chord, inc, p_inc, 0, [pos 1], [0 0]);
t = foil1.ex(end,2) - foil1.in(end,2);
C = [foil1.in(end,1) foil1.in(end,2)+t/2];
P = vertcat(foil1.ex, foil1.in, foil2.ex, foil2.in);
d_vec = abs(P - C.*ones(length(P),2));
r = sqrt(d_vec(:,1).^2 + d_vec(:,2).^2);
r_max = min(r);

r_ex = r_max - offset;
r_in = r_ex - thick;
area = pi*(r_ex^2 - r_in^2)/2;
area_media = pi*((r_ex - r_in)^2)/2;
cent = C;
I = pi*(r_ex^4 - r_in^4)*[1/4 1/2; 1/2 1/4];
[I_max, theta] = inercia_principal(I);

prop.I = I;
prop.I_max = I_max;
prop.theta_max = theta;
prop.centroide = cent;
prop.area_material = area;
prop.area_media = area_media;

% plot
if ~silence
    figure;
    hold on; axis equal; grid on;

    % perfil
    f = get_foil_prop(foil_name, chord, inc, p_inc, 0, [0 1], [0 0]);
    plot(f.ex(:,1), f.ex(:,2), f.in(:,1), f.in(:,2), 'blue');

    % longarina
    viscircles([cent;cent],[r_ex;r_in], 'Color', 'black', 'LineWidth', 1);

    % centroide
    scatter(cent(1), cent(2));
    
    % inercias principais
    plot([cent(1) cent(1)], [cent(2) cent(2)+30], 'black', 'LineWidth', 1.1);
    plot([cent(1) cent(1)+30], [cent(2) cent(2)], 'black', 'LineWidth', 1.1);
    [delta_x, delta_y] = pol2cart(theta,30);
    plot([cent(1) cent(1)+delta_x], [cent(2) cent(2)+delta_y], 'r', 'LineWidth', 1.1);
    [delta_x, delta_y] = pol2cart(theta+pi/2,30);
    plot([cent(1) cent(1)+delta_x], [cent(2) cent(2)+delta_y], 'r', 'LineWidth', 1.1);
    
    
end
end
