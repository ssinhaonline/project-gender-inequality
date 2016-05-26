%% Load tags distribution dataset

maleTagsDistribution = dataset('File', '../fixtures/all_csv/male_tags_distribution.csv', 'ReadVarNames', true, 'ReadObsNames', false, 'Delimiter', ';');
femaleTagsDistribution = dataset('File', '../fixtures/all_csv/female_tags_distribution.csv', 'ReadVarNames', true, 'ReadObsNames', false, 'Delimiter', ';');

numRows = size(maleTagsDistribution, 1);
for RowIter = 1 : numRows
    maleTagsDistribution.Color{RowIter} = 'M';
end
clear numRows RowIter

maleTagsDistribution(:,'Angle') = [];
maleTagsDistribution(:,'Font') = [];
maleTagsDistribution(:,'Repeat_') = [];
maleTagsDistribution.Properties.VarNames{3} = 'Gender';

numRows = size(femaleTagsDistribution, 1);
for RowIter = 1 : numRows
    femaleTagsDistribution.Color{RowIter} = 'F';
end
clear numRows RowIter

femaleTagsDistribution(:,'Angle') = [];
femaleTagsDistribution(:,'Font') = [];
femaleTagsDistribution(:,'Repeat_') = [];
femaleTagsDistribution.Properties.VarNames{3} = 'Gender';

allTagsDistribution = vertcat(maleTagsDistribution, femaleTagsDistribution);
allTagsDistribution.Gender = nominal(allTagsDistribution.Gender);
clear maleTagsDistribution femaleTagsDistribution

%% Grouped Bar Plot

% Create input
n = [allTagsDistribution.Weight(allTagsDistribution.Gender == 'M') allTagsDistribution.Weight(allTagsDistribution.Gender == 'F')];

% Create figure and axes handle
figurehandle = figure;
axeshandle = axes('Parent', figurehandle);
hold(axeshandle, 'on')

% Plot horizontal bar
barhandle = barh(n, 'grouped');
set(barhandle(1),'DisplayName','M','FaceColor','b');
set(barhandle(2),'DisplayName','F','FaceColor','r');

% Name bars on Y axis
set(axeshandle,'XAxisLocation','top','YTick',...
    [0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21],'YTickLabel',...
    {'','Clear grading criteria','Gives good feedback','Tough grader','Lectures are long','Gives Pop Quizzes','Expect Homework','Tests? Not many','Amazing lectures','Tests are tough','There for you','Beware of group projects','Assigns long papers','Participation matters','Get ready to read','Inspirational','Hilarious','Skip class? You won''t pass','Would take again','Gives extra credit','Respected by students',''});

% Set the remaining axes properties

ylim(axeshandle,[0 21]);
box(axeshandle,'on');
axis(axeshandle,'ij');

% Create legend
legend(axeshandle,'show');

% Create title
title({'Distribution of tags received by Male and Female Professors'});

clearvars

%% Load top tags distribution dataset

maleTagsDistribution = dataset('File', '../fixtures/all_csv/male_top_20_tags.csv', 'ReadVarNames', true, 'ReadObsNames', false, 'Delimiter', ',');
femaleTagsDistribution = dataset('File', '../fixtures/all_csv/female_top_20_tags.csv', 'ReadVarNames', true, 'ReadObsNames', false, 'Delimiter', ',');

numRows = size(maleTagsDistribution, 1);
for RowIter = 1 : numRows
    maleTagsDistribution.Color{RowIter} = 'M';
end
clear numRows RowIter

maleTagsDistribution(:,'Angle') = [];
maleTagsDistribution(:,'Font') = [];
maleTagsDistribution(:,'Repeat_') = [];
maleTagsDistribution.Properties.VarNames{3} = 'Gender';

numRows = size(femaleTagsDistribution, 1);
for RowIter = 1 : numRows
    femaleTagsDistribution.Color{RowIter} = 'F';
end
clear numRows RowIter

femaleTagsDistribution(:,'Angle') = [];
femaleTagsDistribution(:,'Font') = [];
femaleTagsDistribution(:,'Repeat_') = [];
femaleTagsDistribution.Properties.VarNames{3} = 'Gender';

allTagsDistribution = vertcat(maleTagsDistribution, femaleTagsDistribution);
allTagsDistribution.Gender = nominal(allTagsDistribution.Gender);
clear maleTagsDistribution femaleTagsDistribution

%% Grouped Bar Plot

% Create input
n = [allTagsDistribution.Weight(allTagsDistribution.Gender == 'M') allTagsDistribution.Weight(allTagsDistribution.Gender == 'F')];

% Create figure and axes handle
figurehandle = figure;
axeshandle = axes('Parent', figurehandle);
hold(axeshandle, 'on')

% Plot horizontal bar
barhandle = barh(n, 'grouped');
set(barhandle(1),'DisplayName','M','FaceColor','b');
set(barhandle(2),'DisplayName','F','FaceColor','r');

% Name bars on Y axis
set(axeshandle,'XAxisLocation','top','YTick',...
    [0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21],'YTickLabel',...
    {'','Clear grading criteria','Gives good feedback','Tough grader','Lectures are long','Gives Pop Quizzes','Expect Homework','Tests? Not many','Amazing lectures','Tests are tough','There for you','Beware of group projects','Assigns long papers','Participation matters','Get ready to read','Inspirational','Hilarious','Skip class? You won''t pass','Would take again','Gives extra credit','Respected by students',''});

% Set the remaining axes properties

ylim(axeshandle,[0 21]);
box(axeshandle,'on');
axis(axeshandle,'ij');

% Create legend
legend(axeshandle,'show');

% Create title
title({'Distribution of top 3 tags received by Male and Female Professors'});

clearvars
