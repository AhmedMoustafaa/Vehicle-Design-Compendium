function [] = plot_esforcos( esforcos )
%PLOT_ESFORCOS Summary of this function goes here
%   Detailed explanation goes here

figure('Name', 'Esforcos');
subplot(2,2,1), plot(esforcos.s,esforcos.V,'-o'); grid on; title('Cortante');
subplot(2,2,2), plot(esforcos.s,esforcos.M, '-o'); grid on; title('Momento Fletor');
subplot(2,2,4), plot(esforcos.s,esforcos.Mt, '-o'); grid on; title('Momento Torsor');
subplot(2,2,3), plot(esforcos.s,esforcos.F, '-o'); grid on; title('Normal');
end

