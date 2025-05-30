simulation_file = 'qeyssat_2035_direct_overpass.json';

% if ~exist('simulation_file', 'var')
%     error('No filename provided. Usage: matlab -batch "simulation_file=''yourfile.json''; myscript"');
% end
% disp(['Running simulation: ', simulation_file]);

% add qrackling to path
qrackling_dir = '../../Qrackling';
addpath(genpath(qrackling_dir))

wdir = pwd();
simulations_dir = fullfile(wdir, 'simulations');

% get simulation from file
simulation_file_path = fullfile(simulations_dir, simulation_file);
str = fileread(simulation_file_path);
sim = jsondecode(str);

% set simulation time
pass_time = datetime( ...
    sim.simulation.pass_time.year,   ...
    sim.simulation.pass_time.month,  ...
    sim.simulation.pass_time.day,    ...
    sim.simulation.pass_time.hour,   ...
    sim.simulation.pass_time.minute, ...
    sim.simulation.pass_time.second  ...
);
start_time = pass_time - sim.simulation.duration.day / 2;
stop_time = pass_time + sim.simulation.duration.day / 2;

% setup components
source = components.Source( ...
    sim.source.Wavelength, ...
    'Repetition_Rate',     sim.source.Repetition_Rate, ...
    'MPN_Signal',          sim.source.MPN_Signal       ...
);

qeyssat_telescope = components.Telescope( ...
    0.25,              ...
    'Wavelength',      sim.source.Wavelength, ...
    'Pointing_Jitter', 1e-6                   ...
);

uplink_camera = beacon.Camera( ...
    qeyssat_telescope ...
);

bb84_detector = components.Detector( ...
    sim.source.Wavelength,             ...
    sim.bb84_detector.Repetition_Rate, ...
    sim.bb84_detector.Time_Gate_Width, ...
    sim.bb84_detector.Spectral_Filter, ...
    'Preset',                          components.loadPreset(string(sim.bb84_detector.Preset)) ...
);

% satellite = nodes.Satellite( ...
%     qeyssat_telescope, ...
%     'Camera',     uplink_camera,           ...
%     'Name',       sim.satellite.Name,      ...
%     'KeplerElements', [ ...
%         sim.satellite.KeplerElements.semi_major_axis,       ...
%         sim.satellite.KeplerElements.eccentricity,          ...
%         sim.satellite.KeplerElements.inclination,           ...
%         sim.satellite.KeplerElements.raan,                  ...
%         sim.satellite.KeplerElements.argument_of_periapsis, ...
%         sim.satellite.KeplerElements.mean_anomaly,          ...    
%     ], ...
%     'startTime',  start_time,              ...
%     'stopTime',   stop_time,               ...
%     'sampleTime', sim.satellite.sampleTime ...
% );
satellite = SPOQC(785);

ground_station = HubOpticalGroundStation(sim.source.Wavelength);

