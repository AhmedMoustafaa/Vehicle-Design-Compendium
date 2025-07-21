%% Setup and Start Optimization
%
% Optimization Problem:
% Minimize the spar mass of the wing main structure,
% constrained by failure, geometric and project design.
%
% The wing plant form is a double tapered kind.
% 
%% Optimization Variables:
% X(1) => web_pos_tip
% X(2) => width_tip
% X(3) => width_root
% X(4) => box_thickness
% X(5) => reinforcer_thickness

%% setup project variables

% select run case (details at 'run_cases.m')
run = 1;
run_cases % generates data/run_config.mat

%% setup airfoil shape data
addpath geometry/foil
parse_foil % generates data/foil_fit.mat

%% setup wing geometry
wing_geometry % generates data/wing_geometry.mat

%% bounds
nvars = 5;

lb = [.01 .01 .01 1 2e-3]';
ub = [.6 .4 .4 4 1e-2]';

%% constraints
Aineq = [1 1 0 0 0; 1 0 1 0 0];
% limits based on airfoil construction method and control surfaces
bineq = [.75 .75]';

%% run optimizer
addpath optimizers
optimizer = 'ga';
parallel = false;

switch optimizer
    case 'ga'   % genetic algorith
        ga_opt
    case 'ps'   % pattern search
        x0 = [];
        ps_opt
    case 'psw'  % particle swarm
        psw_opt
    case 'sa'   % simulated annealing
        x0 = [];
        sa_opt
end

clearvars Aineq bineq lb ub nvars optimizer parallel

%%
[~,data] = fit_function(optresult.x);


