function [phi] = ang_torcao_macico(T, G, Ip, l)
%ANG_TORCAO_MACICO Calcula o angulo de torcao no ponto l
% a partir da funcao do Torque e momento polar de inercia
if isnumeric(T)
    T = @(x) x.*0 + T;
end
if isnumeric(Ip)
    Ip = @(x) x.*0 + Ip;
end
phi = integral(@(x) T(x)./(G*Ip(x)), 0, l);
end

