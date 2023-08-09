%% This code controls cleaning lines for hybridization and ligation solutions. 
% We initially set the possible angles and then continue to set the valve and pump
% separately: first for the hybridization and then the ligation solutions.

%% Set angle: prints current angle in degrees

for angle = 0.5:0.25:0.75 % angles of servo: 0.5 then 0.75
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

t = timer('TimerFcn','on_off=3; disp("Hybridization line clean Done " + string(datetime("now")))','StartDelay',(167)); %167 seconds for cleaning
disp("Hybridization line clean Start " + string(datetime("now")))
start(t) % setting up and starting the timer for 167 seconds

outputSingleScan(s,[0 0 0 0 on_off speed]); % setting the speed and turning the cycle on
while on_off == 1

end
outputSingleScan(s,[0 0 0 0 on_off speed]) % turning it off 
delete(t)

pause (45) % waiting for 45 s before repeating the same process for the ligation solution; 
          

outputSingleScan(s,valveP4);
pause(10);

on_off = 1;
speed = 3;

t = timer('TimerFcn','on_off=3; disp("Ligation line clean Done " + string(datetime("now")))','StartDelay',(167));
disp("Ligation line clean Start " + string(datetime("now")))
start(t)

outputSingleScan(s,[0 0 0 0 on_off speed]);
while on_off == 1

end
outputSingleScan(s,[0 0 0 0 on_off speed])
delete(t)

pause (45)