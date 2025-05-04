function hogs = HOGS_QEYSSAT(options)
%% a modification of the existing HOGS model which implements QEYSSAT uplink sources and
%appropriate receiver architecture

arguments
    options.Protocol {mustBeMember(options.Protocol,{'BB84','BBM92'})} = 'BB84';
end

%% use HOGS with 808nm detectors as a baseline
    hogs = HOGS(785);


%% then add a source dependent on the protocol in use
    switch options.Protocol 
        case 'BB84'
        QEYSSAT_Source = components.Source(785,...
                                        'Repetition_Rate',1E8,...
                                        'MPN_Signal',0.8,...
                                        'MPN_Decoy',0.3,...
                                        'Probability_Signal',0.5,...
                                        'Probability_Decoy',0.25,...
                                        'State_Prep_Error',0.0025);

        case 'BBM92'
        QEYSSAT_Source = components.Source(785,...
                                        'Repetition_Rate',660E6,...
                                        'MPN_Signal',0.09,...
                                        'State_Prep_Error',0.0025);
    end

    hogs.Source = QEYSSAT_Source;
