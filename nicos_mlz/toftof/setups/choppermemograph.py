description = 'memograph readout for the chopper cooling system'

group = 'lowlevel'

memograph = 'memograph07.care.frm2'
channel = 'TOF2'
system = 'chopper'
_group = 2

devices = {
    't_in_%s_cooling' % system[:2]: device('nicos_mlz.devices.memograph.MemographValue',
        hostname = '%s' % memograph,
        group = _group,
        valuename = 'T_in %s' % channel,
        description = 'inlet temperature %s cooling' % system,
        fmtstr = '%.1f',
        warnlimits = (-1, 17.5),  # -1 no lower value
        lowlevel = False,
        unit = 'degC',
    ),
    't_out_%s_cooling' % system[:2]: device('nicos_mlz.devices.memograph.MemographValue',
        hostname = '%s' % memograph,
        group = _group,
        valuename = 'T_out %s' % channel,
        description = 'outlet temperature %s cooling' % system,
        fmtstr = '%.1f',
        lowlevel = False,
        unit = 'degC',
    ),
    'p_in_%s_cooling' % system[:2]: device('nicos_mlz.devices.memograph.MemographValue',
        hostname = '%s' % memograph,
        group = _group,
        valuename = 'P_in %s' % channel,
        description = 'inlet pressure %s cooling' % system,
        fmtstr = '%.1f',
        lowlevel = False,
        unit = 'bar',
    ),
    'p_out_%s_cooling' % system[:2]: device('nicos_mlz.devices.memograph.MemographValue',
        hostname = '%s' % memograph,
        group = _group,
        valuename = 'P_out %s' % channel,
        description = 'outlet pressure %s cooling' % system,
        fmtstr = '%.1f',
        lowlevel = False,
        unit = 'bar',
    ),
    'flow_in_%s_cooling' % system[:2]: device('nicos_mlz.devices.memograph.MemographValue',
        hostname = '%s' % memograph,
        group = _group,
        valuename = 'FLOW_in %s' % channel,
        description = 'inlet flow %s cooling' % system,
        fmtstr = '%.1f',
        warnlimits = (0.2, 100),  # 100 no upper value
        lowlevel = False,
    ),
    'flow_out_%s_cooling' % system[:2]: device('nicos_mlz.devices.memograph.MemographValue',
        hostname = '%s' % memograph,
        group = _group,
        valuename = 'FLOW_out %s' % channel,
        description = 'outlet flow %s cooling' % system,
        fmtstr = '%.1f',
        lowlevel = False,
        unit = 'l/min',
    ),
    'leak_%s_cooling' % system[:2]: device('nicos_mlz.devices.memograph.MemographValue',
        hostname = '%s' % memograph,
        group = _group,
        valuename = 'Leak %s' % channel,
        description = 'leakage %s cooling' % system,
        fmtstr = '%.1f',
        warnlimits = (-1, 1),  # -1 no lower value
        lowlevel = False,
        unit = 'l/min',
    ),
    'power_%s_cooling' % system[:2]: device('nicos_mlz.devices.memograph.MemographValue',
        hostname = '%s' % memograph,
        group = _group,
        valuename = 'Cooling %s' % channel,
        description = 'cooling %s cooling' % system,
        fmtstr = '%.1f',
        lowlevel = False,
        unit = 'kW',
    ),
}
