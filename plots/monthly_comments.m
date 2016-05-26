%% Load monthly distribution of comments dataset
monthlyCommentsDistribution = dataset('File', '../fixtures/all_csv/monthly_comments_distribution.csv', 'ReadVarNames', true, 'ReadObsNames', false, 'Delimiter', ',');
monthlyCommentsDistribution.gender = nominal(monthlyCommentsDistribution.gender);

%% Plot number of comments by month
% Create figure
figurehandle = figure;

% Create axes
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

% Create multiple lines using two plot functions
maleplothandle = plot(monthlyCommentsDistribution.month(monthlyCommentsDistribution.gender == 'M', :), smooth(monthlyCommentsDistribution.num_comments(monthlyCommentsDistribution.gender == 'M', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% maleplothandle = plot(monthlyCommentsDistribution.month(monthlyCommentsDistribution.gender == 'M', :), (monthlyCommentsDistribution.num_comments(monthlyCommentsDistribution.gender == 'M', :)));

set(maleplothandle,'DisplayName','Male');
hold on;

femaleplothandle = plot(monthlyCommentsDistribution.month(monthlyCommentsDistribution.gender == 'F', :), smooth(monthlyCommentsDistribution.num_comments(monthlyCommentsDistribution.gender == 'F', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% femaleplothandle = plot(monthlyCommentsDistribution.month(monthlyCommentsDistribution.gender == 'F', :), (monthlyCommentsDistribution.num_comments(monthlyCommentsDistribution.gender == 'F', :)));

set(femaleplothandle,'DisplayName','Female');

% Create xlabel
xlabel('Month');

% Create ylabel
ylabel('Number of comments');

% Create title
title('Number of Comments by month');

box(axeshandle,'on');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});

% Create legend
legend(axeshandle,'show');
%% Clear variables

clearvars;

%% Load monthly distribution of scores dataset
monthlyRatingsDistribution = dataset('File', './monthly_average_scores_distribution_MFprofs+goodgrades.csv', 'ReadVarNames', true, 'ReadObsNames', false, 'Delimiter', ',');
monthlyRatingsDistribution.gender = nominal(monthlyRatingsDistribution.gender);

%% Plot average clarity scores by month
% Create figure
figurehandle = figure;

% Create axes
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

% Create multiple lines using two plot functions
maleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'M', :), smooth(monthlyRatingsDistribution.avg_clarity(monthlyRatingsDistribution.gender == 'M', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% maleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'M', :), (monthlyRatingsDistribution.avg_clarity(monthlyRatingsDistribution.gender == 'M', :)));

set(maleplothandle,'DisplayName','Male');
hold on;

femaleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'F', :), smooth(monthlyRatingsDistribution.avg_clarity(monthlyRatingsDistribution.gender == 'F', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
%femaleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'F', :), (monthlyRatingsDistribution.avg_clarity(monthlyRatingsDistribution.gender == 'F', :)));

set(femaleplothandle,'DisplayName','Female');

% Create xlabel
xlabel('Month');

% Create ylabel
ylabel('Average Clarity score');

% Create title
title('Clarity score vs month');

% Set Y-limits
ylim(axeshandle,[3 4]);

box(axeshandle,'on');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});

% Create legend
legend(axeshandle,'show');

%% Plot average easiness scores by month
% Create figure
figurehandle = figure;

% Create axes
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

% Create multiple lines using two plot functions
maleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'M', :), smooth(monthlyRatingsDistribution.avg_easiness(monthlyRatingsDistribution.gender == 'M', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% maleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'M', :), (monthlyRatingsDistribution.avg_easiness(monthlyRatingsDistribution.gender == 'M', :)));

set(maleplothandle,'DisplayName','Male');
hold on;

femaleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'F', :), smooth(monthlyRatingsDistribution.avg_easiness(monthlyRatingsDistribution.gender == 'F', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% femaleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'F', :), (monthlyRatingsDistribution.avg_easiness(monthlyRatingsDistribution.gender == 'F', :)));

set(femaleplothandle,'DisplayName','Female');

% Create xlabel
xlabel('Month');

% Create ylabel
ylabel('Average Easiness score');

% Create title
title('Easiness score vs month');

% Set Y-limits
ylim(axeshandle,[3 4]);

box(axeshandle,'on');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});

