%% This code is for setting up a PBS rinse.
% We initially set the possible angles and then continue to set the valve and pump
% separately: first for the hybridization and then the ligation solutions.

%% Set angle

while angle > 0.25 % angle of servo keeps decrementing until it reaches 0.25
    for angle = angle:-0.05:0.25
    writePosition(m, angle); % setting servo to angle
    pause(2);
    end
end
%% Set valve and pump

outputSingleScan(s,valveP1); % creating session for PBS rinsing valve
pause(10); % pause for 10 s to ensure calibration

on_off = 1;
speed = 3;
t = timer('TimerFcn','on_off=3; disp("Rinse Done " + string(datetime("now")))','StartDelay',(435));
disp("PBS Rinse Start " + string(datetime("now")))

outputSingleScan(s,[0 0 0 0 on_off speed]);
start(t); % setting up and starting the timer for 435 seconds

while on_off == 1

end

outputSingleScan(s,[0 0 0 0 on_off speed]); % turning it off
delete(t);

pause(45)
