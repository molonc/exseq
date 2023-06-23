clear a m
a = arduino();
m = servo(a, 'D4', 'MinPulseDuration', 500*10^-6, 'MaxPulseDuration', 2500*10^-6);

for angle = 0:0.25:1 % angles of servo: 0.5 then 0.75
writePosition(m, angle); % setting the servo to that angle
current_pos = readPosition(m);
current_pos = current_pos*180; % converts angle to degrees
fprintf('Current motor position is %d degrees\n', current_pos);
pause(2);
end