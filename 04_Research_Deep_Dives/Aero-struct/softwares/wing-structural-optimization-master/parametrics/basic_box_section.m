function [section] = basic_box_section(root, tip)
%BASIC_BOX_PARAMETRICS Summary of this function goes here
%   section.x_position -> position of the frontmost box web
%   section.width -> width of the section
%   section.box_thickness 

x_position = [root.position*root.chord - root.chord/4, ...
              tip.position*tip.chord - tip.chord/4];
section.x_position = x_position;
               
section.width = [root.width*root.chord, ...
                 tip.width*tip.chord];
              
section.thickness = [root.thickness, tip.thickness];

chords = [root.chord tip.chord];

section.chords = chords;

section.limits = [(x_position + chords/4); ...
                  (x_position + chords/4 + section.width)];
section.limits = [{section.limits(1,:)'}, {section.limits(2,:)'}];

end

