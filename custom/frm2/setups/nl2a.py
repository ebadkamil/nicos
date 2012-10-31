description = 'FRM II neutron guide line 2a shutter'

group = 'lowlevel'

includes = ['guidehall']

nethost = 'tacodb.taco.frm2'

devices = dict(
    NL2a     = device('nicos.taco.NamedDigitalInput',
                      description = 'NL2a shutter status',
                      mapping = {0: 'closed', 1: 'open'},
                      pollinterval = 60,
                      maxage = 120,
                      tacodevice = '//%1/frm2/shutter/nl2a' % (nethost, ),
)
