%% This code is for setting up a short PBST run (washing).
% We initially set the possible angles and then continue to set the valve
% and pump.

%% Set angle
while angle < 0.75
    for angle = angle:0.05:0.75 % angle ranges from 0 to 0.75 while incrementing at 0.05
    writePosition(m, angle); % setting angle of servomotor
    pause(2);
    end
end

%% Set valve and pump

outputSingleScan(s,valveP7); % creating session for PBST valve
pause(10); % pause for 10 s to ensure calibration

on_off = 1;
speed = 3;
t = timer('TimerFcn','on_off=3; disp("Wash Done " + string(datetime("now")))','StartDelay',(600));
disp("Wash Start " + string(datetime("now"))) %setting timer to 10 mins for washing

outputSingleScan(s,[0 0 0 0 on_off speed]); 
start(t); % setting the speed and turning the cycle on

% shaking back and forth throughout washing process
while on_off == 1

    for angle = 0.6:-0.05:0.35
    writePosition(m, angle);
    pause(2);
    end
    
    pause(5);
    
    for angle = 0.35:0.05:0.6
        writePosition(m, angle);
        pause(2);
    end
    pause(5);
end
outputSingleScan(s,[0 0 0 0 on_off speed]); % turning it off
delete(t)

pause(45)