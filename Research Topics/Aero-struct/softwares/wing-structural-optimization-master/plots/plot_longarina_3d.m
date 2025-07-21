function [] = plot_longarina_3d(data)

panels = data.panels;
props = data.props;
wing = data.wing;
lg = data.long_geo;

figure('Name', 'Geometria 3D');
set(gca, 'ydir', 'reverse');
hold on; axis equal; view(-45, 45);
a1 = zeros(length(panels),2);
b1 = zeros(length(lg.chords),2);
a2 = a1; a3 = a1; a4 = a1; a5 = a1; a6 = a1; a7 = a1; a8 = a1;
b2 = b1; b3 = b1; b4 = b1; b5 = b1; b6 = b1; b7 = b1; b8 = b1;

%% plot wing sections

sp = [wing.spans lg.spans(2)];
c = [wing.chords lg.chords(2)];

for i=1:length(c)
    foil = get_foil_prop(c(i), 0, [0 1], [0 0]);
    % perfil
    le = length(foil.ex); li = length(foil.in);
    ze = ones(le,1)*sp(i); zi = ones(li,1)*sp(i);
    plot3(foil.ex(:,1), ze, foil.ex(:,2), 'black', foil.in(:,1), zi, foil.in(:,2),  'black');
    plot3(foil.ex(:,1), -ze, foil.ex(:,2), 'black', foil.in(:,1), -zi, foil.in(:,2),  'black');
end

%% plot spar

c = [panels.chord];
mc_t = [panels.t_mc];
mt_t = [panels.t_mt];
a_t = [panels.t_alma];
s = [panels.span];
l = [panels.limits];
l = vertcat(l(1:2:end), l(2:2:end));
vert = [props.vertices];
vert = reshape(vert,4,2,[]);

for i = 1:length(panels)
    
    % mesas
    z = ones(5,1)*s(i);
    X = [vert(1:2,1,i)' vert(4,1,i)' vert(3,1,i) vert(1,1,i)'];
    Y = [vert(1:2,2,i)' vert(4,2,i)' vert(3,2,i) vert(1,2,i)'];
    X_i = X + [1 -1 -1 1 1]*a_t(i);
    Y_i = Y + horzcat(mc_t(i)*[-1 -1], mt_t(i)*[1 1], -mc_t(i));
    plot3(X,z,Y, 'blue');
    plot3(X_i,z,Y_i, 'blue--');
    plot3(X,-z,Y, 'blue');
    plot3(X_i,-z,Y_i, 'blue--');

    a1(i,:) = [X(1) Y(1)]; a2(i,:) = [X(2) Y(2)];
    a3(i,:) = [X(3) Y(3)]; a4(i,:) = [X(4) Y(4)];
    a5(i,:) = [X_i(1) Y_i(1)]; a6(i,:) = [X_i(2) Y_i(2)];
    a7(i,:) = [X_i(3) Y_i(3)]; a8(i,:) = [X_i(4) Y_i(4)];
end

%% plot spar relevant sections

% plot on parametric positions
for i=1:length(lg.chords)
    panel.span = lg.spans(i);
    panel.chord = lg.chords(i);
    panel.limits = lg.limits(:,i);
    panel.t_alma = lg.t_alma(i);
    panel.t_mc = lg.t_mc(i);
    panel.t_mt = lg.t_mt(i);
    
    prop_d(i) = sec_caixao_retangular(panel);
    vert = prop_d(i).vertices;
    
    z = ones(5,1)*panel.span;
    X = [vert(1:2,1)' vert(4,1)' vert(3,1) vert(1,1)'];
    Y = [vert(1:2,2)' vert(4,2)' vert(3,2) vert(1,2)'];
    X_i = X + [1 -1 -1 1 1]*panel.t_alma;
    Y_i = Y + horzcat(panel.t_mc*[-1 -1], panel.t_mt*[1 1], -panel.t_mc);
    plot3(X,z,Y, 'blue');
    plot3(X_i,z,Y_i, 'blue--');
    plot3(X,-z,Y, 'blue');
    plot3(X_i,-z,Y_i, 'blue--');

    b1(i,:) = [X(1) Y(1)]; b2(i,:) = [X(2) Y(2)];
    b3(i,:) = [X(3) Y(3)]; b4(i,:) = [X(4) Y(4)];
    b5(i,:) = [X_i(1) Y_i(1)]; b6(i,:) = [X_i(2) Y_i(2)];
    b7(i,:) = [X_i(3) Y_i(3)]; b8(i,:) = [X_i(4) Y_i(4)];
    
end

% plot on afil section
panel.span = wing.spans(2);
panel.chord = wing.chords(2);
panel.limits = [interp1(s, l(1,:), panel.span); interp1(s, l(2,:), panel.span)];
panel.t_alma = interp1(lg.spans,lg.t_alma,panel.span);
panel.t_mc = interp1(lg.spans,lg.t_mc,panel.span);
panel.t_mt = interp1(lg.spans,lg.t_mt,panel.span);

prop_c = sec_caixao_retangular(panel);
vert = prop_c.vertices;

z = ones(5,1)*panel.span;
X = [vert(1:2,1)' vert(4,1)' vert(3,1) vert(1,1)'];
Y = [vert(1:2,2)' vert(4,2)' vert(3,2) vert(1,2)'];
X_i = X + [1 -1 -1 1 1]*panel.t_alma;
Y_i = Y + horzcat(panel.t_mc*[-1 -1], panel.t_mt*[1 1], -panel.t_mc);
plot3(X,z,Y, 'blue');
plot3(X_i,z,Y_i, 'blue--');
    
%% plot spar lines
a1 = [b1(1,:); a1; b1(end,:)];
a2 = [b2(1,:); a2; b2(end,:)];
a3 = [b3(1,:); a3; b3(end,:)];
a4 = [b4(1,:); a4; b4(end,:)];
s = [lg.spans(1) s lg.spans(end)];

plot3(a1(:,1),s,a1(:,2),'blue'); plot3(a2(:,1),s,a2(:,2),'blue');
plot3(a1(:,1),-s,a1(:,2),'blue'); plot3(a2(:,1),-s,a2(:,2),'blue');
plot3(a3(:,1),s,a3(:,2),'blue'); plot3(a4(:,1),s,a4(:,2),'blue');
plot3(a3(:,1),-s,a3(:,2),'blue'); plot3(a4(:,1),-s,a4(:,2),'blue');
% plot3(a5(:,1),s,a5(:,2),'blue--'); plot3(a6(:,1),s,a6(:,2),'blue--');
% plot3(a7(:,1),s,a7(:,2),'blue--'); plot3(a8(:,1),s,a8(:,2),'blue--');


vert = [[props.vertices_lm] prop_d(end).vertices_lm];
vert = reshape(vert,4,2,[]);
X = reshape(vert(:,1,:),1,[]);
Y = reshape(vert(:,2,:),1,[]);
Z = repelem([[panels.span] lg.spans(end)],4);
XYZ = [X' Y' Z']*1000;
save('long_data_points','XYZ');

end