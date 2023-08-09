%% This is the code for setting up the priming of the imaging buffer.
% We initially set the possible angles and then continue to set the valve and pump

%% Do this step while the plate is still on the tilting platform

%% Set angle

for angle = 0.25:0.1:0.75 % going through a range of angles
writePosition(m, angle); % writing angle to servo
current_pos = readPosition(m);
current_pos = current_pos*180; % converting angle to degrees
fprintf('Current motor position is %d degrees\n', current_pos);
pause(2);
end

%% pick valve, set speed, and turn on

outputSingleScan(s,valveP6); % creating session for imaging buffer valve
pause(10); % pause for 10 s to ensure calibration

on_off = 1;
speed = 3; % setting the speed

t = timer('TimerFcn','on_off=3; disp("Imaging Buffer Priming Done " + string(datetime("now")))','StartDelay',(240)); 
% carry out imaging buffer priming for 40 seconds
disp("Imaging Buffer Priming Start " + string(datetime("now")))
outputSingleScan(s,[0 0 0 0 on_off speed]);
start(t) % starting timer for imaging buffer priming which lasts for about 40 mins

while on_off == 1

end

outputSingleScan(s,[0 0 0 0 on_off speed])
delete(t); % turning it off
