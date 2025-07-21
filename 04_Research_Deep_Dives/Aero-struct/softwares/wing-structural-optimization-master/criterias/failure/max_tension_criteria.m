function ms = max_tension_criteria(sigma, mat, opt)

ms = zeros(3,1);

sigma1 = sigma(1,1);
sigma2 = sigma(2,2);
tau6 = sigma(1,2);

switch opt
    case 'axial'
        F1t = mat.axial_trac;
        F1c = mat.axial_comp;
        F2t = mat.trans_trac;
        F2c = mat.trans_comp;
    case 'trans'
        F2t = mat.axial_trac;
        F2c = mat.axial_comp;
        F1t = mat.trans_trac;
        F1c = mat.trans_comp;
end
F6 = mat.shear;

if sigma1 >= 0
    ms(1) = F1t/sigma1 - 1;
else
    ms(1) = -F1c/sigma1 - 1;
end

if sigma2 >= 0
    ms(2) = F2t/sigma2 - 1;
else
    ms(2) = -F2c/sigma2 - 1;
end

ms(3) = abs(F6/tau6) - 1;
inf = (ms == -Inf)|(ms == Inf);
ms = min(ms(~inf));