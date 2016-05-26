%% Import data from text file.
% Script for importing data from the following text file:
%
%    /home/datalab01/Desktop/Souradeep_Docs/Thesis/project-gender-inequality/fixtures/all_csv/Displine_disparity_helpfulness2.csv
%
% To extend the code to different selected data or a different text file,
% generate a function instead of a script.

% Auto-generated by MATLAB on 2016/02/08 16:31:59

%% Initialize variables.
filename = '/home/datalab01/Desktop/Souradeep_Docs/Thesis/project-gender-inequality/fixtures/all_csv/Displine_disparity_helpfulness2.csv';
delimiter = ',';
startRow = 2;

%% Format string for each line of text:
%   column1: text (%s)
%	column2: double (%f)
%   column3: double (%f)
% For more information, see the TEXTSCAN documentation.
formatSpec = '%s%f%f%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to format string.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'HeaderLines' ,startRow-1, 'ReturnOnError', false);

%% Close the text file.
fclose(fileID);

%% Post processing for unimportable data.
% No unimportable data rules were applied during the import, so no post
% processing code is included. To generate code which works for
% unimportable data, select unimportable cells in a file and regenerate the
% script.

%% Allocate imported array to column variable names
help_discipline = dataArray{:, 1};
help_size = dataArray{:, 2};
help_disparity = dataArray{:, 3};


%% Clear temporary variables
clearvars filename delimiter startRow formatSpec fileID dataArray ans;

%% Generate stem plot

% Create axes
axes1 = axes('Parent', figure);
%hold(axes1,'on');
hold on;

% Create xlabel
xlabel('Discipline Size');

% Create ylabel
ylabel('Disparity.Helpfulness');

% Uncomment the following line to preserve the X-limits of the axes
xlim(axes1,[0 150000]);
% Uncomment the following line to preserve the Y-limits of the axes
ylim(axes1,[0 0.01]);

box(axes1,'on');

% Set the remaining axes properties
set(axes1,'XScale','log','YScale','log');

stem(help_size, help_disparity)

