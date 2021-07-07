clc
clear
close all

%load aaa.txt
data = load("coords_bd09mc.txt");
figure
plot(data(:,2),data(:,1))
xlabel("纬度方向/m")
ylabel("经度方向/m")
