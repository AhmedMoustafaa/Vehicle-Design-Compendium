function phi = wing_torsion(panel, prop, load, mat)
sp = [panel.span];
Mt = load.Mt(load.i:end);
Am = [prop.area_media]; Am = Am(load.i:end);
t_c = [panel.t_caixao]; t_c = t_c(load.i:end);
h = [prop.height]; h = h(load.i:end);
w = [prop.width]; w = w(load.i:end);

dphidz = Mt.*2.*(h+w)./(4.*Am.^2.*mat.G.*t_c);
phi = cumtrapz(sp,dphidz);

end