%% This code handles the stripping solution.
% We initially set the possible angles and then continue to set the valve
% and pump for the stripping solution.

%% Set angle
% for angle = 0.25:0.1:0.75 
% writePosition(m, angle);
% current_pos = readPosition(m);
% current_pos = current_pos*180;
% fprintf('Current motor position is %d degrees\n', current_pos);
% pause(2);
% end

while angle < 0.75 
    for angle = angle:0.05:0.75 % Angles range from 0 to 0.75 and increment at 0.05
    writePosition(m, angle); % setting angle of servo
    pause(2);
    end
end
%% Set valve and pump
outputSingleScan(s,valveP8); % initializing session for stripping solution valve
pause(10);

disp("Stripping Initiated " + string(datetime("now")))
t = timer('TimerFcn','on_off=3; disp("Primer done " + string(datetime("now")))','StartDelay',(3600)); % timer set to an hour for stripping
start(t);  % setting up and starting the timer for 167 seconds

on_off = 1;
speed = 2;
outputSingleScan(s,[0 0 0 0 on_off speed]); % setting the speed and turning the cycle on

% while loop below changes servo angle to ensure shaking
while on_off == 1

    for angle = 0.6:-0.05:0.35 % decrementing angle from 0.6 to 0.35 by 0.05
    writePosition(m, angle);
    pause(2);
    end
    
    pause(5);
    
    for angle = 0.35:0.05:0.6 % incrementing angle from 0.35 to 0.6 by 0.05
        writePosition(m, angle);
        pause(2);
    end
    pause(5);
end
outputSingleScan(s,[0 0 0 0 on_off speed]); % turning it off 
delete(t)

pause (45)

