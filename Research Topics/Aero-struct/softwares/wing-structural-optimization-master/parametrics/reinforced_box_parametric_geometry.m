function [geometry] = reinforced_box_parametric_geometry( X, wing_geometry)
%% This script uses a parametrization for a reinforced box configuration
% Input:
% X -> Vector of parametric input
% wing_geometry -> struct with wing geometric info
%
% Output:
% geometry ->
%  - x_position -> positions of the center of the structure
% cross-section relative to the foil cross-section
%  - width -> width of the 



% tip station
tip.position                = X(1); % position of the frontmost part in percentage of chord
tip.width                   = X(2); % width in percentage of chord
tip.height                  = -1;   % it will serach for the maximum height avaliable 
tip.thickness               = X(4); % thickness of the box
tip.reinforcer              = X(5); % thickness of the reinforcer
tip.chord                   = wing_geometry.chord_transitions(3);

% mid station
mid.position                = X(1); %
mid.width                   = X(3); %
mid.height                  = -1;   % it will serach for the maximum height avaliable 
mid.thickness               = X(4); %
mid.reinforcer              = X(5); %
mid.chord                   = wing_geometry.chord_transitions(2);

% root station
root.position               = X(1); %
root.width                  = X(3); %
root.height                 = -1;   % it will serach for the maximum height avaliable 
root.thickness              = X(4); %
root.reinforcer             = X(5); %
root.chord                  = wing_geometry.chord_transitions(1);

%% generates the geometry

% first section
first_sec = basic_box_section(root, mid);

% second section
second_sec = basic_box_section(mid, tip);

% semi-span main parameters
geometry.x_position = [first_sec.x_position second_sec.x_position(2)];
geometry.width = [first_sec.width second_sec.width(2)];
geometry.thickness = [first_sec.thickness second_sec.thickness(2)];

geometry.limits = [first_sec.limits second_sec.limits(2)];
geometry.reinforcer = [root.reinforcer mid.reinforcer tip.reinforcer];
end
