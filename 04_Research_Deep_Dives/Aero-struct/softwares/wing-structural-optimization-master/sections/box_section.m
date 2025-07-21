function prop = box_section(panel)
addpath prop_geo

chord = panel.chord;
mc_thick = panel.t_mc;
mt_thick = panel.t_mt;
alma_thick = panel.t_alma;
limits = panel.limits;

% calculo da geometria da secao

% perfil
foil = get_foil_prop(chord, 0, limits, [0 0]);

% limites do perfil
a1_c = foil.ex(1,:);
a2_c = foil.ex(end,:);
a1_t = foil.in(1,:);
a2_t = foil.in(end,:);

% limites construtivos do retangulo

if a1_c(2) < a2_c(2)
    A = a1_c;
    B = [a2_c(1) a1_c(2)];
else
    A = [a1_c(1) a2_c(2)];
    B = a2_c;
end
if a1_t(2) < a2_t(2)
    C = [a1_t(1) a2_t(2)];
    D = a2_t;
else
    C = a1_t;
    D = [a2_t(1) a1_t(2)];
end

% dimensoes
width = D(1) - C(1);
height = A(2) - C(2);
alma_len = height-mt_thick-mc_thick;

% areas
mc_area = mc_thick*width;
mt_area = mt_thick*width;
alma_area = alma_thick*alma_len;

% centroides
mc_cent = A + [width -mc_thick]/2;
mt_cent = C + [width mt_thick]/2;
a1_cent = C + [alma_thick/2 mt_thick+alma_len/2];
a2_cent = D + [-alma_thick/2 mt_thick+alma_len/2];
c = [mc_cent; mt_cent; a1_cent; a2_cent];
a = [mc_area; mt_area; alma_area; alma_area];
cent = centroide_multielemento(c, a);

% segundo momento de inercia
alma_Ix = alma_thick*alma_len^3/12; % no eixo do centroide
alma_Iy = alma_thick^3*alma_len/12;
alma_I = [alma_Ix 0; 0 alma_Iy]; % produto de inercia avaliado no eixo de simetria vale 0 (centroide) (aproximando a alma para um retangulo)

mc_Ix = width*mc_thick^3/12;
mc_Iy = width^3*mc_thick/12;
mc_I = [mc_Ix 0; 0 mc_Iy];

mt_Ix = width*mt_thick^3/12;
mt_Iy = width^3*mt_thick/12;
mt_I = [mt_Ix 0; 0 mt_Iy];

% translacao dos eixos para o centroide da secao
mc_I = translada_eixo(mc_I, mc_cent-cent, mc_area);
mt_I = translada_eixo(mt_I, mt_cent-cent, mt_area);
a1_I = translada_eixo(alma_I, a1_cent-cent, alma_area);
a2_I = translada_eixo(alma_I, a2_cent-cent, alma_area);

% tensor de inercia da secao
I = mc_I + mt_I + a1_I + a2_I;
I(1,2) = 0; % Ixy deve ser nulo
I(2,1) = 0;

% tensor de inercia principal da secao
[I_max, theta] = inercia_principal(I);

% areas
area_media = (width-alma_thick)*(height-mc_thick/2-mt_thick/2);
area = sum(a);

% vertices e vertices na linha media
vert = [A;B;C;D];
vert_lm = vert + [alma_thick -mc_thick; -alma_thick -mc_thick; ...
                  alma_thick +mt_thick; -alma_thick +mt_thick]/2;

prop.I = I;
prop.I_max = I_max;
prop.Iz0 = I_max(1,1);
prop.Iy0 = I_max(2,2);
prop.theta_max = theta;
prop.centroide = cent;
prop.area_media = area_media;
prop.area = area;
prop.width = width;
prop.height = height;
prop.alma_len = alma_len;
prop.vertices = vert;
prop.vertices_lm = vert_lm;
prop.mc_cent = mc_cent;
prop.mt_cent = mt_cent;

end

