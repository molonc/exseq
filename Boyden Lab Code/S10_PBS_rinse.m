%% The code is for setting up and controlling the PBS rinsing process.
% We initially set the possible angles and then continue to set the valve
% and pump.

%% Set angle

for angle = 0.75:-0.1:0.25 % range of possible servo angles: starting from 0.75 and then decrementing until 0.25
writePosition(m, angle); % writing angle to servo
current_pos = readPosition(m);
current_pos = current_pos*180; % converting angle to degrees
fprintf('Current motor position is %d degrees\n', current_pos);
pause(2);
end

%% Set valve and pump

outputSingleScan(s,valveP1); % creating session for PBS valve valve
pause(10); % pause for 10 s to ensure calibration

on_off = 1;
speed = 3;
t = timer('TimerFcn','on_off=3; disp("Rinse Done " + string(datetime("now")))','StartDelay',(435));
disp("PBS Rinse Start " + string(datetime("now")))

outputSingleScan(s,[0 0 0 0 on_off speed]);
start(t); % setting up and starting the timer for 435 seconds

while on_off == 1

end

outputSingleScan(s,[0 0 0 0 on_off speed]);
delete(t); % turning it off 

pause(45)
