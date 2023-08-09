%% This code controls clearing the air valve. 
% We initially set the possible angles and then continue to set the valve
% and pump.

%% Set angle

for angle = 0.25 % angle of servo: only 0.25
writePosition(m, angle); % setting servo to that angle
current_pos = readPosition(m);
current_pos = current_pos*180; % converting angle to degrees
fprintf('Current motor position is %d degrees\n', current_pos);
pause(2);
end

%% Set valve and pump

outputSingleScan(s,valveP5); % creating session for air valve
pause(10); % pause for 10 s to ensure calibration

on_off = 1;
speed = 2;
t = timer('TimerFcn','on_off=3; disp("Chamber clear " + string(datetime("now")))','StartDelay',(190));
disp("Air Clear Start " + string(datetime("now")))

outputSingleScan(s,[0 0 0 0 on_off speed]);
start(t); % setting up and starting the timer for 190 seconds

while on_off == 1

end

outputSingleScan(s,[0 0 0 0 on_off speed]); % turning it off 
delete(t);

pause(45)