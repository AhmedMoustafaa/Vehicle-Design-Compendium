function ms = tsai_hill_criteria(sigma, mat)

F1t = mat.axial_trac;
F1c = mat.axial_comp;
F2t = mat.trans_trac;
F2c = mat.trans_comp;
F6 = mat.shear;

sigma1 = sigma(1,1);
sigma2 = sigma(2,2);
tau6 = sigma(1,2);

if sigma(1,1) > 0
    F1 = F1t;
else
    F1 = F1c;
end

if sigma(2,2) > 0
    F2 = F2t;
else
    F2 = F2c;
end

A = 1/F1^2;
B = 1/F2^2;
C = -A;
D = 1/F6^2;

ms = A*sigma1^2 + B*sigma2^2 + C*sigma1*sigma2 + D*tau6^2;
