description = 'Motor for FOV camera translation in large detector box'

group = 'optional'

devices = dict(
    ccdtx = device('nicos.devices.taco.Motor',
        description = 'Camera Translation X',
        tacodevice = 'antares/copley/m07',
        abslimits = (-9999, 9999),
        userlimits = (-0, 693),
    ),
)
