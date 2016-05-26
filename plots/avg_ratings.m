%% Load appropriate variables into dataset

ds_temp = dataset('File', '../fixtures/all_csv/Avg_ratings_distribution.csv', 'ReadVarNames', true, 'ReadObsNames', false, 'Delimiter', ',');
ds = ds_temp(:, {'gender', 'clarity', 'easiness', 'helpfulness', 'overall_quality'});
ds.gender = nominal(ds.gender);
clear ds_temp

%% Plot clarity scores histogram

male_clar = ds.clarity(ds.gender == 'M', :);
female_clar = ds.clarity(ds.gender == 'F');

figure;
h1 = histogram(male_clar);
h1.Normalization = 'probability';
h1.BinWidth = 0.5;
hold on
h2 = histogram(female_clar);
h2.Normalization = 'probability';
h2.BinWidth = 0.5;

group = [repmat({'M'}, 5, 1); repmat({'F'}, 10, 1)];
boxplot([male_clar;female_clar], group);


clear male_clar female_clar h1 h2 group

%% Plot easiness scores histogram

male_ease = ds.easiness(ds.gender == 'M', :);
female_ease = ds.easiness(ds.gender == 'F');

figure;
h1 = histogram(male_ease);
h1.Normalization = 'probability';
h1.BinWidth = 0.5;
hold on
h2 = histogram(female_ease);
h2.Normalization = 'probability';
h2.BinWidth = 0.5;

clear male_ease female_ease h1 h2 

%% Plot helpfulness scores histogram

male_help = ds.helpfulness(ds.gender == 'M', :);
female_help = ds.helpfulness(ds.gender == 'F');

figure;
h1 = histogram(male_help);
h1.Normalization = 'probability';
h1.BinWidth = 0.5;
hold on
h2 = histogram(female_help);
h2.Normalization = 'probability';
h2.BinWidth = 0.5;

clear male_help female_help h1 h2 

%% Plot overall quality scores histogram

male_ovr = ds.overall_quality(ds.gender == 'M', :);
female_ovr = ds.overall_quality(ds.gender == 'F');

figure;
h1 = histogram(male_ovr);
h1.Normalization = 'probability';
h1.BinWidth = 0.5;
hold on
h2 = histogram(female_ovr);
h2.Normalization = 'probability';
h2.BinWidth = 0.5;

clear male_help female_help h1 h2 