description = 'Vacuum sensors of detector and collimation tube'

group = 'lowlevel'

nethost = 'sans1srv.sans1.frm2'

devices = dict(
    det_tube = device('nicos.devices.taco.AnalogInput',
        description = 'pressure detector tube: Tube',
        tacodevice = '//%s/sans1/tube/p1' % (nethost,),
        fmtstr = '%.4G',
        pollinterval = 15,
        maxage = 60,
        lowlevel = True,
    ),
    det_nose = device('nicos.devices.taco.AnalogInput',
        description = 'pressure detector tube: Nose',
        tacodevice = '//%s/sans1/tube/p2' % (nethost,),
        fmtstr = '%.4G',
        pollinterval = 15,
        maxage = 60,
        lowlevel = True,
    ),
    # det_p3 = device('nicos.devices.taco.AnalogInput',
    #     description = 'pressure detector tube: NOT IN USE!!!',
    #     tacodevice = '//%s/sans1/tube/p3' % (nethost, ),
    #     fmtstr = '%.4G',
    #     pollinterval = 15,
    #     maxage = 60,
    #     lowlevel = True,
    # ),
    coll_tube = device('nicos.devices.taco.AnalogInput',
        description = 'pressure collimation tube: Tube',
        tacodevice = '//%s/sans1/coll/p1' % (nethost,),
        fmtstr = '%.4G',
        pollinterval = 15,
        maxage = 60,
        lowlevel = True,
    ),
    coll_nose = device('nicos.devices.taco.AnalogInput',
        description = 'pressure collimation tube: Nose',
        tacodevice = '//%s/sans1/coll/p2' % (nethost,),
        fmtstr = '%.4G',
        pollinterval = 15,
        maxage = 60,
        lowlevel = True,
    ),
    coll_pump = device('nicos.devices.taco.AnalogInput',
        description = 'pressure collimation tube: Pump',
        tacodevice = '//%s/sans1/coll/p3' % (nethost,),
        fmtstr = '%.4G',
        pollinterval = 15,
        maxage = 60,
        lowlevel = True,
    ),
)