% Create legend
legend(axeshandle,'show');

%% Plot average helpfulness scores by month
% Create figure
figurehandle = figure;

% Create axes
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

% Create multiple lines using two plot functions
maleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'M', :), smooth(monthlyRatingsDistribution.avg_helpfulness(monthlyRatingsDistribution.gender == 'M', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% maleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'M', :), (monthlyRatingsDistribution.avg_helpfulness(monthlyRatingsDistribution.gender == 'M', :)));

set(maleplothandle,'DisplayName','Male');
hold on;

femaleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'F', :), smooth(monthlyRatingsDistribution.avg_helpfulness(monthlyRatingsDistribution.gender == 'F', :), 3));

% Uncomment next line and comment previous line for unsmoothed line 
% femaleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'F', :), (monthlyRatingsDistribution.avg_helpfulness(monthlyRatingsDistribution.gender == 'F', :)));

set(femaleplothandle,'DisplayName','Female');

% Create xlabel
xlabel('Month');

% Create ylabel
ylabel('Average Helpfulness score');

% Create title
title('Helpfulness score vs month');

% Set Y-limits
ylim(axeshandle,[3 4]);


% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});

% Create legend
legend(axeshandle,'show');

%% Plot average interest levels by month
% Create figure
figurehandle = figure;

% Create axes
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

% Create multiple lines using two plot functions
maleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'M', :), smooth(monthlyRatingsDistribution.avg_interest(monthlyRatingsDistribution.gender == 'M', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% maleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'M', :), (monthlyRatingsDistribution.avg_interest(monthlyRatingsDistribution.gender == 'M', :)));

set(maleplothandle,'DisplayName','Male');
hold on;

femaleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'F', :), smooth(monthlyRatingsDistribution.avg_interest(monthlyRatingsDistribution.gender == 'F', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% femaleplothandle = plot(monthlyRatingsDistribution.month(monthlyRatingsDistribution.gender == 'F', :), (monthlyRatingsDistribution.avg_interest(monthlyRatingsDistribution.gender == 'F', :)));

set(femaleplothandle,'DisplayName','Female');

% Create xlabel
xlabel('Month');

% Create ylabel
ylabel('Average Interest levels');

% Create title
title('Interest levels vs month');

% Set Y-limits
ylim(axeshandle,[3 4]);

box(axeshandle,'on');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});

% Create legend
legend(axeshandle,'show');

%% Clear variables

clearvars;

%% Load best and worst scores by month dataset

monthlyBestWorstScoresDistribution = dataset('File', './monthwise_best_worst_scores_distribution_MFprofs2.csv', 'ReadVarNames', true, 'ReadObsNames', false, 'Delimiter', ',');
monthlyBestWorstScoresDistribution.gender = nominal(monthlyBestWorstScoresDistribution.gender);

%% Plot monthwise best clarity distribution

% Create figure
figurehandle = figure;

% Create axes
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

% Create multiple lines using two plot functions
maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), smooth(monthlyBestWorstScoresDistribution.best_clarity(monthlyBestWorstScoresDistribution.gender == 'M', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), (monthlyBestWorstScoresDistribution.best_clarity(monthlyBestWorstScoresDistribution.gender == 'M', :)));

set(maleplothandle,'DisplayName','Male');
hold on;

femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), smooth(monthlyBestWorstScoresDistribution.best_clarity(monthlyBestWorstScoresDistribution.gender == 'F', :), 3));
% Uncomment next line and comment previous line for unsmoothed line
% femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), (monthlyBestWorstScoresDistribution.best_clarity(monthlyBestWorstScoresDistribution.gender == 'F', :)));

set(femaleplothandle,'DisplayName','Female');

% Create xlabel
xlabel('Month');

% Create ylabel
ylabel('Professor density');

% Create title
title('Best months for Clarity');

box(axeshandle,'on');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});

% Set Y limits
ylim(axeshandle,[0 0.5]);

% Create legend
legend(axeshandle,'show');

%% Plot monthwise worst clarity distribution

% Create figure
figurehandle = figure;

% Create axes
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

% Create multiple lines using two plot functions
maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), smooth(monthlyBestWorstScoresDistribution.worst_clarity(monthlyBestWorstScoresDistribution.gender == 'M', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), (monthlyBestWorstScoresDistribution.worst_clarity(monthlyBestWorstScoresDistribution.gender == 'M', :)));

