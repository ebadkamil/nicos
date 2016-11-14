# -*- coding: utf-8 -*-

description = "High voltage setup"
group = "optional"

nethost = "heidi22.poli.frm2"

devices = dict(
    fug = device("devices.taco.VoltageSupply",
                 description = "High voltage",
                 tacodevice = "//%s/heidi2/fug/ctrl" % nethost,
                 abslimits = (-10, 10),
                 unit = "kV",
                 pollinterval = 5,
                 maxage = 6,
                ),
    fugwatch = device("poli.highvoltage.HVWatch",
                      description = "En-/Disable Watchdog for controlling hv "
                                    "in respect to temperature deviation",
                      states = ["off", "on"],
                     ),
)
