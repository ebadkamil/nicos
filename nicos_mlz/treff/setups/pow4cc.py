# -*- coding: utf-8 -*-

description = "Toellner power supply 4 current setup"
group = "optional"

tango_base = "tango://phys.treff.frm2:10000/treff/"

excludes = ["pow4vc"]

devices = dict(
    pow4hf   = device('nicos.devices.tango.PowerSupply',
                      description = "Power supply 4 current control ch 1",
                      tangodevice = tango_base + "toellner/pow4hf",
                     ),
    pow4grad = device('nicos.devices.tango.PowerSupply',
                      description = "Power supply 4 current control ch 2",
                      tangodevice = tango_base + "toellner/pow4grad",
                     ),
 )