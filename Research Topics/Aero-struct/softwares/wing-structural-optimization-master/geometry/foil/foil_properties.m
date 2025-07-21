function [foil] = foil_properties(chord, scale_thick, limits, offset, foil_name)
%GET_FOIL_PROP Get airfoil geormetric data and info
%   offsets = [ext_offset int_offset]

%%
try
    load(['foils/' foil_name '.mat'], 'ex_lin', 'in_lin', 'ext', 'int', 'esp');
catch
    error('Por favor, execute o script $parse_foil$ antes de iniciar a rotina');
end

% esp = 0.0001;
% set limits
% limits = limits - p_rot;
% limits = Rot*[limits; 0 0];
% limits = limits + p_rot;
a = limits(1);
b = limits(2);

% Scale foil to the chord
ext = horzcat((0:esp:1)', ex_lin(0:esp:1));
int = horzcat((0:esp:1)', in_lin(0:esp:1));

ext = ext.*chord;
int = int.*chord;

% Translate the points to 1/4 of the chord in x
ext(:,1) = ext(:,1) - chord/4;
int(:,1) = int(:,1) - chord/4;

% Translate the points to camber line of the foil (y)
[~,i] = min(abs(ext(:,1)));
shift = (ext(i,2) + int(i,2))/2;

% spar section

ext = horzcat((a:esp:b)', ex_lin(a:esp:b));
int = horzcat((a:esp:b)', in_lin(a:esp:b));

% Scale foil to the chord
ext = ext.*chord;
int = int.*chord;

% Translate the points to 1/4 of the chord in x
ext(:,1) = ext(:,1) - chord/4;
int(:,1) = int(:,1) - chord/4;

% Translate the points to camber line of the foil (y)
ext(:,2) = ext(:,2) - shift;
int(:,2) = int(:,2) - shift;

% apply scale for a thick (please do not use)
if scale_thick ~= 0
    % ext
    tangent_vec_ext = horzcat(diff(ext(:,1)), diff(ext(:,2)));
    ext(end,:) = [];
    ext = ext + tangent_vec_ext/2;
    normal_vec_ext = [cos(pi/2) -sin(pi/2); sin(pi/2) cos(pi/2)]*tangent_vec_ext';
    mod_normal_vec_ext = sqrt(normal_vec_ext(:,1).^2 + normal_vec_ext(:,2).^2);
    normal_vec_ext = normal_vec_ext'./(ones(length(normal_vec_ext),2).*mod_normal_vec_ext');
    ext = ext + normal_vec_ext*scale_thick;
    
    % int
    tangent_vec_int = [diff(int(:,1)) diff(int(:,2))];
    int(end,:) = [];
    int = int + tangent_vec_int/2;
    normal_vec_int = [cos(pi/2) -sin(pi/2); sin(pi/2) cos(pi/2)]*tangent_vec_int';
    mod_normal_vec_int = sqrt(normal_vec_int(:,1).^2 + normal_vec_int(:,2).^2);
    normal_vec_int = normal_vec_int'./(ones(length(normal_vec_int),2).*mod_normal_vec_int');
    int = int - normal_vec_int*scale_thick;
end

% apply offset
ext(:,2) = ext(:,2) - offset(1);
int(:,2) = int(:,2) + offset(2);

% perimeter
dx = diff(ext(:,1));
dy = diff(ext(:,2));
ds = sqrt(dy.^2 + dx.^2);
ex_len = sum(ds);

dx = diff(int(:,1));
dy = diff(int(:,2));
ds = sqrt(dy.^2 + dx.^2);
in_len = sum(ds);

front_len = ext(1,2) - int(1,2);
back_len = ext(end,2) - int(end,2);

% get area
area = trapz(int(:,1),ext(:,2) - int(:,2));

% vector of points
x = vertcat(ext(:,1), int(:,1), linspace(int(1,1),ext(1,1))', linspace(int(end,1),ext(end,1))');
y = vertcat(ext(:,2), int(:,2), linspace(int(1,2),ext(1,2))', linspace(int(end,2),ext(end,2))');

% make the struct
foil.extra_length = ex_len;
foil.intra_length = in_len;
foil.front_length = front_len;
foil.back_length = back_len;
foil.perimeter = ex_len + in_len + front_len + back_len;
foil.area = area;
foil.ex = ext;
foil.in = int;
foil.x = x;
foil.y = y;
end

