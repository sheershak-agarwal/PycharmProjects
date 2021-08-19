clear 
close all
clc
addpath('C:\Users\Sheershak Agarwal\Desktop\PycharmProjects\ParkAndMeasure\')

diritory="SN210002";
cd(diritory);
file_pool= dir();
disp(file_pool);

phase=[];amp=[];
for i=3:length(file_pool)
    file_name=file_pool(i).name;
    disp(file_name);
    read_in; raw_data=table2array(raw_data);
    phase(:,i-2)=raw_data(:,19);
    amp(:,i-2)=raw_data(:,18);
end

disp(phase);

%% raw mean without excluding the bad measurement
mean_amp=mean(amp');
mean_phase=mean(phase');

for i =1:512
    good_index = find(abs(amp(i,:)-mean_amp(i))<10) ; % if more than 10db, exclude the data
    good_measurement(i)= length(good_index);
    new_mean_amp (i) = mean(amp(i,good_index));
    new_mean_phase (i) = mean(phase(i,good_index));
end
    
hist(good_measurement,10)

%%%calcualtion calibrated phase and amp
cal_phase=-new_mean_phase;
element=1:512;
cal_amp=new_mean_amp-mean(new_mean_amp);

m=[element;cal_amp;cal_phase]';
disp(m);
csvwrite('final_calibration.csv',m);

[X,Y]=meshgrid(1:16,1:32);
% read_in_x_y
x=reshape(X,[1,512]);
y=reshape(Y,[1,512]);
scatter3(x,y,ones(length(x),1)',40*ones(length(x),1)',cal_phase,'*')
view(0,90)

scatter3(x,y,ones(length(x),1)',40*ones(length(x),1)',cal_amp,'*')
view(0,90)
    

find(cal_amp==min(cal_amp))
    
    
    