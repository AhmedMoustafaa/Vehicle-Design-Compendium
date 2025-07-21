%% Start with the default options
options = optimoptions('ga');
%% Modify options setting
options = optimoptions(options,'CreationFcn', @gacreationlinearfeasible);
options = optimoptions(options,'MaxGenerations',100);
options = optimoptions(options,'PopulationSize', 200);
% options = optimoptions(options,'CrossoverFraction', 0.9);
% options = optimoptions(options,'StallTest', 'geometricweighted');
% options = optimoptions(options,'MaxStallTime', 3600);
% options = optimoptions(options,'FitnessScalingFcn', {  @fitscalingtop [] });
% options = optimoptions(options,'SelectionFcn', @selectionremainder);
% options = optimoptions(options,'CrossoverFcn', {  @crossoverheuristic [] });
% options = optimoptions(options,'MutationFcn', @mutationadaptfeasible);
% options = optimoptions(options,'HybridFcn', {  @patternsearch [] });
options = optimoptions(options,'Display', 'final');
options = optimoptions(options,'OutputFcn',@save_iter);
options = optimoptions(options,'PlotFcn', {  @gaplotbestf @gaplotbestindiv @gaplotdistance @gaplotexpectation @gaplotrange @gaplotscorediversity @gaplotscores @gaplotselection @gaplotstopping});
options = optimoptions(options,'UseVectorized', false);
options = optimoptions(options,'UseParallel', parallel);

% options = optimoptions(options,'InitialPopulationMatrix', optresult.x);
% options = optimoptions(options,'InitialScoresMatrix', score);

%% run ga
[x,fval,exitflag,output,population,score] = ...
ga(@f_objetivo,nvars,Aineq,bineq,[],[],lb,ub,[],[4],options);

optresult.x = x;
optresult.fval = fval;
optresult.exitflag = exitflag;
optresult.output = output;
optresult.population = population;
optresult.score = score;

clearvars x fval exitflag output population score

function [state,options,optchanged] = save_iter(options,state,flag)
optchanged = false;
save('run/iter_ga.mat', 'state');
end