set(maleplothandle,'DisplayName','Male');
hold on;

femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), smooth(monthlyBestWorstScoresDistribution.worst_clarity(monthlyBestWorstScoresDistribution.gender == 'F', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), (monthlyBestWorstScoresDistribution.worst_clarity(monthlyBestWorstScoresDistribution.gender == 'F', :)));

set(femaleplothandle,'DisplayName','Female');

% Create xlabel
xlabel('Month');

% Create ylabel
ylabel('Professor density');

% Create title
title('Worst months for Clarity');

box(axeshandle,'on');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});

% Set Y limits
ylim(axeshandle,[0 0.5]);

% Create legend
legend(axeshandle,'show');

%% Plot monthwise best easiness distribution

% Create figure
figurehandle = figure;

% Create axes
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

% Create multiple lines using two plot functions
maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), smooth(monthlyBestWorstScoresDistribution.best_easiness(monthlyBestWorstScoresDistribution.gender == 'M', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), (monthlyBestWorstScoresDistribution.best_easiness(monthlyBestWorstScoresDistribution.gender == 'M', :)));

set(maleplothandle,'DisplayName','Male');
hold on;

femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), smooth(monthlyBestWorstScoresDistribution.best_easiness(monthlyBestWorstScoresDistribution.gender == 'F', :), 3));
% Uncomment next line and comment previous line for unsmoothed line
% femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), (monthlyBestWorstScoresDistribution.best_easiness(monthlyBestWorstScoresDistribution.gender == 'F', :)));

set(femaleplothandle,'DisplayName','Female');

% Create xlabel
xlabel('Month');

% Create ylabel
ylabel('Professor density');

% Create title
title('Best months for Easiness');

box(axeshandle,'on');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});

% Set Y limits
ylim(axeshandle,[0 0.5]);

% Create legend
legend(axeshandle,'show');

%% Plot monthwise worst easiness distribution

% Create figure
figurehandle = figure;

% Create axes
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

% Create multiple lines using two plot functions
maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), smooth(monthlyBestWorstScoresDistribution.worst_easiness(monthlyBestWorstScoresDistribution.gender == 'M', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), (monthlyBestWorstScoresDistribution.worst_easiness(monthlyBestWorstScoresDistribution.gender == 'M', :)));

set(maleplothandle,'DisplayName','Male');
hold on;

femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), smooth(monthlyBestWorstScoresDistribution.worst_easiness(monthlyBestWorstScoresDistribution.gender == 'F', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), (monthlyBestWorstScoresDistribution.worst_easiness(monthlyBestWorstScoresDistribution.gender == 'F', :)));

set(femaleplothandle,'DisplayName','Female');

% Create xlabel
xlabel('Month');

% Create ylabel
ylabel('Professor density');

% Create title
title('Worst months for Easiness');

box(axeshandle,'on');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});

% Set Y limits
ylim(axeshandle,[0 0.5]);

% Create legend
legend(axeshandle,'show');

%% Plot monthwise best helpfulness distribution

% Create figure
figurehandle = figure;

% Create axes
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

% Create multiple lines using two plot functions
maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), smooth(monthlyBestWorstScoresDistribution.best_helpfulness(monthlyBestWorstScoresDistribution.gender == 'M', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), (monthlyBestWorstScoresDistribution.best_helpfulness(monthlyBestWorstScoresDistribution.gender == 'M', :)));

set(maleplothandle,'DisplayName','Male');
hold on;

femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), smooth(monthlyBestWorstScoresDistribution.best_helpfulness(monthlyBestWorstScoresDistribution.gender == 'F', :), 3));
% Uncomment next line and comment previous line for unsmoothed line
% femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), (monthlyBestWorstScoresDistribution.best_helpfulness(monthlyBestWorstScoresDistribution.gender == 'F', :)));

set(femaleplothandle,'DisplayName','Female');

% Create xlabel
xlabel('Month');

% Create ylabel
ylabel('Professor density');

% Create title
title('Best months for Helpfulness');

box(axeshandle,'on');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});

% Set Y limits
ylim(axeshandle,[0 0.5]);

