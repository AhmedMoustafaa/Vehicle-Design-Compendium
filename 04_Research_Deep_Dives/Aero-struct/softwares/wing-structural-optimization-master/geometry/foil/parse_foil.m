% Load foil name
load('data/run_config', 'foil_name');

% Read the .dat file
delimiter = ' ';
startRow = 2;
formatSpec = '%f%f%[^\n\r]';
fileID = fopen(['foils/' foil_name '.dat'],'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'MultipleDelimsAsOne', true, 'TextType', 'string', 'HeaderLines' ,startRow-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');
fclose(fileID);
dat = [dataArray{1:end-1}];
clearvars delimiter startRow formatSpec fileID dataArray ans;
% separate foil intra and extra (selig format)
[~, i] = min(dat(:,1));

int = dat(i:end,:);
ext = dat(1:i,:);

% rotate the foil (please do not use)
% Rot = [cosd(ang_rot) -sind(ang_rot); sind(ang_rot) cosd(ang_rot)];
% if ang_rot ~=0
%     % Translate the points to p_rot
%     ext(:,1) = ext(:,1) - p_rot;
%     int(:,1) = int(:,1) - p_rot;
% 
%     % Rotate
%     ext = Rot*ext';
%     ext = ext';
% 
%     int = Rot*int';
%     int = int';
% 
%     % Translate back
%     ext(:,1) = ext(:,1) + p_rot;
%     int(:,1) = int(:,1) + p_rot;
% end
% linear interpolation curve fit
ft = fittype('linearinterp');
[x, y] = prepareCurveData(ext(:,1), ext(:,2));
ex_lin = fit(x, y, ft);
[x, y] = prepareCurveData(int(:,1), int(:,2));
in_lin = fit(x, y, ft);
esp_in = abs(min(diff(int(:,1))));
esp_ex = abs(min(diff(ext(:,1))));
esp = min([esp_in esp_ex])*1e-1;


% % Translate the points to 1/4 of the chord in x
% ext(:,1) = ext(:,1) - 1/4;
% int(:,1) = int(:,1) - 1/4;
% 
% % Translate the points to camber line of the foil (y)
% [~,i] = min(abs(ext(:,1)));
% shift = int(i,2) + (ext(i,2) - int(i,2))/2;
% ext(:,1) = ext(:,1) + 1/4;
% int(:,1) = int(:,1) + 1/4;


save(['foils/' foil_name '.mat'], 'ex_lin', 'in_lin', 'ext', 'int', 'esp');
clearvars x y ft ex_lin in_lin esp_in esp_ex esp dat ext i int shift foil_name
