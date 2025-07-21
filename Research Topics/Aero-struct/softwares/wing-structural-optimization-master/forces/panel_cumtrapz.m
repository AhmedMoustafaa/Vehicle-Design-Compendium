function [s, w] = panel_cumtrapz(s, w)
% PANEL_CUMTRAPZ This function performs cummulative trapezoidal integration
%
% ATTENTION:
% This is waste of time, not wasting mine anymore. Please use cumtrapz with
% zero at the tips. I will leave here for historic porpuse.
%
% Those next lines performs a diffrent kind ofcummulative trapezoidal
% integration.
%
% To understand why a convencional trapezoidal integration wasn't made, one
% must understande that the input force loads acts upon a area of a
% aerodynamic panel.
%
% If a cumtrapz is directly made with raw distributed load forces and
% positions the result will be different from the concentrated forces
% solution, therefore a not desired solution.
%
% One way to counter this is adding the zero lift points at the tips in the
% load array, so the total solution will be satisfatory. But there is other
% way of distribute the load so it get more physically compatible.
%
% When the load force is divided by the span-wise length of the panel we
% get the exact constant distributed load for that panel. But a constant
% distributed load for each panel make the overall distribution
% discontinous (with steps), and it isn't very apropriated representation
% of the lift load, as it is almost continous. For the shear forces, it's
% ok to use the convencional trapezoidal representation (with the zero
% valued tips), it gives the same output, but for the bending moment one
% can use linear representations of the distribution in each panel with a
% equivalent below area.
%
% w_i(s) = F/l ==> constant distribution
% w_i(s) = a*s + b ==> linear distribution
% were
% a = (w(i) - w(i-1)) / (s(i) - s(i-1))
% b = (s(i)*w(i-1) - s(i-1)*w(i)) / (s(i) - s(i-1))
% 
% integral of w_i(s) ds from s(i-1) to 2*(s(i) - s(i-1))
% == (1/2) * (2*a*s(i-1) - 3*a*s(i) - 2*b) * (2*s(i-1) -s(i))
% 
% integral of w_i(s)*s ds from s(i-1) to (2*s(i) - s(i-1))
% == (
%
%
% It is clear that with the increase of N (number of panels) there is no
% need for this methodo as the two types of integrals converges to the same
% value. But in this method of distribution the cumutalive integral is 
% smaller than the traditional trapezoidal integration.
%
%

%w_i = w(2:end);
%w_i_minus = w(1:end-1);
%s_i = s(2:end);
%s_i_minus = s(1:end-1);

for i = 2:length(w)
    a = (w(i) - w(i-1)) / (s(i) - s(i-1));
    b = (s(i)*w(i-1) - s(i-1)*w(i)) / (s(i) - s(i-1));
    s_i_plus = 2*s(i) - s(i-1);
    w_i_plus = a*(s_i_plus) + b;
    w(i) = w_i_plus;
    s(i) = s_i_plus;
end

%w_int =  0;
%ws_int = (1/3)*(w_i - w_i_minus).*(s_i.^2 + s_i.*s_i_minus + s_i_minus.^2) + ...
%         (1/2)*(s_i.*w_i_minus - s_i_minus.*w_i).*(s_i.^2 - s_i_minus.^2)./(s_i - s_i_minus);
end

