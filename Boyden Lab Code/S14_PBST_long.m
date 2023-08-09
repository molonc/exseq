%% This is the code for carrying out a PBST long wash.
% We start by setting the angle and then proceeding to setting the valve
% and pump.

%% Set angle

for angle = 0.75 % only one servo angle needed for the PBST long wash
writePosition(m, angle);
current_pos = readPosition(m);
current_pos = current_pos*180; % convert angle to degrees
fprintf('Current motor position is %d degrees\n', current_pos);
pause(2); % pause for 10 s to ensure calibration
end

%% valve and pump

outputSingleScan(s,valveP7); % starting session for the PBST valve
pause(10);

on_off = 1;
speed = 2;
t = timer('TimerFcn','on_off=3; disp("Wash Done " + string(datetime("now")))','StartDelay',(5400)); % wash goes on for 1 hr and 30 mins
disp("PBST Long Wash Start " + string(datetime("now")))
outputSingleScan(s,[0 0 0 0 on_off speed]);
start(t); % starting the timer for 90 mins

% shaking back and forth during wash
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
delete(t); % turning it off

pause(45)