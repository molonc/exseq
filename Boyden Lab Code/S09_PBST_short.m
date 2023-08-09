%% This code controls a short PBST wash. 
% We initially set the possible angles and then continue to set the valve
% and pump.
%% Set angle

while angle < 0.75
    for angle = angle:0.05:0.75 % angle starts from 0 and then increments by 0.05 until it reaches 0.75
    writePosition(m, angle); % writing angle to servo
    pause(2);
    end
end

%% Set valve and pump

outputSingleScan(s,valveP7); % starting session for PBST valve
pause(10); % pause for 10 s to ensure calibration

on_off = 1;
speed = 3;
t = timer('TimerFcn','on_off=3; disp("Wash Done " + string(datetime("now")))','StartDelay',(735)); 
disp("Wash Start " + string(datetime("now")))

outputSingleScan(s,[0 0 0 0 on_off speed]);
start(t); % setting up and starting the timer for 735 seconds

% changes angles throughout session to ensure complete wash
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

outputSingleScan(s,[0 0 0 0 on_off speed]);
delete(t)  % turning it off 

pause(45)