% Create legend
legend(axeshandle,'show');

%% Plot monthwise worst helpfulness distribution

% Create figure
figurehandle = figure;

% Create axes
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

% Create multiple lines using two plot functions
maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), smooth(monthlyBestWorstScoresDistribution.worst_helpfulness(monthlyBestWorstScoresDistribution.gender == 'M', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), (monthlyBestWorstScoresDistribution.worst_helpfulness(monthlyBestWorstScoresDistribution.gender == 'M', :)));

set(maleplothandle,'DisplayName','Male');
hold on;

femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), smooth(monthlyBestWorstScoresDistribution.worst_helpfulness(monthlyBestWorstScoresDistribution.gender == 'F', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), (monthlyBestWorstScoresDistribution.worst_helpfulness(monthlyBestWorstScoresDistribution.gender == 'F', :)));

set(femaleplothandle,'DisplayName','Female');

% Create xlabel
xlabel('Month');

% Create ylabel
ylabel('Professor density');

% Create title
title('Worst months for Helpfulness');

box(axeshandle,'on');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});

% Set Y limits
ylim(axeshandle,[0 0.5]);

% Create legend
legend(axeshandle,'show');

%% Plot monthwise best interest level distribution

% Create figure
figurehandle = figure;

% Create axes
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

% Create multiple lines using two plot functions
maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), smooth(monthlyBestWorstScoresDistribution.best_interest(monthlyBestWorstScoresDistribution.gender == 'M', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), (monthlyBestWorstScoresDistribution.best_interest(monthlyBestWorstScoresDistribution.gender == 'M', :)));

set(maleplothandle,'DisplayName','Male');
hold on;

femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), smooth(monthlyBestWorstScoresDistribution.best_interest(monthlyBestWorstScoresDistribution.gender == 'F', :), 3));
% Uncomment next line and comment previous line for unsmoothed line
% femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), (monthlyBestWorstScoresDistribution.best_interest(monthlyBestWorstScoresDistribution.gender == 'F', :)));

set(femaleplothandle,'DisplayName','Female');

% Create xlabel
xlabel('Month');

% Create ylabel
ylabel('Professor density');

% Create title
title('Best months for Interest level');

box(axeshandle,'on');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});

% Set Y limits
ylim(axeshandle,[0 0.5]);

% Create legend
legend(axeshandle,'show');

%% Plot monthwise worst interest level distribution

% Create figure
figurehandle = figure;

% Create axes
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

% Create multiple lines using two plot functions
maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), smooth(monthlyBestWorstScoresDistribution.worst_interest(monthlyBestWorstScoresDistribution.gender == 'M', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% maleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'M', :), (monthlyBestWorstScoresDistribution.worst_interest(monthlyBestWorstScoresDistribution.gender == 'M', :)));

set(maleplothandle,'DisplayName','Male');
hold on;

femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), smooth(monthlyBestWorstScoresDistribution.worst_interest(monthlyBestWorstScoresDistribution.gender == 'F', :), 3));

% Uncomment next line and comment previous line for unsmoothed line
% femaleplothandle = plot(monthlyBestWorstScoresDistribution.month(monthlyBestWorstScoresDistribution.gender == 'F', :), (monthlyBestWorstScoresDistribution.worst_interest(monthlyBestWorstScoresDistribution.gender == 'F', :)));

set(femaleplothandle,'DisplayName','Female');

% Create xlabel
xlabel('Month');

% Create ylabel
ylabel('Professor density');

% Create title
title('Worst months for Interest levels');

box(axeshandle,'on');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});

% Set Y limits
ylim(axeshandle,[0 0.5]);

% Create legend
legend(axeshandle,'show');

%% Clear variables

clearvars;

%% Load dataset with all comment scores by months dataset

allCommentScores = dataset('File', '../fixtures/all_csv/all_comments_month_avg_scores_gender.csv', 'ReadVarNames', true, 'ReadObsNames', false, 'Delimiter', ',');
allCommentScores.gender = nominal(allCommentScores.gender);

%% Scatter plot months vs clarity scores by gender

figurehandle = figure;
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

