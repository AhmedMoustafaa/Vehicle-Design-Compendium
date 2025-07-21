function mat = material_properties(nome)
switch nome
    case 'carbono_bi'
        mat.axial_trac  = 6.82e08;  % Pa <= 682 MPa
        mat.axial_comp  = 3.41e08;  % Pa <= 341 MPa
        mat.axial_E     = 5.10e10;  % Pa <= 51000 MPa
        mat.axial_poison= 0.28;     % adm <= 0.28
        mat.trans_trac  = 6.82e08;  % Pa <= 682 MPa
        mat.trans_comp  = 3.41e08;  % Pa <= 341 MPa
        mat.trans_E     = 4.8929e10;  % Pa <= 48929 MPa
        mat.trans_poison= 0.02;     % adm <= 0.28
        mat.G           = 2.00e09;  % Pa <= 2000 MPa
        mat.shear       = 7.20e07;  % Pa <= 72 MPa
        mat.dens        = 1545;     % Kg*m^-3 <= 1545 Kg*m^-3
    case 'carbono_uni'
        mat.axial_trac  = 1.13e09;  % Pa <= 1130 MPa
        mat.axial_comp  = 3.41e08;  % Pa <= 341 MPa
        mat.axial_E     = 9.43e10;  % Pa <= 94300 MPa
        mat.axial_poison= 0.33;     % adm <= 0.33
        mat.trans_trac  = 4.30e08;  % Pa <= 43 MPa
        mat.trans_comp  = 1.33e08;  % Pa <= 133 MPa
        mat.trans_E     = 3.25e09;  % Pa <= 3250 MPa
        mat.trans_poison= 0.03;     % adm <= 0.33
        mat.G           = 1.98e09;  % Pa <= 1980 MPa
        mat.shear       = 6.00e07;  % Pa <= 60 MPa
        mat.dens        = 1500;     % Kg*m^-3
    case 'balsa'
        mat.axial_trac  = 4.00e07;  % Pa <= 40 MPa
        mat.axial_comp  = 6.90e06;  % Pa <= 6.9 MPa
        mat.axial_E     = 4.10e09;  % Pa <= 4100 MPa
        mat.trans_trac  = 8.00e05;  % Pa <= 0.8 MPa
        mat.trans_comp  = 1.00e05;  % Pa (sem dados confiaveis)
        mat.trans_E     = 9.50e07;  % Pa <= 95 MPa
        mat.G           = 1.66e08;  % Pa <= 166 MPa
        mat.shear       = 1.30e06;  % Pa <= 1.3 MPa
        mat.poison      = 0.25;     % adm
        mat.dens        = 0150;     % Kg*m^-3
    case 'freijo'
        mat.axial_trac  = 1.02e08;  % Pa <=
        mat.axial_comp  = 4.50e07;  % Pa
        mat.axial_E     = 1.60e10;  % Pa
        mat.trans_trac  = 4.20e06;  % Pa
        mat.trans_comp  = 2.00e06;  % Pa (sem dados, usando spruce)
        mat.trans_E     = 9.00e08;  % Pa (sem dados, usando spruce)
        mat.G           = 3.50e09;  % Pa (sem dados, usando spruce)
        mat.shear       = 8.70e06;  % Pa
        mat.poison      = 0.30;     % adm
%         mat.dens        = 0610;     % Kg*m^-3
        mat.dens        = 0362;     % vareta de freijo
%         mat.dens        = 0593;     % tora de freijo
%         mat.dens        = 0452;     % vara de compensado
end