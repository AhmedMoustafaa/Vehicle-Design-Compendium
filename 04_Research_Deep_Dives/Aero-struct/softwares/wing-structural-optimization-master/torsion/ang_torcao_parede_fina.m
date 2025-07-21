function [phi_total, dphi_dx] = ang_torcao_parede_fina(Torque, thick, s, Am, G, lim)
% ANG_TORCAO_PAREDE_FINA Calcula o angulo total de torcao ou a variacao do
% angulo no comprimento
%   Torque -> Torque total ou distribuido
%   thick -> distribuicao de espessura da secao (pode ser um cell)
%   s -> comprimentos da secao (pode ser um cell)
%   Am -> area media da secao
%   G -> modulo de resistencia a torcao
%   L -> comprimento total na envergadura

int = integral_linha_media(thick, s);
if isnumeric(Torque)
    Torque = @(x) x.*0 + Torque;
end
dphi_dx = @(x) Torque(x).*int./(4*G.*Am.^2);
phi_total = integral(dphi_dx, lim(1), lim(2));
end

