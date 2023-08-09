%% This code is for clearing the lines for hybridization and ligation solutions.
% We initially set the possible angles and then continue to set the valve and pump
% separately: first for the hybridization and then the ligation solutions.

%% Set angle
for angle = 0.75:-0.1:0.25 % 3 possible angles: 0.75, 0.5, 0.25
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
speed = 2;

t = timer('TimerFcn','on_off=3; disp("Hybridization line clear Done " + string(datetime("now")))','StartDelay',(190));
disp("Hybridization line clear Start " + string(datetime("now"))) 
start(t); % setting up and starting the timer for 190 s

outputSingleScan(s,[0 0 0 0 on_off speed]); % starting session for clearing hybridization valve 
while on_off == 1

end
outputSingleScan(s,[0 0 0 0 on_off speed])
delete(t)

pause (45) % pause before repeating process for ligation solution


outputSingleScan(s,valveP4);
pause(10);

on_off = 1;
speed = 2;

t = timer('TimerFcn','on_off=3; disp("Ligation line clear Done " + string(datetime("now")))','StartDelay',(190));
disp("Ligation line clear Start " + string(datetime("now"))) 
start(t);

outputSingleScan(s,[0 0 0 0 on_off speed]);
while on_off == 1

end
outputSingleScan(s,[0 0 0 0 on_off speed])
delete(t)

pause (45)