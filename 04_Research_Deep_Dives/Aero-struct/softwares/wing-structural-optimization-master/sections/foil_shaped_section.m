function prop = foil_shaped_section(panel)
addpath prop_geo

chord = panel.chord;
mc_thick = panel.t_mc;
mt_thick = panel.t_mt;
alma_thick = panel.t_alma;
limits = panel.limits;

% definicao da secao aerodinamica
% foil_name = 's1210.dat';
% chord = 600;
% inc = 0; % negativo -> aumenta o angulo de ataque !!!NAO MUDAR, ainda em desenvolvimento!!!
% p_inc = 1; % ponto/eixo de torcao - (0) bordo de ataque - (1) bordo de fuga

% definicao das espessuras
% mc_thick = 5;
% mt_thick = 5;
% alma_thick = 1;

% percent de corda longarina
% limits = [0.25 0.3];

% calculo da geometria da secao

% mesas
m_f = get_foil_prop(chord, 0, limits, [mc_thick mt_thick]/2);

% mesa compressao
mc_area = m_f.extra_length*mc_thick;
mc_cent = centroide_elemento(m_f.ex);

% mesa tracao
mt_area = m_f.intra_length*mc_thick;
mt_cent = centroide_elemento(m_f.in);

% almas
a_f = get_foil_prop(chord, 0, limits + [alma_thick -alma_thick]./(2*chord), [mc_thick mt_thick]);
a1_area = a_f.front_length*alma_thick;
a2_area = a_f.back_length*alma_thick;
a1_cent = [a_f.in(1,1) (a_f.in(1,2)+a_f.front_length/2)];
a2_cent = [a_f.in(end,1) (a_f.in(end,2)+a_f.back_length/2)];

% centroide
c = [mc_cent; mt_cent; a1_cent; a2_cent];
a = [mc_area; mt_area; a1_area; a2_area];
cent = centroide_multielemento(c, a);

% segundo momento de area de cada elemento
mc_I = segundo_momento_de_area(mc_thick, m_f.ex - mc_cent); % no eixo do centroide
mt_I = segundo_momento_de_area(mt_thick, m_f.in - mt_cent);

a1_Ix = alma_thick*a_f.front_length^3/12; % no eixo do centroide
a1_Iy = alma_thick^3*a_f.front_length/12;
a1_I = [a1_Ix 0; 0 a1_Iy]; % produto de inercia avaliado no eixo de simetria vale 0 (centroide) (aproximando a alma para um retangulo)

a2_Ix = alma_thick*a_f.back_length^3/12;
a2_Iy = alma_thick^3*a_f.back_length/12;
a2_I = [a2_Ix 0; 0 a2_Iy];

% translacao dos eixos para o centroid da secao
mc_I = translada_eixo(mc_I, mc_cent-cent, mc_area);
mt_I = translada_eixo(mt_I, mt_cent-cent, mt_area);
a1_I = translada_eixo(a1_I, a1_cent-cent, a1_area);
a2_I = translada_eixo(a2_I, a2_cent-cent, a2_area);

% tensor de inercia da secao
I = mc_I + mt_I + a1_I + a2_I;

% tensor de inercia principal da secao
[I_max, theta] = inercia_principal(I);

% areas
foil_lm = get_foil_prop(chord, 0, limits + [alma_thick -alma_thick]./(2*chord), [mc_thick mt_thick]/2);
area_media = foil_lm.area;
area = m_f.extra_length*mc_thick + m_f.intra_length*mt_thick + alma_thick*(a_f.front_length + a_f.back_length);

prop.I = I;
prop.I_max = I_max;
prop.Iz0 = I_max(1,1);
prop.Iy0 = I_max(2,2);
prop.theta_max = theta;
prop.centroide = cent;
prop.area_media = area_media;
prop.area = area;
prop.foil = get_foil_prop(chord, 0, limits, [0 0]);
prop.foil_med = foil_lm;
prop.mc_cent = mc_cent;
prop.mt_cent = mt_cent;

end

