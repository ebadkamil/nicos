

devices = dict(
    selector_speed = device('nicos.devices.generic.VirtualMotor',
        abslimits = (0, 28500),
        precision = 10,
        unit = 'rpm',
    ),
    selcradle = device('nicos.devices.generic.VirtualMotor',
        abslimits = (-10, 10),
        precision = 0.001,
        unit = 'deg',
    ),
    selector_lambda = device('nicos_mlz.reseda.devices.astrium.SelectorLambda',
        seldev = 'selector_speed',
        tiltdev = 'selcradle',
        unit = 'A',
        fmtstr = '%.2f',
        twistangle = 48.27,
        length = 0.25,
        radius = 0.16,
        beamcenter = 0.115,
        maxspeed = 28500,
    ),
    selector_delta_lambda = device('nicos_mlz.reseda.devices.astrium.SelectorLambdaSpread',
        lamdev = 'selector_lambda',
        unit = '%',
        fmtstr = '%.1f',
        n_lamellae = 64,
        d_lamellae = 0.8,
        diameter = 0.32,
    ),

    arm1_rot = device('nicos.devices.generic.VirtualMotor',
        abslimits = (-95, 5),
        fmtstr = '%.3f',
        unit = 'deg',
        curvalue = -55,
    ),
    arm2_rot = device('nicos.devices.generic.VirtualMotor',
        abslimits = (-15, 58),
        fmtstr = '%.3f',
        unit = 'deg',
        curvalue = 0,
    ),
    armctrl = device('nicos_mlz.reseda.devices.ArmController',
        arm1 = 'arm1_rot',
        arm2 = 'arm2_rot',
        minangle = 50,
    ),
    psd_channel = device('nicos_virt_mlz.reseda.devices.CascadeDetector',
        description = 'CASCADE detector channel',
        foilsorder = [5, 4, 3, 0, 1, 2, 6, 7],
    ),
)
