%% Import data from text file.
% Script for importing data from the following text file:
%
%    /home/datalab01/Desktop/Souradeep_Docs/Thesis/project-gender-inequality/fixtures/all_csv/sentiment_v_overall_mini.csv
%
% To extend the code to different selected data or a different text file,
% generate a function instead of a script.

% Auto-generated by MATLAB on 2016/03/17 10:39:08

%% Initialize variables.
filename = '/home/datalab01/Desktop/Souradeep_Docs/Thesis/project-gender-inequality/fixtures/all_csv/sentiment_v_overall_mini.csv';
delimiter = ',';
startRow = 2;

%% Read columns of data as strings:
% For more information, see the TEXTSCAN documentation.
formatSpec = '%q%q%q%q%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to format string.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'HeaderLines' ,startRow-1, 'ReturnOnError', false);

%% Close the text file.
fclose(fileID);

%% Convert the contents of columns containing numeric strings to numbers.
% Replace non-numeric strings with NaN.
raw = repmat({''},length(dataArray{1}),length(dataArray)-1);
for col=1:length(dataArray)-1
    raw(1:length(dataArray{col}),col) = dataArray{col};
end
numericData = NaN(size(dataArray{1},1),size(dataArray,2));

for col=[2,3,4]
    % Converts strings in the input cell array to numbers. Replaced non-numeric
    % strings with NaN.
    rawData = dataArray{col};
    for row=1:size(rawData, 1);
        % Create a regular expression to detect and remove non-numeric prefixes and
        % suffixes.
        regexstr = '(?<prefix>.*?)(?<numbers>([-]*(\d+[\,]*)+[\.]{0,1}\d*[eEdD]{0,1}[-+]*\d*[i]{0,1})|([-]*(\d+[\,]*)*[\.]{1,1}\d+[eEdD]{0,1}[-+]*\d*[i]{0,1}))(?<suffix>.*)';
        try
            result = regexp(rawData{row}, regexstr, 'names');
            numbers = result.numbers;
            
            % Detected commas in non-thousand locations.
            invalidThousandsSeparator = false;
            if any(numbers==',');
                thousandsRegExp = '^\d+?(\,\d{3})*\.{0,1}\d*$';
                if isempty(regexp(thousandsRegExp, ',', 'once'));
                    numbers = NaN;
                    invalidThousandsSeparator = true;
                end
            end
            % Convert numeric strings to numbers.
            if ~invalidThousandsSeparator;
                numbers = textscan(strrep(numbers, ',', ''), '%f');
                numericData(row, col) = numbers{1};
                raw{row, col} = numbers{1};
            end
        catch me
        end
    end
end


%% Split data into numeric and cell columns.
rawNumericColumns = raw(:, [2,3,4]);
rawCellColumns = raw(:, 1);


%% Exclude rows with non-numeric cells
I = ~all(cellfun(@(x) (isnumeric(x) || islogical(x)) && ~isnan(x),rawNumericColumns),2); % Find rows with non-numeric cells
rawNumericColumns(I,:) = [];
rawCellColumns(I,:) = [];

%% Create output variable
tabSentiment = table;
tabSentiment.gender = rawCellColumns(:, 1);
tabSentiment.overall = cell2mat(rawNumericColumns(:, 1));
tabSentiment.positive = cell2mat(rawNumericColumns(:, 2));
tabSentiment.negative = cell2mat(rawNumericColumns(:, 3));

%% Clear temporary variables
clearvars filename delimiter startRow formatSpec fileID dataArray ans raw col numericData rawData row regexstr result numbers invalidThousandsSeparator thousandsRegExp me rawNumericColumns rawCellColumns I J K;

%% Load dataset
dsSentiment = table2dataset(tabSentiment);
dsSentiment.gender = nominal(dsSentiment.gender);
%% Create plot

maleSentiTemp = dsSentiment(dsSentiment.gender == 'M', :);
femaleSentiTemp = dsSentiment(dsSentiment.gender == 'F', :);

maleSenti = sortrows(maleSentiTemp, 'overall');
femaleSenti = sortrows(femaleSentiTemp, 'overall');

clear maleSentiTemp femaleSentiTemp

%% Plot positive sentiment graph
figureh = figure;
axesh = axes('Parent', figureh);
hold(axesh, 'on');
plot(maleSenti.overall, smooth(maleSenti.positive));
hold on;
plot(femaleSenti.overall, smooth(femaleSenti.positive));

clear figureh axesh
%% %% Plot negative sentiment graph
figureh = figure;
axesh = axes('Parent', figureh);
hold(axesh, 'on');
plot(maleSenti.overall, smooth(maleSenti.negative, 101));
hold on;
plot(femaleSenti.overall, smooth(femaleSenti.negative, 101));

clear figureh axesh
%%

scatter(maleSenti.overall, smooth(maleSenti.negative));
hold on;
scatter(femaleSenti.overall, femaleSenti.negative);