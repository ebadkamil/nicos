description = 'PUMA Eulerian cradle with IPC motorbus'
group = 'optional'

includes = ['base']
excludes = ['mono1']

devices = dict(
    MonoIPC  = device('devices.vendor.ipc.IPCModBusTaco',
                      tacodevice = 'mira/rs485/mgott',
                      lowlevel = True),

    co_ephi  = device('devices.vendor.ipc.Coder',
                      lowlevel = True,
                      bus = 'MonoIPC',
                      addr = 68,
                      zerosteps = 9059075,
                      slope = -4096,
                      circular = -360,
                      unit = 'deg'),
    mo_ephi  = device('devices.vendor.ipc.Motor',
                      lowlevel = True,
                      bus = 'MonoIPC',
                      addr = 58,
                      zerosteps = 500000,
                      slope = 200.0,
                      abslimits = (-180.0, 180.0),
                      unit = 'deg'),
    ephi     = device('devices.generic.Axis',
                      motor = 'mo_ephi',
                      coder = 'co_ephi',
                      obs = [],
                      fmtstr = '%.3f',
                      precision = 0.01),

    co_echi  = device('devices.vendor.ipc.Coder',
                      lowlevel = True,
                      bus = 'MonoIPC',
                      addr = 65,
                      zerosteps = 5334445,
                      slope = -8192.5,
                      unit = 'deg'),
    mo_echi  = device('devices.vendor.ipc.Motor',
                      lowlevel = True,
                      bus = 'MonoIPC',
                      addr = 49,
                      zerosteps = 500000,
                      slope = 200.0,
                      abslimits = (-355.0, 355.0),
                      unit = 'deg'),
    echi     = device('devices.generic.Axis',
                      motor = 'mo_echi',
                      coder = 'co_echi',
                      obs = [],
                      fmtstr = '%.3f',
                      precision = 0.01,
                      offset = -189.99926762282576),

    ec       = device('devices.tas.EulerianCradle',
                      tas = 'mira',
                      chi = 'echi',
                      omega = 'ephi',
                      cell = 'Sample'),
)

