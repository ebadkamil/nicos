description = 'STRESS-SPEC setup with robot'

group = 'basic'

includes = ['aliases', 'system', 'mux', 'monochromator', 'detector',
            'primaryslit', 'slits', 'reactor']

excludes = ['stressi']

modules = ['commands.standard', 'stressi.commands']

sysconfig = dict(
    datasinks = ['caresssink'],
)

servername = 'STRESSICTRL'

nameservice = 'stressictrl'

caresspath = '/opt/caress'
toolpath = '/opt/caress'

devices = dict(
    dummyO = device('devices.vendor.caress.Motor',
                    description = 'Feedback device for the robotor',
                    fmtstr = '%.2f',
                    unit = 'deg',
                    coderoffset = 0,
                    abslimits = (0, 0),
                    nameserver = '%s' % (nameservice,),
                    objname = 'VME',
                    config = 'DUMMYO 114 11 0x00f1c000 1 4096 500 50 2 24 50 '
                             '-1 10 1 5000 1 10 0 0 0',
                    lowlevel = True,
                    pollinterval = None,
                   ),
    dummyT = device('devices.vendor.caress.Motor',
                    description = 'Feedback device for the robotor',
                    fmtstr = '%.2f',
                    unit = 'deg',
                    coderoffset = 0,
                    abslimits = (0, 0),
                    nameserver = '%s' % (nameservice,),
                    objname = 'VME',
                    config = 'DUMMYT 114 11 0x00f1c000 3 4096 500 5  2 24 50 '
                             '1 10 1 3000 1 30 0 0 0',
                    lowlevel = True,
                    pollinterval = None,
                   ),
    # *** Roboter Kath ***
    robx = device('devices.vendor.caress.Motor',
                  description = 'Robot X',
                  fmtstr = '%.2f',
                  unit = 'mm',
                  config = 'ROBX 500 RoboterX.Caress_Object',
                  coderoffset = 0,
                  nameserver = '%s' % (nameservice,),
                  abslimits = (-9999., 9999.),
                  absdev = False,
                 ),
    roby = device('devices.vendor.caress.Motor',
                  description = 'Robot Y',
                  fmtstr = '%.2f',
                  unit = 'mm',
                  config = 'ROBY 500 RoboterY.Caress_Object',
                  coderoffset = 0,
                  nameserver = '%s' % (nameservice,),
                  abslimits = (-9999., 9999.),
                  absdev = False,
                 ),
    robz = device('devices.vendor.caress.Motor',
                  description = 'Robot Z',
                  fmtstr = '%.2f',
                  unit = 'mm',
                  config = 'ROBZ 500 RoboterZ.Caress_Object',
                  coderoffset = 0,
                  nameserver = '%s' % (nameservice,),
                  abslimits = (-9999., 9999.),
                  absdev = False,
                 ),
    roba = device('devices.vendor.caress.Motor',
                  description = 'Robot A',
                  fmtstr = '%.2f',
                  unit = 'deg',
                  config = 'ROBA 500 RoboterA.Caress_Object',
                  coderoffset = 0,
                  nameserver = '%s' % (nameservice,),
                  abslimits = (-180, 180),
                  absdev = False,
                 ),
    robb = device('devices.vendor.caress.Motor',
                  description = 'Robot B',
                  fmtstr = '%.2f',
                  unit = 'deg',
                  config = 'ROBB 500 RoboterB.Caress_Object',
                  coderoffset = 0,
                  nameserver = '%s' % (nameservice,),
                  abslimits = (-360, 360),
                  absdev = False,
                 ),
    robc = device('devices.vendor.caress.Motor',
                  description = 'Robot C',
                  fmtstr = '%.2f',
                  unit = 'deg',
                  config = 'ROBC 500 RoboterC.Caress_Object',
                  coderoffset = 0,
                  nameserver = '%s' % (nameservice,),
                  abslimits = (-720, 720),
                  absdev = False,
                 ),

    # *** Roboter Joint ***
    robj1 = device('devices.vendor.caress.Motor',
                   description = 'Robot J1',
                   fmtstr = '%.2f',
                   unit = 'deg',
                   config = 'ROBJ1 500 RoboterJ1.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (-160, 160),
                   absdev = False,
                  ),
    robj2 = device('devices.vendor.caress.Motor',
                   description = 'Robot J2',
                   fmtstr = '%.2f',
                   unit = 'deg',
                   config = 'ROBJ2 500 RoboterJ2.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (-137.5, 137.5),
                   absdev = False,
                  ),
    robj3 = device('devices.vendor.caress.Motor',
                   description = 'Robot J3',
                   fmtstr = '%.2f',
                   unit = 'deg',
                   config = 'ROBJ3 500 RoboterJ3.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (-150, 150),
                   absdev = False,
                  ),
    robj4 = device('devices.vendor.caress.Motor',
                   description = 'Robot J4',
                   fmtstr = '%.2f',
                   unit = 'deg',
                   config = 'ROBJ4 500 RoboterJ4.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (-270, 270),
                   absdev = False,
                  ),
    robj5 = device('devices.vendor.caress.Motor',
                   description = 'Robot J5',
                   fmtstr = '%.2f',
                   unit = 'deg',
                   config = 'ROBJ5 500 RoboterJ5.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (-105, 120),
                   absdev = False,
                  ),
    robj6 = device('devices.vendor.caress.Motor',
                   description = 'Robot J6',
                   fmtstr = '%.2f',
                   unit = 'deg',
                   config = 'ROBJ6 500 RoboterJ6.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (-15000, 15000),
                   absdev = False,
                  ),
    # *** Roboter Tool Number ***
    robt = device('devices.vendor.caress.Motor',
                  description = 'Robot T (tool number)',
                  fmtstr = '%.2f',
                  unit = '',
                  config = 'ROBT 500 RoboterToolNumber.Caress_Object',
                  coderoffset = 0,
                  nameserver = '%s' % (nameservice,),
                  abslimits = (0, 1000),
                  absdev = False,
                 ),
    robs = device('devices.vendor.caress.Motor',
                  description = 'Robot S (sample number)',
                  fmtstr = '%d',
                  unit = '',
                  config = 'ROBS 500 RoboterSampleNumber.Caress_Object',
                  coderoffset = 0,
                  nameserver = '%s' % (nameservice,),
                  abslimits = (0, 100),
                  absdev = False,
                 ),
    robsj = device('devices.vendor.caress.Motor',
                   description = 'Robot SJ (% of maximum speed)',
                   fmtstr = '%.2f',
                   unit = '%',
                   config = 'ROBSJ 500 RoboterSpeedJoint.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (0, 20),
                   absdev = False,
                  ),
    robsl = device('devices.vendor.caress.Motor',
                   description = 'Robot SL (linear speed)',
                   fmtstr = '%.2f',
                   unit = 'mm/s',
                   config = 'ROBSL 500 RoboterSpeedLinear.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (0, 1000),
                   absdev = False,
                  ),
    robsr = device('devices.vendor.caress.Motor',
                   description = 'Robot SR (rotation speed)',
                   fmtstr = '%.2f',
                   unit = 'deg/s',
                   config = 'ROBSR 500 RoboterSpeedRotation.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (0, 1000),
                   absdev = False,
                  ),
    # *** Roboter Standard Values ***
    omgs_r = device('devices.vendor.caress.Motor',
                    description = 'Robot OMGS',
                    fmtstr = '%.2f',
                    unit = 'deg',
                    nameserver = '%s' % (nameservice,),
                    coderoffset = 0.,
                    abslimits = (0, 140),
                    config = 'OMGR 500 OMGR.Caress_Object',
                    absdev = False,
                   ),
    tths_r = device('devices.vendor.caress.Motor',
                    description = 'Robot TTHS',
                    fmtstr = '%.2f',
                    unit = 'deg',
                    nameserver = '%s' % (nameservice,),
                    config = 'TTHR 500 TTHR.Caress_Object',
                    coderoffset = 0.,
                    abslimits = (0, 140),
                    absdev = False,
                   ),
    roba_t = device('stressi.wavelength.TransformedMoveable',
                    description = 'Transformed roba device',
                    dev = 'roba',
                    informula = '180. - x',
                    outformula = '180. - x',
                    precision = 0.001,
                    # lowlevel = True,
                   ),
)
# TOL TTHR=0.1 OMGR=0.1 CHIR=0.1 PHIR=0.1 XR=0.1 YR=0.1 ZR=0.1
# BLS XR=-2000,2000 BLS YR=-2000,2000 BLS ZR=-2000,2000
# SOF TTHR = 0 OMGR = 0 CHIR = 0 PHIR = 0 XR = 0 YR = 0 ZR = 0 ROBSR = 0
# ROBSL = 0 ROBSJ = 0 ROBT = 0 ROBS = 0

alias_config = {
    'tths': {'tths_r': 200,},
    'omgs': {'omgs_r': 200,},
    'chis': {'roba_t': 200,},
    'phis': {'robc': 200,},
    'xt': {'robx': 200,},
    'yt': {'roby': 200,},
    'zt': {'robz': 200,},
}

# The dummyO and dummyT must be initialized for the CARESS robot service
startupcode = """
CreateDevice('dummyO')
CreateDevice('dummyT')
"""
