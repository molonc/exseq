%% This code handles the hybridization process

%% Set angle: defining possible range of angles for the servomotor

for angle = 0.25:0.1:0.75 % starting from 0.25 to 0.75 at a step size of 0.1
writePosition(m, angle); % reading angle
current_pos = readPosition(m);
current_pos = current_pos*180; % converting angle to radians
fprintf('Current motor position is %d degrees\n', current_pos);
pause(2);
end

%% valve and pump

outputSingleScan(s,valveP2); % creating session for hybridization solution
pause(10);

% setting up timer and beginning filling the chamber for 3 minutes
on_off = 1;
speed = 3;
t = timer('TimerFcn','on_off=3; disp("Hybridization Set " + string(datetime("now")))','StartDelay',(177)); % 177 is approx 3 mins
% timing is still a work in progress

disp("Primer Hybridization Prime " + string(datetime("now")))
outputSingleScan(s,[0 0 0 0 on_off speed]);
start(t);

while on_off == 1

end

outputSingleScan(s,[0 0 0 0 on_off speed]);
delete(t);

pause(45)

pause(2700) %2700 refers to 45 mins of incubation/shaking