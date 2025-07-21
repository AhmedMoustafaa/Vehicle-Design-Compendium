function [ raw_fit, data ] = fit_function( X )
% fitness_function
% X -> a array of the optimization variables
%
%% Load files

% run configuration
load('data/run_config.mat', 'section_type', 'constraint_type');

% wing basic geometry
load('data/wing_geometry.mat', 'wing');

% wing aerodynamic loading with N stations and M cases
load('data/loads.mat', 'loads');

%% Generates beam geometry from parametrization
addpath parametrics
switch section_type
    case 'reinforced_box'
        geometry = reinforced_box_parametric_geometry(X, wing);
end

%% Generates the wing stations
addpath geometry
s = loads(1).x(n_sec+1:end);
stations = generate_wing_stations(wing, geometry, s);

%% Calculate section properties per station
for i = n_sec:-1:1
    switch section_type
        case 'reinforced_box'
            properties = reinforced_box_section(stations(i), wing);
        case 'D'
            properties = D_section(stations(i), wing);
        case 'foil_shaped'
            properties = foild_shaped_section(stations(i), wing);
        case 'O'
            properties = O_section(stations(i), wing);
        case 'box'
            properties = box_section(stations(i), wing);
    end
    stations(i).properties = properties;
end

%% Calculate force and moment diagrams for the structure per loading case
for i = length(loads):-1:1
    switch constraint_type
        case 'ss'
            internal_loads(i) = beam_forces_SS(loads(i), wing, stations);
        case 'fx'
            internal_loads(i) = beam_forces_FX(loads(i), wing, stations);
    end
end

%% Calculate structural criterias
addpath criterias
for j = length(internal_loads):-1:1
    for i = 1:n_sec
        ms_asa_l(i) = safety_margin(station(i), internal_loads(j).L, i, sections(i)); % left wing
        ms_asa_r(i) = safety_margin(station(i), internal_loads(j).R, i, sections(i)); % right wing
    end
    ms(j) = min([ms_asa_l ms_asa_r]);
end

[min_ms, i] = min(ms);
critic_cond = loads(i);

report = report_45(station, sections, wing);

%% Calculate total mass
[mass, dm] = long_mass(station, sections, long_geo, freijo, balsa);
mass = 2*mass;

%% Calculate the fitness of X
raw_fit = weight_function(mass, min_ms, report);

%% Data for future analysis
data.panels = station;
data.report_45 = report;
data.long_geo = long_geo;
data.wing = wing;
data.mass = mass;
data.dm = dm;
data.min_ms = min_ms;
data.ms = ms;
data.esforcos = internal_loads;
data.props = sections;
data.desenho = desenho;
data.critic_cond = critic_cond;

%toc
end
