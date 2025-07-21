function [properties] = reinforced_box_section(station, foil_name)
addpath geometry/foil geometry/section geometry/transform

chord = station.chord;
thickness = station.thickness;
limits = station.limits;

% geometric properties

foil = foil_properties(chord, 0, limits, [0 0], foil_name);

% foil countour
a1_c = foil.ex(1,:);
a2_c = foil.ex(end,:);
a1_t = foil.in(1,:);
a2_t = foil.in(end,:);

% foil inscrite retangle

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

% dimensions
width = D(1) - C(1);
height = A(2) - C(2);
web_length = height-2*thickness;

% areas
compression_flange_area = thickness*width;
traction_flange_area = thickness*width;
web_area = thickness*web_length;

% controids
compression_flange_centroid = A + [width -thickness]/2;
traction_flange_centroid = C + [width thickness]/2;
front_web_centroid = C + [thickness/2 thickness+web_length/2];
back_web_centroid = D + [-thickness/2 thickness+web_length/2];
c = [compression_flange_centroid; traction_flange_centroid; front_web_centroid; back_web_centroid];
a = [compression_flange_area; traction_flange_area; web_area; web_area];
centroid = multielement_centroid(c, a);

% second moment of inertia (t*l^3/12)
web_Ix = thickness*web_length^3/12; % no eixo do centroide
web_Iy = thickness^3*web_length/12;
% I12 = I21 = 0 <-> the axis are on the symetry axis (aproximating the web
% for a rectangle)
web_I = [web_Ix 0; 0 web_Iy]; 

compression_flange_Ix = width*thickness^3/12;
compression_flange_Iy = width^3*thickness/12;
compression_flange_I = [compression_flange_Ix 0; 0 compression_flange_Iy];

traction_flange_Ix = width*thickness^3/12;
traction_flange_Iy = width^3*thickness/12;
traction_flange_I = [traction_flange_Ix 0; 0 traction_flange_Iy];

% translate (geometrically) the tensors to the centroid
compression_flange_I = translate_inertia_tensor(compression_flange_I, compression_flange_centroid-centroid, compression_flange_area);
traction_flange_I = translate_inertia_tensor(traction_flange_I, traction_flange_centroid-centroid, traction_flange_area);
front_web_I = translate_inertia_tensor(web_I, front_web_centroid-centroid, web_area);
back_web_I = translate_inertia_tensor(web_I, back_web_centroid-centroid, web_area);

% section second moment of inertia tensor
I = compression_flange_I + traction_flange_I + front_web_I + back_web_I;
I(1,2) = 0; % Ixy deve ser nulo
I(2,1) = 0;

% pricipal second moment of inertia tensor
[I_max, theta] = principal_inertia_tensor(I);

% areas
% width_avergage = width-thickness;
% height_average = height-thickness;
area_mid = (width-thickness)*(height-thickness);
area = sum(a);

% line and mid line vertices
vert = [A;B;C;D];
vert_mid = vert + thickness*[1 -1; -1 -1; 1 1; -1 1]/2;

properties.I = I;
properties.I_max = I_max;
properties.Iz0 = I_max(1,1);
properties.Iy0 = I_max(2,2);
properties.theta_max = theta;
properties.centroide = centroid;
properties.area_mid = area_mid;
properties.area = area;
properties.width = width;
properties.height = height;
properties.alma_len = web_length;
properties.vertices = vert;
properties.vertices_mid = vert_mid;
% prop_cx.width_med = width_avergage;
% prop_cx.height_med = height_average;
properties.mc_cent = compression_flange_centroid;
properties.mt_cent = traction_flange_centroid;

end

