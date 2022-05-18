clear;

filename = "..\..\meassure_data\razor_9dof\meanListAccel.csv";

if isfile(filename)
    M_accel = readmatrix(filename);
end

filename = "..\..\meassure_data\razor_9dof\meanListMag.csv";
if isfile(filename)
    M_mag = readmatrix(filename);
end

filename = "..\..\meassure_data\razor_9dof\meanListGyro.csv";
if isfile(filename)
    M_gyro = readmatrix(filename);
end

disp("M_accel");
disp("=================================================");
ros_razor_callibrateFn(M_accel);
disp("M_mag");
disp("=================================================");
ros_razor_callibrateFn(M_mag);
disp("M_gyro");
disp("=================================================");
ros_razor_callibrateFn(M_gyro);