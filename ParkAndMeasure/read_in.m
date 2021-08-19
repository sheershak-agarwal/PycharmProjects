%% Import data from text file
% Script for importing data from the following text file:
%
%    filename: D:\SN210001\SN210001_04_08_21_12_49_13_AM__FSW_Data.csv
%
% Auto-generated by MATLAB on 04-Aug-2021 15:48:46

%% Set up the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 34);

% Specify range and delimiter
opts.DataLines = [2, Inf];
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["VarName1", "Frequency_1", "Amplitude_1", "Phase_1", "Frequency_2", "Amplitude_2", "Phase_2", "Frequency_3", "Amplitude_3", "Phase_3", "Frequency_4", "Amplitude_4", "Phase_4", "Frequency_5", "Amplitude_5", "Phase_5", "Frequency_6", "Amplitude_6", "Phase_6", "Frequency_7", "Amplitude_7", "Phase_7", "Frequency_8", "Amplitude_8", "Phase_8", "Frequency_9", "Amplitude_9", "Phase_9", "Frequency_10", "Amplitude_10", "Phase_10", "Frequency_11", "Amplitude_11", "Phase_11"];
opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Specify variable properties
opts = setvaropts(opts, ["Amplitude_11", "Phase_11"], "TrimNonNumeric", true);
opts = setvaropts(opts, ["Amplitude_11", "Phase_11"], "ThousandsSeparator", ",");

% Import the data
raw_data = readtable(file_name, opts);


%% Clear temporary variables
clear opts