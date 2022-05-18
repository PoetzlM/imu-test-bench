clear;

filename = "..\..\meassure_data\meanListAccel.csv";
if isfile(filename)
    M_accel = readmatrix(filename);
end

filename = "..\..\meassure_data\meanListMag.csv";
if isfile(filename)
    M_mag = readmatrix(filename);
end

filename = "..\..\meassure_data\meanListGyro.csv";
if isfile(filename)
    M_gyro = readmatrix(filename);
end

calcPrintComp(M_accel, "M_accel");
calcPrintComp(M_mag, "M_mag");
calcPrintComp(M_gyro, "M_gyro");

function calcPrintComp(M_cal, name)

    [A, b, expMFS] = magcal(M_cal, "auto");

    %calc corrected values
    xCorrected = (M_cal-b)*A;
    
    %f_hdl = figure;
    %figure(f_hdl);
    figure('name', name);
    

    scatter3(M_cal(:,1), M_cal(:,2), M_cal(:,3));
    hold on;
    scatter3(xCorrected(:,1), xCorrected(:,2), xCorrected(:,3));
    hold on;

    disp(name);
    disp("=================================================");
    disp(A);
    disp(b);

end


