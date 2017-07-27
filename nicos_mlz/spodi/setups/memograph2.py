description = 'memograph readout'

includes = []

group = 'optional'

devices = dict(
    t_in_spodi2    = device('nicos_mlz.frm2.devices.memograph.MemographValue',
                            hostname = 'memograph-uja02.care.frm2',
                            group = 2,
                            valuename = 'T_in SPODI2',
                            description = 'inlet temperature memograph',
                            fmtstr = '%.2F',
                            warnlimits = (-1, 17.5), #-1 no lower value
                            unit = 'degC',
                           ),
    t_out_spodi2   = device('nicos_mlz.frm2.devices.memograph.MemographValue',
                            hostname = 'memograph-uja02.care.frm2',
                            group = 2,
                            valuename = 'T_out SPODI2',
                            description = 'outlet temperature memograph',
                            pollinterval = 30,
                            maxage = 60,
                            fmtstr = '%.2F',
                            unit = 'degC',
                           ),
    p_in_spodi2    = device('nicos_mlz.frm2.devices.memograph.MemographValue',
                            hostname = 'memograph-uja02.care.frm2',
                            group = 2,
                            valuename = 'P_in SPODI2',
                            description = 'inlet pressure memograph',
                            pollinterval = 30,
                            maxage = 60,
                            fmtstr = '%.2F',
                            unit = 'bar',
                           ),
    p_out_spodi2   = device('nicos_mlz.frm2.devices.memograph.MemographValue',
                            hostname = 'memograph-uja02.care.frm2',
                            group = 2,
                            valuename = 'P_out SPODI2',
                            description = 'outlet pressure memograph',
                            pollinterval = 30,
                            maxage = 60,
                            fmtstr = '%.2F',
                            unit = 'bar',
                           ),
    flow_in_spodi2 = device('nicos_mlz.frm2.devices.memograph.MemographValue',
                            hostname = 'memograph-uja02.care.frm2',
                            group = 2,
                            valuename = 'FLOW_in SPODI2',
                            description = 'inlet flow memograph',
                            pollinterval = 30,
                            maxage = 60,
                            fmtstr = '%.2F',
                            warnlimits = (0.2, 100), #100 no upper value
                            unit = 'l/min',
                           ),
    flow_out_spodi2 = device('nicos_mlz.frm2.devices.memograph.MemographValue',
                             hostname = 'memograph-uja02.care.frm2',
                             group = 2,
                             valuename = 'FLOW_out SPODI2',
                             description = 'outlet flow memograph',
                             pollinterval = 30,
                             maxage = 60,
                             fmtstr = '%.2F',
                             unit = 'l/min',
                            ),
    leak_spodi2    = device('nicos_mlz.frm2.devices.memograph.MemographValue',
                            hostname = 'memograph-uja02.care.frm2',
                            group = 2,
                            valuename = 'Leak SPODI2',
                            description = 'leakage memograph',
                            pollinterval = 30,
                            maxage = 60,
                            fmtstr = '%.2F',
                            warnlimits = (-1, 1), #-1 no lower value
                            unit = 'l/min',
                           ),
    cooling_spodi2 = device('nicos_mlz.frm2.devices.memograph.MemographValue',
                            hostname = 'memograph-uja02.care.frm2',
                            group = 2,
                            valuename = 'Cooling SPODI2',
                            description = 'cooling power memograph',
                            pollinterval = 30,
                            maxage = 60,
                            fmtstr = '%.2F',
                            unit = 'kW',
                           ),
)