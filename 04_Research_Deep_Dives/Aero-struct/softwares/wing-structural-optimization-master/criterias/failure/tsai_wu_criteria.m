function ms = tsai_wu_criteria(sigma, mat, opt)

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

sigma1 = sigma(1,1);
sigma2 = sigma(2,2);
tau6 = sigma(1,2);

f1 = 1/F1t - 1/F1c;
f11 = 1/(F1t*F1c);

f2 = 1/F2t - 1/F2c;
f22 = 1/(F2t*F2c);

f66 = 1/F6^2;

f12 = -.5*sqrt(f11*f22);

fi = f1*sigma1 + f2*sigma2 + f11*sigma1^2 + f22*sigma2^2 + f66*tau6^2 + 2*f12*sigma1*sigma2;
a = f11*sigma1^2 + f22*sigma2^2 + f66*tau6^2 + f12*sigma1*sigma2;
b = f1*sigma1 + f2*sigma2;
rt = roots([a b -1]);
sf = max(rt);
ms = sf - 1;
