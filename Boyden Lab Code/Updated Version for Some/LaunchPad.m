%% initialize daq and its digital and analog outputs
% Dev5 for dragonfly, Dev2 for SoRa
s = daq('ni');
addoutput(s, 'Dev5', 'Port1/Line0:3', 'Digital');
addoutput(s,'Dev5',{'0', '1'},'Voltage'); 
pause(1);

% Set valve definitions and initialize MVP
valveP1=[1 0 0 0 0 0]; % 1X PBS
valveP2=[0 1 0 0 0 0]; % Hybridization Solution
valveP3=[1 1 0 0 0 0]; % Ligation Buffer
valveP4=[0 0 1 0 0 0]; % Ligation Solution
valveP5=[1 0 1 0 0 0]; % Air
valveP6=[0 1 1 0 0 0]; % Imaging Buffer
valveP7=[1 1 1 0 0 0]; % PBST
valveP8=[0 0 0 1 0 0]; % Stripping Solution
valveInitialize=[1 1 1 1 0 0];

write(s, valveInitialize)
pause(5)

clear a m 


a = arduino();
m = servo(a, 'D4', 'MinPulseDuration', 670*10^-6, 'MaxPulseDuration', 2600*10^-6);
%% Modules

% S01_Hyb_Lig_clean
% 
% S02_Hyb_Lig_rinse
% 
% S03_Hyb_Lig_clear
% 
% S04_Stripping
% 
% S05_PBST_short
% 
% S06_PBS_rinse
% 
% S07_Air_clear 
% 
% S08_Hybridization
% 
% S09_PBST_short
% 
% S10_PBS_rinse
% 
% S11_Air_clear
% 
% S12_Ligation_buffer
% 
% S13_Ligation
% 
% S14_PBST_long
% 
% S10_PBS_rinse

% S11_Air_clear
% 
% S15_ImagingBufferSetup
% % 
% S16_Imaging8hours_slow