%% This code controls the ligation solution.
% We initially set the possible angles and then continue to set the valve
% and pump. In this case, we set up a timer twice.

%% Set angle

for angle = 0.25 %stays at one angle for ligation 
writePosition(m, angle); %setting servo to angle
current_pos = readPosition(m);
current_pos = current_pos*180; % converts angle to degrees
fprintf('Current motor position is %d degrees\n', current_pos);
pause(2); % pause for 10 s to ensure calibration
end

%% valve and pump

outputSingleScan(s,valveP4); % creating session for ligation solution valve
pause(10);

% setting up the speed and timer for about 1 minute
on_off = 1;
speed = 3;
t = timer('TimerFcn','angle=0.75; disp("angle change " + string(datetime("now")))','StartDelay',(90)); %work in progress

% starting timer with predetermined speed
disp("Ligation Solution Input Start " + string(datetime("now")))
outputSingleScan(s,[0 0 0 0 on_off speed]);
start(t);

while angle == 0.25 

end
writePosition(m, angle);
delete(t);

t = timer('TimerFcn','on_off=3; disp("Ligation Start " + string(datetime("now")))','StartDelay',(100)); %work in progress
start(t);

while on_off == 1

end

outputSingleScan(s,[0 0 0 0 on_off speed]);
delete(t);



outputSingleScan(s,[0 0 0 0 on_off speed]);
delete(t);

pause(45)

pause(10800)
