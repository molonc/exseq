%% This code controls the ligation buffer.
% We initially set the possible angles and then continue to set the valve
% and pump.

%% Set angle

for angle = 0.25:0.1:0.75 % three angles for the servo: 0.25, 0.5, 0.75
writePosition(m, angle); % writing angle to servo
current_pos = readPosition(m); 
current_pos = current_pos*180;
fprintf('Current motor position is %d degrees\n', current_pos);
pause(2);
end

%% valve and pump

outputSingleScan(s,valveP3); % creating session for ligation buffer valve
pause(10);

on_off = 1;
speed = 3;
t = timer('TimerFcn','on_off=3; disp("Ligation buffer done" + string(datetime("now")))','StartDelay',(200)); %was 167, now 200

disp("Ligation buffer start " + string(datetime("now")))
outputSingleScan(s,[0 0 0 0 on_off speed]);
start(t); % starting timer for ligation buffer which lasts for about 3 mins

while on_off == 1

end

outputSingleScan(s,[0 0 0 0 on_off speed]); % turning it off 
delete(t);

pause(45)

pause(900)