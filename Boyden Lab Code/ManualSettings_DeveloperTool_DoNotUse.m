%% Set angle
while angle < 0.75
    for angle = angle:0.05:0.75
    writePosition(m, angle);
    pause(2);
    end
end


%% pick valve, set speed, and turn on

outputSingleScan(s,valveP7);
pause(5);


on_off = 3; % x<1.5 = on; x>3 = off
speed = 1; % 
outputSingleScan(s,[0 0 0 0 on_off speed]);

while on_off == 1
    
    for angle = 0.6:-0.05:0.35
    writePosition(m, angle);
    pause(2);
    end
    
    pause(5);
    
    for angle = 0.35:0.05:0.6
        writePosition(m, angle);
        pause(2);
    end
    pause(5);
end
% 
% pause (10)
% 
% speed = 2;
% outputSingleScan(s,[0 0 0 0 on_off speed]);
% 
% pause (10)
% 
% speed = 3;
% outputSingleScan(s,[0 0 0 0 on_off speed]);
% 
% pause (60)
% 
% 
% speed = 2;
% outputSingleScan(s,[0 0 0 0 on_off speed]);
% 
% pause (10)
% 
% speed = 1; % 
% outputSingleScan(s,[0 0 0 0 on_off speed]);
% 
% pause (10)

% on_off = 3;
% outputSingleScan(s,[0 0 0 0 on_off speed]);