function [raw_fit] = weight_function(mass, safety_margin, report)
%WEIGHT_FUNCTION Summary of this function goes here
%   Detailed explanation goes here

if safety_margin <= 0
    gain = -1*mass/(1+safety_margin);
elseif safety_margin <= 1 && report < 1
    gain = 1.5;
elseif report >= 1
    gain = 0.5;
else
    gain = 1;
end

raw_fit = gain/mass;
raw_fit = -raw_fit;
end

