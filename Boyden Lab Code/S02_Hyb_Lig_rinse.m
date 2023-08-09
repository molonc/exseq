%% This code controls rinsing lines for the hybridization and ligation solutions.
% We initially set the possible angles and then continue to set the valve and pump
% separately: first for the hybridization and then the ligation solutions.

%% Set angle

for angle = 0.75 % only one angle for rinsing
writePosition(m, angle); % setting the servo to that angle
current_pos = readPosition(m);
current_pos = current_pos*180; % converts angle to degrees
fprintf('Current motor position is %d degrees\n', current_pos);
pause(2);
end

%% Set valve and pump

outputSingleScan(s,valveP2); % creating session for hybridization solution valve
pause(10); % pause for 10 s to ensure calibration

on_off = 1;
speed = 3;

t = timer('TimerFcn','on_off=3; disp("Hybridization line rinse Done " + string(datetime("now")))','StartDelay',(167));
disp("Hybridization line rinse Start " + string(datetime("now")))
start(t) % setting up and starting timer for 167 s

outputSingleScan(s,[0 0 0 0 on_off speed]); % setting the speed and turning the cycle on
while on_off == 1

end
outputSingleScan(s,[0 0 0 0 on_off speed]) % turning it off 
delete(t)

pause (45) % waiting for 45s before switching to rinsing ligation solution

outputSingleScan(s,valveP4); % repeat the whole rinsing process
pause(10);

on_off = 1;
speed = 3;

t = timer('TimerFcn','on_off=3; disp("Ligation line rinse Done " + string(datetime("now")))','StartDelay',(167));
disp("Ligation line rinse Start " + string(datetime("now")))
start(t)


outputSingleScan(s,[0 0 0 0 on_off speed]);
while on_off == 1

end
outputSingleScan(s,[0 0 0 0 on_off speed])
delete(t)

pause (45)