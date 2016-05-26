function plot_props_score_v_size(X1, YMatrix1, G1, G2)
%plot_props_fscore_v_msize(X1, YMATRIX1)
%  X1:  vector of x data
%  YMATRIX1:  matrix of y data
%  G1: character of x population size
%  G2: character of y scores

%  Auto-generated by MATLAB on 12-Feb-2016 09:46:19

% Create figure
figure1 = figure;

% Create axes
axes1 = axes('Parent',figure1);
hold(axes1,'on');

% Create multiple lines using matrix input to semilogx
semilogx1 = semilogx(X1,YMatrix1,'Parent',axes1);
set(semilogx1(1),'DisplayName','Overall');
set(semilogx1(2),'DisplayName','Clarity');
set(semilogx1(3),'DisplayName','Easiness');
set(semilogx1(4),'DisplayName','Helpfulness');

%Determine sexes
if G1 == 'M'
    gender1 = 'Male'
    gender2 = 'Female'
else
    gender1 = 'Female'
    gender2 = 'Male'
end

% Create xlabel
xlabel(strcat(gender1, ' population size'));

% Create ylabel
ylabel(strcat(gender2, ' average score'));

% Create title
title(strcat(gender2, ' average scores vs discipline ', gender1, ' population'));

box(axes1,'on');
% Set the remaining axes properties
set(axes1,'XScale','linear');
% Create legend
legend1 = legend(axes1,'show');
set(legend1,...
    'Position',[0.741148229908655 0.767324284842468 0.0937269357077752 0.133597880049988]);