%% environment
loc = which('nodes.Satellite');
[path, ~, ~] = fileparts(loc);
elems = strsplit(path, filesep);
path_root = string(join(elems(1:end-2), filesep)) + filesep;
whichSeparator = @(Path, Sep) Sep{cellfun(@(sep) contains(Path, sep), Sep)};
MakePathNative = @(Path) strjoin(strsplit(Path, whichSeparator(Path, {'/', '\'})), filesep);
brightness_data = load(path_root + MakePathNative("Examples/Data/measured background counts/HWU_Experimental_Sky_Brightness.mat")).data;

sky_brightness = permute(brightness_data.Spectral_Pointance,[3,1,2]);

sky_elevations = linspace(0, 90, 46);
sky_headings = linspace(0, 360, 91);

mapped_night_sky = environment.mapToEnvironment( ...
    brightness_data.Headings,   ...
    brightness_data.Elevations, ...
    sky_brightness,             ... %780nm is at index 1
    sky_headings,               ...
    sky_elevations,             ...
    "Wavelength",               brightness_data.Wavelengths ...
);

loc = which('utilities.readModtranFile');
[path, ~, ~] = fileparts(loc);
elems = strsplit(path, filesep);
path_root = string(join(elems(1:end-1), filesep)) + filesep;
example_path = "Examples/Data/atmospheric transmittance/varying elevation MODTRAN data 2/";
data_path = path_root + MakePathNative(example_path);
paths = dir(data_path);
FilterStrings = @(haystack, needle) haystack(arrayfun(@(h) contains(h, needle), haystack));
csv_files = FilterStrings({paths.name}, ".csv");

schema = {'data_type', 'visibility', 'visibility_label', 'zenith_label', 'zenith_angle', 'end'};
file_details = cellfun(@(f) cell2struct(split(f, "_"), schema), csv_files);
elevations = sort(str2double(replace({file_details.zenith_angle}, "deg", "")));
sorted_file_names = string( ...
    arrayfun( ...
        @(n) csv_files(contains(csv_files, "_" + num2str(n) + "deg")), ...
        elevations, ...
        UniformOutput=false)');

wavelengths = [];
transmissions = [];
for f = sorted_file_names'
    [w, t] = utilities.readModtranFile(char(data_path + f));
    wavelengths = [wavelengths, w(~isnan(w))];
    transmissions = [transmissions, t(~isnan(t))];
end
[sky_transmission, headings] = environment.allSkyTransmission(transmissions, wavelengths(:, 1), elevations);

Extrema = @(arr) [min(arr), max(arr)];
InRange = @(value, bounds) all([any(value >= bounds), any(value <= bounds)]);
Iota = @(x) linspace(0, x, x+1);
Take = @(arr, choices) arr(choices);
IndexOfWavelength = @(wvls, choice) Take(Iota(numel(wvls)), wvls == choice) * InRange(wvls, Extrema(wvls));
DataAtWavelength = @(data, wvls, choice) squeeze(data(IndexOfWavelength(wvls, choice), :, :));
% Picking an example wavelength of 600nm we can then plot the result.

tmp_size = [numel(brightness_data.Wavelengths), size(squeeze(sky_transmission(1, :, :)))];
transmission_at_wavelength = zeros(tmp_size);
for i = 1:numel(brightness_data.Wavelengths)
    wvl = brightness_data.Wavelengths(i);
    transmission_at_wavelength(i, :, :) = ...
        DataAtWavelength(sky_transmission, wavelengths(:, 1), wvl);
end

mapped_transmission = environment.mapToEnvironment( ...
    headings,                   ...
    elevations,                 ...
    flip(transmission_at_wavelength,3), ...
    sky_headings,               ...
    sky_elevations,             ...
    "Wavelengths",              brightness_data.Wavelengths ...
);

env = environment.Environment( ...
    sky_headings,                ...
    sky_elevations,              ...
    brightness_data.Wavelengths, ...
    mapped_night_sky,            ...
    mapped_transmission          ...
);

%% simulation
if sim.simulation.scheme == "uplink"
    satellite.Detector = bb84_detector;
    ground_station.Source = source;

    simulation = nodes.QkdPassSimulation( ...
        satellite,       ...
        ground_station,  ...
        protocol.bbm92_cw(), ...
        Environment=env  ...
    );
    QKD_figure = simulation.plotResult( ...
        satellite,      ...
        ground_station, ...
        "mask",         "Elevation"...
    );
else
    satellite.Source = source;
    ground_station.Detector = bb84_detector;
    
    simulation = nodes.QkdPassSimulation( ...
        ground_station,  ...
        satellite,       ...
        protocol.bbm92_cw(), ...
        Environment=env  ...
    );
    QKD_figure = simulation.plotResult( ...
        ground_station, ...
        satellite,      ...
        "mask",         "Elevation" ...
    );
end

% format data
headers = { ...
    'Elevation',  ...
    'Geometric',  ...
    'Optical',    ...
    'APT',        ...
    'Turbulence', ...
    'Atmospheric',
};
data = [ ...
    simulation.elevation'                 ...
    simulation.losses.geometric.values'   ...
    simulation.losses.optical.values'     ...
    simulation.losses.apt.values'         ...
    simulation.losses.turbulence.values'  ...
    simulation.losses.atmospheric.values' ...
];
results_file = strjoin([ ...
    string(datetime(pass_time, 'Format', 'yyyy_MM_dd_HH_mm_ss')), ...
    '-',                                                          ...
    string(max(simulation.elevation)),                            ...
    '.csv'
],'');

% setup results path
results_dir = fullfile(wdir, 'results');
[filepath, name, ext] = fileparts(simulation_file);
simulation_result_dir = fullfile(results_dir, name);
mkdir(simulation_result_dir);

% write data
simulation_result_path = fullfile(simulation_result_dir, results_file);
writetable( ...
    array2table(data, 'VariableNames', headers), ...
    simulation_result_path                       ...
);

% keep figure open until manually close
uiwait(gcf);

% cleanup
rmpath(genpath(qrackling_dir))