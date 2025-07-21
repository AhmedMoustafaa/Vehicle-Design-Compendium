function prop = D_section(foil_name, chord, thick, alma_thick, limit)
global silence
addpath prop_geo

% definicao da secao aerodinamica
% foil_name = 's1210.dat';
% chord = 600;
inc = 0; % negativo -> aumenta o angulo de ataque !!!NÃO MUDAR, ainda em desenvolvimento!!!
p_inc = 1; % ponto/eixo de torcao - (0) bordo de ataque - (1) bordo de fuga

% definicao das espessuras
% thick = 3;
% alma_thick = 3;

% percent de corda longarina
% limit = 0.25;

foil = get_foil_prop(foil_name, chord, inc, p_inc, -thick/2, [0 limit], [0 0]);

% superior
sup_area = foil.extra_length*thick;
sup_cent = centroide_elemento(foil.ex);

% inferior
inf_area = foil.intra_length*thick;
inf_cent = centroide_elemento(foil.in);

% alma
a_foil = get_foil_prop(foil_name, chord, inc, p_inc, -thick, [0 limit-alma_thick/(2*chord)], [0 0]);
alma_area = a_foil.back_length*alma_thick;
alma_cent = [a_foil.in(end,1) a_foil.in(end,2)+a_foil.back_length/2];

% centroide
c = [sup_cent; inf_cent; alma_cent];
a = [sup_area; inf_area; alma_area];
cent = centroide_multielemento(c, a);

% segundo momento de area de cada elemento
sup_I = segundo_momento_de_area(thick, foil.ex - sup_cent); % no eixo da origem
inf_I = segundo_momento_de_area(thick, foil.in - sup_cent);

a_Ix = alma_thick*a_foil.back_length^3/12; % no eixo do centroide
a_Iy = alma_thick^3*a_foil.back_length/12;
alma_I = [a_Ix 0; 0 a_Iy]; % produto de inercia avaliado no eixo de simetria vale 0 (centroide) (aproximando a alma para um retangulo)

% translacao dos eixos para o centroide da secao
sup_I = translada_eixo(sup_I, sup_cent-cent, sup_area);
inf_I = translada_eixo(inf_I, sup_cent-cent, inf_area);
alma_I = translada_eixo(alma_I, alma_cent-cent, alma_area);

% tensor de inercia da secao
I = sup_I + inf_I + alma_I;

% tensor de inercia principal da secao
[I_max, theta] = inercia_principal(I);

% areas
foil = get_foil_prop(foil_name, chord, inc, p_inc, -thick/2, [0 limit-alma_thick/(2*chord)], [0 0]);
area_media = foil.area;

prop.I = I;
prop.I_max = I_max;
prop.theta_max = theta;
prop.centroide = cent;
prop.area_media = area_media;

% plot
if ~silence
    figure;
    hold on; grid on; axis equal;

    foil = get_foil_prop(foil_name, chord, inc, p_inc, 0, [0 1], [0 0]);
    f_ext = get_foil_prop(foil_name, chord, inc, p_inc, 0, [0 limit], [0 0]);
    f_int = get_foil_prop(foil_name, chord, inc, p_inc, -thick, [0 limit-alma_thick/chord], [0 0]);

    % perfil
    plot(foil.ex(:,1), foil.ex(:,2), 'blue', foil.in(:,1), foil.in(:,2), 'blue');

    % mesas
    plot(f_ext.ex(:,1), f_ext.ex(:,2), 'black', f_ext.in(:,1), f_ext.in(:,2), 'black');
    plot(f_int.ex(:,1), f_int.ex(:,2), 'black', f_int.in(:,1), f_int.in(:,2), 'black');

    % almas
    plot([f_ext.ex(end,1) f_ext.in(end,1)], [f_ext.ex(end,2) f_ext.in(end,2)], 'black');
    plot([f_int.ex(end,1) f_int.in(end,1)], [f_int.ex(end,2) f_int.in(end,2)], 'black');

    % centroides
    scatter(cent(1), cent(2), 'blue');
    scatter(c(:,1), c(:,2));
    
    % inercias principais
    plot([cent(1) cent(1)], [cent(2) cent(2)+30], 'black', 'LineWidth', 1.1);
    plot([cent(1) cent(1)+30], [cent(2) cent(2)], 'black', 'LineWidth', 1.1);
    [delta_x, delta_y] = pol2cart(theta,30);
    plot([cent(1) cent(1)+delta_x], [cent(2) cent(2)+delta_y], 'r', 'LineWidth', 1.1);
    [delta_x, delta_y] = pol2cart(theta+pi/2,30);
    plot([cent(1) cent(1)+delta_x], [cent(2) cent(2)+delta_y], 'r', 'LineWidth', 1.1);
    
end
end