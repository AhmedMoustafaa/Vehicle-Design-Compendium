function [It] = translate_inertia_tensor(I, d, A)
%TRANSLADA_EIXO Translada os valores do Tensor de Inercias I para
%eixos a distâncias (dx e dy)
%
It = [ I(1,1)+d(1).^2*A  prod(d)*A+I(1,2)  ; ...
       prod(d)*A+I(2,1)  I(2,2)+d(2).^2*A ];
end

