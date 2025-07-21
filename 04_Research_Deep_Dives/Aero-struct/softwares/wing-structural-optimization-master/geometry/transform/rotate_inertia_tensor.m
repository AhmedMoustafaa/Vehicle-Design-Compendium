function [Ir] = rotate_inertia_tensor(I, theta)
%ROTACIONA_EIXO Rotaciona os valores do Tensor de Inercias em
%um angulo theta em radianos

Ir = zeros(2);
Ir(1,1) = .5*(I(1,1)+I(2,2)) + .5*(I(2,2) - I(1,1))*cos(2*theta) + I(1,2)*sin(2*theta);
Ir(2,2) = .5*(I(1,1)+I(2,2)) + .5*(I(1,1) - I(2,2))*cos(2*theta) - I(2,1)*sin(2*theta);
Ir(1,2) = .5*(I(1,1)-I(2,2))*sin(2*theta) + I(1,2)*cos(2*theta);
Ir(2,1) = .5*(I(1,1)-I(2,2))*sin(2*theta) + I(2,1)*cos(2*theta);
end

