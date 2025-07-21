%% Start with the default options
options = optimoptions('particleswarm');
%% Modify options setting
options = optimoptions(options,'Display', 'final');
options = optimoptions(options,'OutputFcn',@save_iter);
options = optimoptions(options,'PlotFcn', {  @pswplotbestf @plot_swarm });
options = optimoptions(options,'UseVectorized', false);
options = optimoptions(options,'UseParallel', parallel);

%% run ga
[x,fval,exitflag,output] = ...
particleswarm(@f_objetivo,nvars,lb,ub,options);

optresult.x = x;
optresult.fval = fval;
optresult.exitflag = exitflag;
optresult.output = output;

clearvars x fval exitflag output

function exit = plot_swarm(optimValues,state)
    exit = false;
    pointsize = 10;
    Z = optimValues.swarmfvals;
    X = optimValues.swarm(:,1);
    Y = optimValues.swarm(:,6);
    figure(10);
    scatter(X, Y, pointsize, Z,'filled');
    colorbar;
    title('p_{alma}');
    xlabel('tip');
    ylabel('root');

    X = optimValues.swarm(:,2);
    Y = optimValues.swarm(:,7);
    figure(11);
    scatter(X, Y, pointsize, Z,'filled');
    colorbar;
    title('width');
    xlabel('tip');
    ylabel('root');

    X = optimValues.swarm(:,3);
    Y = optimValues.swarmfvals;
    figure(12);
    scatter(X, Y);
    title('thick_{alma}');
    xlabel('N� plates');
    ylabel('Fittnes');

    X = optimValues.swarm(:,4);
    Y = optimValues.swarmfvals;
    figure(13);
    scatter(X, Y);
    title('thick_{mc}');
    xlabel('N� plates');
    ylabel('Fittnes');

    X = optimValues.swarm(:,5);
    Y = optimValues.swarmfvals;
    figure(14);
    scatter(X, Y);
    title('thick_{mt}');
    xlabel('N� plates');
    ylabel('Fittnes');
    
    Z = optimValues.swarmfvals;
    X = optimValues.swarm(:,1);
    Y = optimValues.swarm(:,2);
    figure(15);
    scatter(X, Y, pointsize, Z,'filled');
    colorbar;
    title('tip');
    xlabel('p_{alma}');
    ylabel('width');
    
    X = optimValues.swarm(:,6);
    Y = optimValues.swarm(:,7);
    figure(16);
    scatter(X, Y, pointsize, Z,'filled');
    colorbar;
    title('root');
    xlabel('p_{alma}');
    ylabel('width');
end

function exit = save_iter(optimValues, state)
    save('run/iter_psw.mat','optimValues');
    exit = false;
end
