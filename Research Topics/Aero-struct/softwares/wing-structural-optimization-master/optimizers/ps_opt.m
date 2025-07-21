% x0 = [4.9866    1.0030    1.0000    2.0000    2.0000    3.9275    1.0083];
%% Start with the default options
options = optimoptions('patternsearch');
%% Modify options setting
options = optimoptions(options,'PollMethod', 'madspositivebasis2n');
options = optimoptions(options,'UseCompletePoll',true);
options = optimoptions(options,'Display', 'final');
options = optimoptions(options,'OutputFcn', { @save_iter });
options = optimoptions(options,'PlotFcn', {  @psplotbestf @psplotmeshsize @psplotfuncount @psplotbestx });
options = optimoptions(options,'UseVectorized', false);
options = optimoptions(options,'UseParallel', parallel);

%% run
[x,fval,exitflag,output] = ...
patternsearch(@f_objetivo,x0,Aineq,bineq,[],[],lb,ub,[],options);

optresult.x = x;
optresult.fval = fval;
optresult.exitflag = exitflag;
optresult.output = output;

clearvars x fval exitflag output

function [stop,options,optchanged] = save_iter(optimvalues,options,flag)
    save('run/iter_ps.mat','optimvalues');
    optchanged = false;
    stop = false;
end
