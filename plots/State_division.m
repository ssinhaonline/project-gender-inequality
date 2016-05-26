%% Load dataset
dsStateDivision = dataset('File', '../fixtures/all_csv/State_division.csv', 'ReadVarNames', true, 'ReadObsNames', false, 'Delimiter', ',');
dsStateDivision.gender = nominal(dsStateDivision.gender);
dsStateDivision.stateAbbr = nominal(dsStateDivision.stateAbbr);
dsStateDivision.stateColor = nominal(dsStateDivision.stateColor);

%% Getting mean of overall score for males and females in Republican and Democratic states

meanRepublicanMale = mean(dsStateDivision(and(dsStateDivision.gender == 'M', dsStateDivision.stateColor == 'Republican'), :).ovr);
meanRepublicanFemale = mean(dsStateDivision(and(dsStateDivision.gender == 'F', dsStateDivision.stateColor == 'Republican'), :).ovr);
meanNeutralMale = mean(dsStateDivision(and(dsStateDivision.gender == 'M', dsStateDivision.stateColor == 'Neutral'), :).ovr);
meanNeutralFemale = mean(dsStateDivision(and(dsStateDivision.gender == 'F', dsStateDivision.stateColor == 'Neutral'), :).ovr);
meanDemocraticMale = mean(dsStateDivision(and(dsStateDivision.gender == 'M', dsStateDivision.stateColor == 'Democratic'), :).ovr);
meanDemocraticFemale = mean(dsStateDivision(and(dsStateDivision.gender == 'F', dsStateDivision.stateColor == 'Democratic'), :).ovr);

y = [meanRepublicanMale meanRepublicanFemale; meanNeutralMale meanNeutralFemale; meanDemocraticMale meanDemocraticFemale];

figurehandle = figure;
axeshandle = axes('Parent', figurehandle);
hold(axeshandle,'on');

barhandle = bar(y);

% Blue for male, red for female
set(barhandle(2),'DisplayName','Female','FaceColor',[1 0 0]);
set(barhandle(1),'BaseValue',3.7,'DisplayName','Male','FaceColor',[0 0 1]);

% Create ylabel
ylabel('Average score');

% Create title
title('Average scores obtained by male and female professors across US states');

box(axeshandle,'on');

% Set the remaining axes properties
set(axeshandle,'XTick',[1 2 3],'XTickLabel',{'Conservative','Neutral','Liberal'},...
    'YTick',[3.7 3.75 3.8],'YTickLabel',{'3.7','3.75','3.8'});

% Show legend
legendhandle = legend(axeshandle,'show');

