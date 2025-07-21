%% Load and save the wing geometry data
load('data/run_config.mat', 'constraint_gap', 'constraint_angle', 'foil_name')

%% Wing plant form
%            root_chord
%         |--------------|
% -------------------------------------------------> x-axis (symetric)
%         |              | ------------------
%         |              |   |              |
%         |              |   | pci*b/2      |
%         |              |   |              |
%         |              |   |              |
%         |              | ---              | b/2
%          \            /                   |
%           \          /                    |
%            \        /                     |
%             \______/ ----------------------  
%             
%             |------|
%       root_chord*taper_ratio

%%
wing.root_chord = 1; % wing root_chord (at the symetry plane)
wing.full_span = 7; % wing full span 
wing.taper_ratio = [1 0.5]; % chord/root_chord
wing.taper_position = 0.75; % percentage of semi-span in wich it tapers
wing.sweep = [0 0]; % wing sweep at 1/4 chord in degrees NOT IMPLEMENTED
wing.dihedral = [0 0]; % wing dihedral angle in degrees NOT IMPLEMENTED
wing.torsion = [0 0]; % wing geometric torsion in degrees (positive pitch up) NOT IMPLEMENTED
wing.foil = {foil_name, foil_name}; % the name of the standart .dat airfoil file NOT IMPLEMENTED
wing.constraint_distance = constraint_gap;
wing.constraint_angle = constraint_angle;

wing.chord_transitions = wing.root_chord*[1 wing.taper_ratio];
wing.span_transitions = [0 cumsum(wing.full_span*[wing.taper_position 1-wing.taper_position]/2)];

save('data/wing_geometry.mat', 'wing');
clearvars wing constraint_gap constraint_angle foil_name