allMaleCommentScoresSample = datasample(allCommentScores(allCommentScores.gender == 'M', :), 1200, 'Replace', false);
scatterhandle1 = scatter(allMaleCommentScoresSample.month, allMaleCommentScoresSample.avg_clarity, 'b', 'x');
set(scatterhandle1,'DisplayName','Male');
hold on;
allFemaleCommentScoresSample = datasample(allCommentScores(allCommentScores.gender == 'F', :), 1200, 'Replace', false);
scatterhandle2 = scatter(allFemaleCommentScoresSample.month, allFemaleCommentScoresSample.avg_clarity, 'r', 'o');
set(scatterhandle2,'DisplayName','Female');

% Create ylabel
ylabel('Average clarity');

% Create title
title('Average clarity scores by month');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});
% Create legend
legendhandle = legend(axeshandle,'show');
set(legendhandle,...
    'Position',[0.844025157875342 0.1711129460279 0.0544474386301323 0.0447204957837644]);

%% Scatter plot months vs easiness scores by gender

figurehandle = figure;
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

allMaleCommentScoresSample = datasample(allCommentScores(allCommentScores.gender == 'M', :), 1200, 'Replace', false);
scatterhandle1 = scatter(allMaleCommentScoresSample.month, allMaleCommentScoresSample.avg_clarity, 'b', 'x');
set(scatterhandle1,'DisplayName','Male');
hold on;
allFemaleCommentScoresSample = datasample(allCommentScores(allCommentScores.gender == 'F', :), 1200, 'Replace', false);
scatterhandle2 = scatter(allFemaleCommentScoresSample.month, allFemaleCommentScoresSample.avg_clarity, 'r', 'o');
set(scatterhandle2,'DisplayName','Female');

% Create ylabel
ylabel('Average easiness');

% Create title
title('Average easiness scores by month');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});
% Create legend
legendhandle = legend(axeshandle,'show');
set(legendhandle,...
    'Position',[0.844025157875342 0.1711129460279 0.0544474386301323 0.0447204957837644]);

%% Scatter plot months vs helpfulness scores by gender

figurehandle = figure;
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

allMaleCommentScoresSample = datasample(allCommentScores(allCommentScores.gender == 'M', :), 1200, 'Replace', false);
scatterhandle1 = scatter(allMaleCommentScoresSample.month, allMaleCommentScoresSample.avg_clarity, 'b', 'x');
set(scatterhandle1,'DisplayName','Male');
hold on;
allFemaleCommentScoresSample = datasample(allCommentScores(allCommentScores.gender == 'F', :), 1200, 'Replace', false);
scatterhandle2 = scatter(allFemaleCommentScoresSample.month, allFemaleCommentScoresSample.avg_clarity, 'r', 'o');
set(scatterhandle2,'DisplayName','Female');

% Create ylabel
ylabel('Average helpfulness');

% Create title
title('Average helpfulness scores by month');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});
% Create legend
legendhandle = legend(axeshandle,'show');
set(legendhandle,...
    'Position',[0.844025157875342 0.1711129460279 0.0544474386301323 0.0447204957837644]);

%% Scatter plot months vs interest levels by gender

figurehandle = figure;
axeshandle = axes('Parent',figurehandle);
hold(axeshandle,'on');

allMaleCommentScoresSample = datasample(allCommentScores(allCommentScores.gender == 'M', :), 1200, 'Replace', false);
scatterhandle1 = scatter(allMaleCommentScoresSample.month, allMaleCommentScoresSample.avg_clarity, 'b', 'x');
set(scatterhandle1,'DisplayName','Male');
hold on;
allFemaleCommentScoresSample = datasample(allCommentScores(allCommentScores.gender == 'F', :), 1200, 'Replace', false);
scatterhandle2 = scatter(allFemaleCommentScoresSample.month, allFemaleCommentScoresSample.avg_clarity, 'r', 'o');
set(scatterhandle2,'DisplayName','Female');

% Create ylabel
ylabel('Average interest');

% Create title
title('Average interest levels by month');

% Set the remaining axes properties
set(axeshandle,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12],'XTickLabel',...
    {'','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});
% Create legend
legendhandle = legend(axeshandle,'show');
set(legendhandle,...
    'Position',[0.844025157875342 0.1711129460279 0.0544474386301323 0.0447204957837644]);

%% Clear variables

clearvars;


