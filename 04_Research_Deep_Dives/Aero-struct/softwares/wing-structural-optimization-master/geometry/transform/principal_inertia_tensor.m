function [Ip,theta_p] = principal_inertia_tensor(I)
%CALC_INERCIA_PRINCIPAL Calcula o Tensor de Inercias Principal e
%seu angulo a partir de um Tensor de Inercias, usando o Circulo de Mohr
Imed = mean(diag(I));
R = sqrt((.5*diff(diag(I)))^2 + I(1,2)^2);
Ip = zeros(2);
Ip(1,1) = Imed + R;
Ip(2,2) = Imed - R;
theta_p = .5*atan(abs(2*I(1,2)/diff(diag(I))));
end

