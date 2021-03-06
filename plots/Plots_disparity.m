Discipline_division;

%% Plot discipline size vs disparity in 'Overall Quality' scores
axes1 = axes('Parent', figure);
hold on;                                      
scatter(dsDiscipline.TotalDisciplineSize, dsDiscipline.OvrDisparity);
text(dsDiscipline.TotalDisciplineSize + 0.001, dsDiscipline.OvrDisparity + 0.001, dsDiscipline.Disciplines, 'FontSize', 17);

% Set the remaining axes properties
set(axes1,'XAxisLocation','origin','XScale','log','YAxisLocation','origin');
xlabel('Discipline Size');
ylabel('Disparity');
title('Disparity_{OverallQuality} vs Discipline sizes');

%% Plot discipline size vs disparity in 'Clarity' scores
axes1 = axes('Parent', figure);
hold on;                                     
scatter(dsDiscipline.TotalDisciplineSize, dsDiscipline.ClarDisparity);
text(dsDiscipline.TotalDisciplineSize + 0.001, dsDiscipline.ClarDisparity + 0.001, dsDiscipline.Disciplines, 'FontSize', 17);

% Set the remaining axes properties
set(axes1,'XAxisLocation','origin','XScale','log','YAxisLocation','origin');
xlabel('Discipline Size');
ylabel('Disparity');
title('Disparity_{Clarity} vs Discipline sizes');
clear axes1

%% Plot discipline size vs disparity in 'Easiness' scores
axes1 = axes('Parent', figure);
hold on;                                      
scatter(dsDiscipline.TotalDisciplineSize, dsDiscipline.EaseDisparity);
text(dsDiscipline.TotalDisciplineSize + 0.001, dsDiscipline.EaseDisparity + 0.001, dsDiscipline.Disciplines);

% Set the remaining axes properties
set(axes1,'XAxisLocation','origin','XScale','log','YAxisLocation','origin');
xlabel('Discipline Size');
ylabel('Disparity');
title('Disparity_{Easiness} vs Discipline sizes')
clear axes1

%% Plot discipline size vs disparity in 'Helpfulness' scores
axes1 = axes('Parent', figure);
hold on;                                      
scatter(dsDiscipline.TotalDisciplineSize, dsDiscipline.HelpDisparity);
text(dsDiscipline.TotalDisciplineSize + 0.001, dsDiscipline.HelpDisparity + 0.001, dsDiscipline.Disciplines);

% Set the remaining axes properties
set(axes1,'XAxisLocation','origin','XScale','log','YAxisLocation','origin');
xlabel('Discipline Size');
ylabel('Disparity');
title('Disparity_{Helpfulness} vs Discipline sizes');
clear axes1

%% Plot gender imbalance vs disparity in 'Overall Quality' scores
axes1 = axes('Parent', figure);
hold on;                                      
scatter(dsDiscipline.Imbalance, dsDiscipline.OvrDisparity);
text(dsDiscipline.Imbalance + 0.001, dsDiscipline.OvrDisparity + 0.001, dsDiscipline.Disciplines, 'FontSize', 17);

% Set the remaining axes properties
set(axes1,'XAxisLocation','origin','XScale','log','YAxisLocation','origin');
xlabel('Imbalance');
ylabel('Disparity');
title('Disparity_{OverallQuality} vs Imbalances');
clear axes1

%% Plot imbalance vs disparity in 'Clarity' scores
axes1 = axes('Parent', figure);
hold on;                                      
scatter(dsDiscipline.Imbalance, dsDiscipline.ClarDisparity);
text(dsDiscipline.Imbalance + 0.001, dsDiscipline.ClarDisparity + 0.001, dsDiscipline.Disciplines);

% Set the remaining axes properties
set(axes1,'XAxisLocation','origin','XScale','log','YAxisLocation','origin');
xlabel('Imbalance');
ylabel('Disparity');
title('Disparity_{Clarity} vs Imbalances')
clear axes1

%% Plot imbalance vs disparity in 'Easiness' scores
axes1 = axes('Parent', figure);
hold on;                                      
scatter(dsDiscipline.Imbalance, dsDiscipline.EaseDisparity);
text(dsDiscipline.Imbalance + 0.001, dsDiscipline.EaseDisparity + 0.001, dsDiscipline.Disciplines);

% Set the remaining axes properties
set(axes1,'XAxisLocation','origin','XScale','log','YAxisLocation','origin');
xlabel('Imbalance');
ylabel('Disparity');
title('Disparity_{Easiness} vs Imbalances')
clear axes1

%% Plot imbalance vs disparity in 'Helpfulness' scores
axes1 = axes('Parent', figure);
hold on;                                      
scatter(dsDiscipline.Imbalance, dsDiscipline.HelpDisparity);
text(dsDiscipline.Imbalance + 0.001, dsDiscipline.HelpDisparity + 0.001, dsDiscipline.Disciplines);

% Set the remaining axes properties
set(axes1,'XAxisLocation','origin','XScale','log','YAxisLocation','origin');
xlabel('Imbalance');
ylabel('Disparity');
title('Disparity_{Helpfulness} vs Imbalances')
clear axes1

