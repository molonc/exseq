%% This code is for the air clearing process.
% We initially set the possible angles and then continue to set the valve
% and pump.

%% Set angle

for angle = 0.25
writePosition(m, angle);
current_pos = readPosition(m); % servo remains at single angle for air clearing
current_pos = current_pos*180; % converting angle to degrees
fprintf('Current motor position is %d degrees\n', current_pos);
pause(2);
end

%% Set valve and pump

outputSingleScan(s,valveP5); % creating session for the air valve
pause(10); % pause for 10 s to ensure calibration

on_off = 1;
speed = 2;
t = timer('TimerFcn','on_off=3; disp("Chamber clear " + string(datetime("now")))','StartDelay',(190)); % about 3 mins for air clearing
disp("Air Clear Start " + string(datetime("now")))


% starting air clearing with predetermined speed
outputSingleScan(s,[0 0 0 0 on_off speed]);
start(t);

while on_off == 1

end

outputSingleScan(s,[0 0 0 0 on_off speed]); % turning it off 
delete(t);

pause(45)