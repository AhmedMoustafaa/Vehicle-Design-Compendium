function [] = plot_longarina(data)
%PLOT_LONGARINA Summary of this function goes here
%   Detailed explanation goes here

panels = data.panels;
wing = data.wing;
lg = data.long_geo;

%% vista superior
figure('Name', 'Geometria Vista Superior'); hold on; axis equal; grid on; set(gca, 'ydir', 'reverse');

% plot da asa
sp = wing.spans;
c = wing.chords;
for i=1:length(c)
    plot(sp(i)*[1 1], [-c(i)*.25 c(i)*.75], 'black--');
end
cd = interp1(sp,c,wing.d/2);
plot(wing.d*[.5 .5], [-cd*.25 cd*.75], 'black');
plot(sp, c*.75, 'black--');
plot(sp, -c*.25, 'black--');

% plot da longarina
c = [lg.chords(1) panels.chord lg.chords(end)];
a = [lg.limits(:,1)' [panels.limits] lg.limits(:,end)'];
a = [a(1:2:end).*c; a(2:2:end).*c];
s = [lg.spans(1) panels.span lg.spans(end)];
for i=1:length(c)
    plot(s(i)*[1 1], a(:,i)' - c(i)*[1 1]/4, 'b');
end
plot(s, a(2,:)-c/4, 'b');
plot(s, a(1,:)-c/4, 'b');
end

