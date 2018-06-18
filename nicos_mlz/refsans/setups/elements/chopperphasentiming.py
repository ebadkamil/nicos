description = 'Chopper Phasentiming, readout for light barrier and Encoderindex'

group = 'optional'

all_lowlevel = False  # or True
#atts = 'nicos.devices.generic.ParamDevice'
atts = 'nicos_mlz.refsans.devices.gkssjson.CPTReadout'

devices = dict(
    #cpt = device('nicos_mlz.refsans.devices.gkssjson.CPTReadout',
    #    description = description,
    #    lowlevel = all_lowlevel,
    #    url = 'http://cpt.refsans.frm2/json?1',
    #    valukey = 'chopper_act',
    #    timeout = .3,
    #    unit = '',
    #),
    cpt1 = device(atts,
        description = 'Disc 1 light barrier '+description,
        url = 'http://cpt.refsans.frm2/json?1',
        valuekey = 'chopper_act',
        timeout = .3,
        channel = 0,
        offset = 0,
        unit = 'rpm',
    ),
     cpt2 = device(atts,
         description = 'Disc 2 light barrier '+description,
         url = 'http://cpt.refsans.frm2/json?1',
         valuekey = 'chopper_act',
         timeout = .3,
         channel = 1,
         offset = 103,
         unit = 'deg',
     ),
    cpt3 = device(atts,
        description = 'Disc 3 light barrier '+description,
        url = 'http://cpt.refsans.frm2/json?1',
        valuekey = 'chopper_act',
        timeout = .3,
        channel = 2,
        offset = 167,
        unit = 'deg',
    ),
    cpt4 = device(atts,
        description = 'Disc 4 light barrier '+description,
        url = 'http://cpt.refsans.frm2/json?1',
        valuekey = 'chopper_act',
        timeout = .3,
        channel = 3,
        offset = 136,
        unit = 'deg',
    ),
    cpt5 = device(atts,
        description = 'Disc 5 index '+description,
        url = 'http://cpt.refsans.frm2/json?1',
        valuekey = 'chopper_act',
        timeout = .3,
        channel = 10,
        offset = 106,
        unit = 'deg',
    ),
    cpt6 = device(atts,
        description = 'Disc 6 index '+description,
        url = 'http://cpt.refsans.frm2/json?1',
        valuekey = 'chopper_act',
        timeout = .3,
        channel = 11,
        offset = 8,
        unit = 'deg',
    ),
)
