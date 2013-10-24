description = 'memograph readout'
devices = dict(
    t_in_memograph_sans1 = device('frm2.memograph.MemographValue',
                            hostname = 'memograph03.care.frm2',
                            group = 2,
                            valuename = 'T_in SANS-1',
                            description = 'inlet temperature memograph',
    ),
    t_out_memograph_sans1 = device('frm2.memograph.MemographValue',
                            hostname = 'memograph03.care.frm2',
                            group = 2,
                            valuename = 'T_out SANS-1',
                            description = 'outlet temperature memograph',
    ),
    p_in_memograph_sans1 = device('frm2.memograph.MemographValue',
                            hostname = 'memograph03.care.frm2',
                            group = 2,
                            valuename = 'P_in SANS-1',
                            description = 'inlet pressure memograph',
    ),
    p_out_memograph_sans1 = device('frm2.memograph.MemographValue',
                            hostname = 'memograph03.care.frm2',
                            group = 2,
                            valuename = 'P_out SANS-1',
                            description = 'outlet pressure memograph',
    ),
    flow_in_memograph_sans1 = device('frm2.memograph.MemographValue',
                            hostname = 'memograph03.care.frm2',
                            group = 2,
                            valuename = 'FLOW_in SANS-1',
                            description = 'inlet flow memograph',
    ),
    flow_out_memograph_sans1 = device('frm2.memograph.MemographValue',
                            hostname = 'memograph03.care.frm2',
                            group = 2,
                            valuename = 'FLOW_out SANS-1',
                            description = 'outlet flow memograph',
    ),
    leak_memograph_sans1 = device('frm2.memograph.MemographValue',
                            hostname = 'memograph03.care.frm2',
                            group = 2,
                            valuename = 'Leak SANS-1',
                            description = 'leakage memograph',
    ),
    cooling_memograph_sans1 = device('frm2.memograph.MemographValue',
                            hostname = 'memograph03.care.frm2',
                            group = 2,
                            valuename = 'Cooling SANS-1',
                            description = 'cooling power memograph',
    ),
)
