% a script which simulates a QEYSSAT pass over HOGS

% add qrackling to path
qrackling_dir = '../../Qrackling';
addpath(genpath(qrackling_dir))

%% what protocol and what direction?
Protocol = 'BBM92';
Link_Direction = 'Up';

%% Build and appropriately modify HOGS
hogs = HOGS_QEYSSAT("Protocol",Protocol);

%% build QEYSSAT
qeyssat = QEYSSAT('Protocol',Protocol);

%% load in environment using a clear night with 50km visibility
env = environment.Environment.Load('Examples/Data/atmospheric transmittance/Dark Environment 20km.mat');


%% perform simulations
%QKD link
switch Protocol
    case 'BB84'
        Protocol_Obj = protocol.decoyBB84;
    case 'BBM92'
        Protocol_Obj = protocol.bbm92_cw;
        %set coincidence window which is acceptable
        Protocol_Obj.coincidence_window = 2E-9; 
end

switch Link_Direction
    case 'Down'
QKDResults = nodes.QkdPassSimulation(hogs,...
    qeyssat,...
    Protocol_Obj,...
    'Environment',env);
%Beacon downlink
%DownlinkBeaconResults = beacon.beaconSimulation(hogs,qeyssat,"Environment",env);
%Beacon uplink
%UplinkBeaconResults = beacon.beaconSimulation(qeyssat,hogs,"Environment",env);
    case 'Up'
QKDResults = nodes.QkdPassSimulation(qeyssat,...
    hogs,...
    Protocol_Obj,...
    'Environment',env);
%Beacon downlink
%DownlinkBeaconResults = beacon.beaconSimulation(qeyssat,hogs,"Environment",env);
%Beacon uplink
%UplinkBeaconResults = beacon.beaconSimulation(hogs,qeyssat,"Environment",env);
end


%% plot
plot(QKDResults)
%plot(DownlinkBeaconResults)
%plot(UplinkBeaconResults)

% cleanup
rmpath(genpath(qrackling_dir))