clc
clear
close all

%load aaa.txt
coords = load("path_data.txt");
figure
xlabel("Longitude")
ylabel("Latitude")
plot(coords(:,1),coords(:,2))
