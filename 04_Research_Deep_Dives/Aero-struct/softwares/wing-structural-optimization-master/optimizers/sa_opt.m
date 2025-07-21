%% Start with the default options
options = optimoptions('simulannealbnd');
%% Modify options setting
options = optimoptions(options,'TemperatureFcn', @temperatureboltz);
options = optimoptions(options,'Display', 'final');
options = optimoptions(options,'HybridInterval', 'end');
options = optimoptions(options,'PlotFcn', {  @saplotbestf @saplotbestx @saplotstopping @saplottemperature @saplotx @saplotf });
options = optimoptions(options,'OutputFcn', {});

[x,fval,exitflag,output] = ...
simulannealbnd(@f_objetivo,x0,lb,ub,options);

optresult.x = x;
optresult.fval = fval;
optresult.exitflag = exitflag;
optresult.output = output;

clearvars x fval exitflag output

function [state,options,optchanged] = save_iter(options,state,flag)
optchanged = false;
save('run/iter_simaneal.mat', 'state');
end
