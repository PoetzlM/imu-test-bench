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

calcPrintComp(M_accel, "M_accel", 256);
%calcPrintComp(M_mag, "M_mag", 0);
%calcPrintComp(M_gyro, "M_gyro", 0);

function calcPrintComp(M_cal, name, scale)

    [A, b, expMFS] = magcal(M_cal, "auto");

    %calc corrected values
    xCorrected = (M_cal-b)*A;
    

    if (scale ~= 0)
        norm = vecnorm(xCorrected.');
        norm_mean = mean(norm);
        scaleFac = scale / norm_mean;
        scaleMatrix = diag([scaleFac, scaleFac, scaleFac]);
        A = A * scaleMatrix;

        xCorrected = (M_cal-b)*A;
    end

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

    norm = vecnorm(xCorrected.');
    norm_mean = mean(norm);
    disp("mean norm");
    disp(norm_mean);

end


