description = 'Monochromator tower devices'

group = 'lowlevel'

tango_base = 'tango://kompasshw.kompass.frm2:10000/kompass/'

devices = dict(
    # A1
    mth_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base + 'mono/mth_m',
        fmtstr = '%.4f',
        lowlevel = True,
    ),
    mth_c = device('nicos.devices.tango.Sensor',
        tangodevice = tango_base + 'mono/mth_c',
        fmtstr = '%.4f',
        lowlevel = True,
    ),
    mth = device('nicos.devices.generic.Axis',
        description = 'monochromator theta (A1)',
        motor = 'mth_m',
        coder = 'mth_c',
        fmtstr = '%.3f',
        precision = 0.001,
    ),
    # A2
    mtt_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base + 'mono/mtt_m',
        fmtstr = '%.4f',
        lowlevel = True,
    ),
    mtt_c = device('nicos.devices.tango.Sensor',
        tangodevice = tango_base + 'mono/mtt_c',
        fmtstr = '%.4f',
        lowlevel = True,
    ),
    air_mono = device('nicos.devices.tango.DigitalOutput',
        tangodevice = tango_base + 'aircontrol/plc_airpads_sampletable',
        lowlevel = True,
    ),
    mtt = device('nicos_mlz.mira.devices.axis.HoveringAxis',
        description = 'primary spectrometer angle (A2)',
        motor = 'mtt_m',
        coder = 'mtt_c',
        startdelay = 2,
        stopdelay = 2,
        switch = 'air_mono',
        switchvalues = (0, 1),
        fmtstr = '%.4f',
        precision = 0.001,
    ),
    mx_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base + 'mono/mx_m',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    mx_c = device('nicos.devices.tango.Sensor',
        tangodevice = tango_base + 'mono/mx_c',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    mx = device('nicos.devices.generic.Axis',
        description = 'monochromator table X',
        motor = 'mx_m',
        coder = 'mx_m',
        fmtstr = '%.2f',
        precision = 0.05,
    ),
    my_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base + 'mono/my_m',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    my_c = device('nicos.devices.tango.Sensor',
        tangodevice = tango_base + 'mono/my_c',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    my = device('nicos.devices.generic.Axis',
        description = 'monochromator table Y',
        motor = 'my_m',
        coder = 'my_m',
        fmtstr = '%.2f',
        precision = 0.05,
    ),
    mc_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base + 'mono/mc_m',
        fmtstr = '%.1f',
        lowlevel = True,
    ),
    mc_c = device('nicos.devices.tango.Sensor',
        tangodevice = tango_base + 'mono/mc_c',
        fmtstr = '%.1f',
        lowlevel = True,
    ),
    mc = device('nicos.devices.generic.Axis',
        description = 'monochromator table cradle',
        motor = 'mc_m',
        coder = 'mc_m',  # 'mc_c',
        fmtstr = '%.1f',
        precision = 0.05,
    ),
    mfv_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base + 'mono/mfv_m',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    # currently unused
    #mfv_c = device('nicos.devices.tango.Sensor',
    #    tangodevice = tango_base + 'mono/mfv_c',
    #    fmtstr = '%.2f',
    #    lowlevel = True,
    #),
    mfv = device('nicos.devices.generic.Axis',
        description = 'monochromator vertical focus',
        motor = 'mfv_m',
        coder = 'mfv_m',
        fmtstr = '%.2f',
        precision = 0.01,
    ),
    mfh_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base + 'mono/mfh_m',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    # currently broken
    #mfh_c = device('nicos.devices.tango.Sensor',
    #    tangodevice = tango_base + 'mono/mfh_c',
    #    fmtstr = '%.2f',
    #    lowlevel = True,
    #),
    mfh = device('nicos.devices.generic.Axis',
        description = 'monochromator horizontal focus',
        motor = 'mfh_m',
        coder = 'mfh_m',
        fmtstr = '%.2f',
        precision = 0.01,
    ),

    mono = device('nicos.devices.tas.Monochromator',
        description = 'monochromator unit to move incoming wavevector',
        unit = 'A-1',
        theta = 'mth',
        twotheta = 'mtt',
        focush = 'mfh',
        focusv = 'mfv',
        # abslimits = (0.1, 10),
        abslimits = (1.08, 3.3),
        focmode = 'manual',  # for now
        hfocuspars = [0],
        vfocuspars = [0],
        scatteringsense = 1,
        crystalside = 1,
        dvalue = 3.355,
    ),

    mshl_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base + 'slit/mshl_m',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    # currently unused
    #mshl_c = device('nicos.devices.tango.Sensor',
    #    tangodevice = tango_base + 'mono/mshl_c',
    #    fmtstr = '%.2f',
    #    lowlevel = True,
    #),
    mshl = device('nicos.devices.generic.Axis',
        description = 'monochromator slit left',
        motor = 'mshl_m',
        coder = 'mshl_m',
        fmtstr = '%.2f',
        precision = 0.01,
        lowlevel = True,
    ),

    mshr_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base + 'slit/mshr_m',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    # currently unused
    #mshr_c = device('nicos.devices.tango.Sensor',
    #    tangodevice = tango_base + 'mono/mshr_c',
    #    fmtstr = '%.2f',
    #    lowlevel = True,
    #),
    mshr = device('nicos.devices.generic.Axis',
        description = 'monochromator slit right',
        motor = 'mshr_m',
        coder = 'mshr_m',
        fmtstr = '%.2f',
        precision = 0.01,
        lowlevel = True,
    ),

    msvb_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base + 'slit/msvb_m',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    # currently unused
    #msvb_c = device('nicos.devices.tango.Sensor',
    #    tangodevice = tango_base + 'mono/msvb_c',
    #    fmtstr = '%.2f',
    #    lowlevel = True,
    #),
    msvb = device('nicos.devices.generic.Axis',
        description = 'monochromator slit bottom',
        motor = 'msvb_m',
        coder = 'msvb_m',
        fmtstr = '%.2f',
        precision = 0.01,
        lowlevel = True,
    ),

    msvt_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base + 'slit/msvt_m',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    # currently unused
    #msvt_c = device('nicos.devices.tango.Sensor',
    #    tangodevice = tango_base + 'mono/msvt_c',
    #    fmtstr = '%.2f',
    #    lowlevel = True,
    #),
    msvt = device('nicos.devices.generic.Axis',
        description = 'monochromator slit top',
        motor = 'msvt_m',
        coder = 'msvt_m',
        fmtstr = '%.2f',
        precision = 0.01,
        lowlevel = True,
    ),

    ms = device('nicos.devices.generic.Slit',
        description = 'slit before monochromator',
        left = 'mshl',
        right = 'mshr',
        bottom = 'msvb',
        top = 'msvt',
        opmode = 'offcentered',
        coordinates = 'opposite',
    ),
)
