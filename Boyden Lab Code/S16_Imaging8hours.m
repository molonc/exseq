%% This code handles 4 hours of imaging (the valve for the imaging buffer)

%% Valve and Pump Settings

outputSingleScan(s,valveP6); % creating session for imaging buffer valve
pause(10); % pause for 10 s to ensure calibration

on_off = 1; % x<1.5 = on; x>3 = off 
speed = 0.1; 

t = timer('TimerFcn','on_off=3; disp("Imaging Done " + string(datetime("now")))','StartDelay',(14400)); % 4 hours
disp("Imaging Start [[" + string(datetime("now")))

outputSingleScan(s,[0 0 0 0 on_off speed]);

while on_off == 1
    
end
outputSingleScan(s,[0 0 0 0 on_off speed]); % ending session
delete(t)


