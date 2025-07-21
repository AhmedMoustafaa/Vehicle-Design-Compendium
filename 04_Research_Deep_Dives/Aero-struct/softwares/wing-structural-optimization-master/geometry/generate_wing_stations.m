function [stations] = generate_wing_stations(wing_geometry, structure_geometry, s)
%GENERATE_WING_STATION This function generates N interpolated stations
%   Detailed explanation goes here
chord       = interp1(wing_geometry.span_transitions, wing_geometry.chord_transitions, s);

a_limit     = interp1(wing_geometry.span_transitions, structure_geometry.x_position, s);
a_limit     = (a_limit+chord/4)./chord;
w           = interp1(wing_geometry.span_transitions, structure_geometry.width, s);
b_limit     = a_limit + w./chord;
limits      = vertcat(a_limit, b_limit);

t_caixao    = interp1(wing_geometry.span_transitions, structure_geometry.thickness, s);
t_refor     = interp1(wing_geometry.span_transitions, structure_geometry.reinforcer, s);

for i = length(s):-1:1
    stations(i).limits = limits(:,i)';
    stations(i).thickness = t_caixao(i);
    stations(i).reinforcer = t_refor(i);
    stations(i).span = s(i);
    stations(i).chord = chord(i);
end
end

