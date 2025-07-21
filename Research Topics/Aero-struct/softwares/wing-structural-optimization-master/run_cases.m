%% optimization run cases
% Here you can create run cases with specific configurations.


%% section configuration
% section_type => the shape of the section (may change how analysis goes)
% section_type = 'foil_shaped';
% section_type = 'box';
% section_type = 'reinforced_box';
% section_type = 'D';
% section_type = 'O';

%% constraint configuration
% constraint_gap (real) => the distance of the restrainsts
%
% constraint_type => if the constraint is simply supported or fixed
% constraint_type = 'ss'; % for simply supported
% constraint_type = 'fx'; % for fixed
%
% constraint_angle (°) => the inclination of a symbolic  truss
% support so an parasol-wing can be modeled
% constraint_angle = 0; % this means a vertical truss or no truss at
% all
% constraint_angle = 90; % this will mean a horizontal struss wich is
% not applicable at all

%%
switch run
    case 1
        section_type = 'reinforced_box';
        constraint_gap = 0.1;
        constraint_type = 'ss';
        constraint_angle = 0;
        foil_name = 's1223';
end

save('data/run_config.mat', 'section_type', 'constraint_gap', ...
     'constraint_type', 'constraint_angle', 'foil_name');
clearvars('section_type', 'constraint_gap', 'constraint_type', ...
          'constraint_angle', 'foil_name')
