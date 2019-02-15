description = 'memograph readout'

group = 'lowlevel'

devices = dict(
    t_in_memograph = device('nicos_mlz.devices.memograph.MemographValue',
        hostname = 'memograph03.care.frm2',
        group = 2,
        valuename = 'T_in SANS1',
        description = 'inlet temperature memograph',
        fmtstr = '%.2F',
        warnlimits = (-1, 17.5),  # -1 no lower value
        lowlevel = True,
    ),
    t_out_memograph = device('nicos_mlz.devices.memograph.MemographValue',
        hostname = 'memograph03.care.frm2',
        group = 2,
        valuename = 'T_out SANS1',
        description = 'outlet temperature memograph',
        fmtstr = '%.2F',
        lowlevel = True,
    ),
    p_in_memograph = device('nicos_mlz.devices.memograph.MemographValue',
        hostname = 'memograph03.care.frm2',
        group = 2,
        valuename = 'P_in SANS1',
        description = 'inlet pressure memograph',
        fmtstr = '%.2F',
        lowlevel = True,
    ),
    p_out_memograph = device('nicos_mlz.devices.memograph.MemographValue',
        hostname = 'memograph03.care.frm2',
        group = 2,
        valuename = 'P_out SANS1',
        description = 'outlet pressure memograph',
        fmtstr = '%.2F',
        lowlevel = True,
    ),
    flow_in_memograph = device('nicos_mlz.devices.memograph.MemographValue',
        hostname = 'memograph03.care.frm2',
        group = 2,
        valuename = 'FLOW_in SANS1',
        description = 'inlet flow memograph',
        fmtstr = '%.2F',
        warnlimits = (0.2, 100),  # 100 no upper value
        lowlevel = True,
    ),
    flow_out_memograph = device('nicos_mlz.devices.memograph.MemographValue',
        hostname = 'memograph03.care.frm2',
        group = 2,
        valuename = 'FLOW_out SANS1',
        description = 'outlet flow memograph',
        fmtstr = '%.2F',
        lowlevel = True,
    ),
    leak_memograph = device('nicos_mlz.devices.memograph.MemographValue',
        hostname = 'memograph03.care.frm2',
        group = 2,
        valuename = 'Leak SANS1',
        description = 'leakage memograph',
        fmtstr = '%.2F',
        warnlimits = (-1, 1),  # -1 no lower value
        lowlevel = True,
    ),
    cooling_memograph = device('nicos_mlz.devices.memograph.MemographValue',
        hostname = 'memograph03.care.frm2',
        group = 2,
        valuename = 'Cooling SANS1',
        description = 'cooling memograph',
        fmtstr = '%.2F',
        lowlevel = True,
    ),
)
