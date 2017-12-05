description = 'STRESS-SPEC setup with robot'

group = 'basic'

includes = ['aliases', 'aliases_chiphi', 'system', 'mux', 'monochromator',
            'detector', 'primaryslit', 'slits', 'reactor']

excludes = ['stressi']

modules = ['nicos.commands.standard', 'nicos_mlz.stressi.commands']

sysconfig = dict(
    datasinks = ['caresssink'],
)

nameservice = 'stressictrl.stressi.frm2'

caresspath = '/opt/caress'
toolpath = '/opt/caress'

devices = dict(
    dummyO = device('nicos.devices.vendor.caress.EKFMotor',
                    description = 'OMGS feedback device for the robot',
                    fmtstr = '%.2f',
                    unit = 'deg',
                    coderoffset = -1229.1539993286133,
                    abslimits = (0, 140),
                    nameserver = '%s' % (nameservice,),
                    objname = 'VME',
                    config = 'DUMMYO 114 11 0x00f1c000 1 4096 500 50 2 24 50 '
                             '-1 10 1 5000 1 10 0 0 0',
                    lowlevel = True,
                   ),
    dummyT = device('nicos.devices.vendor.caress.EKFMotor',
                    description = 'TTHS feedback device for the robot',
                    fmtstr = '%.2f',
                    unit = 'deg',
                    coderoffset = 1244.04814453125,
                    abslimits = (0, 140),
                    nameserver = '%s' % (nameservice,),
                    objname = 'VME',
                    config = 'DUMMYT 114 11 0x00f1c000 3 4096 500 5  2 24 50 '
                             '1 10 1 3000 1 30 0 0 0',
                    lowlevel = True,
                   ),
    # *** Roboter Kath ***
    robx = device('nicos.devices.generic.Axis',
                  description = 'Robot X Axis',
                  motor = device('nicos_mlz.stressi.devices.robot.RobotMotor',
                                 fmtstr = '%.2f',
                                 unit = 'mm',
                                 config = 'ROBX 500 RoboterX.Caress_Object',
                                 coderoffset = 0,
                                 nameserver = '%s' % (nameservice,),
                                 abslimits = (-9999., 9999.),
                                 absdev = False,
                                 speedmotor = 'robsl',
                                ),
                  precision = 0.1,
                  maxtries = 10,
                  lowlevel = True,
                 ),
    roby = device('nicos.devices.generic.Axis',
                  description = 'Robot Y Axis',
                  motor = device('nicos_mlz.stressi.devices.robot.RobotMotor',
                                 fmtstr = '%.2f',
                                 unit = 'mm',
                                 config = 'ROBY 500 RoboterY.Caress_Object',
                                 coderoffset = 0,
                                 nameserver = '%s' % (nameservice,),
                                 abslimits = (-9999., 9999.),
                                 absdev = False,
                                 speedmotor = 'robsl',
                                ),
                  precision = 0.1,
                  maxtries = 10,
                  lowlevel = True,
                 ),
    robz = device('nicos.devices.generic.Axis',
                  description = 'Robot Z Axis',
                  motor = device('nicos_mlz.stressi.devices.robot.RobotMotor',
                                 fmtstr = '%.2f',
                                 unit = 'mm',
                                 config = 'ROBZ 500 RoboterZ.Caress_Object',
                                 coderoffset = 0,
                                 nameserver = '%s' % (nameservice,),
                                 abslimits = (-9999., 9999.),
                                 absdev = False,
                                 speedmotor = 'robsl',
                                ),
                  precision = 0.1,
                  maxtries = 10,
                  lowlevel = True,
                 ),
    roba = device('nicos.devices.generic.Axis',
                  description = 'Robot A Axis',
                  motor = device('nicos_mlz.stressi.devices.robot.RobotMotor',
                                 fmtstr = '%.2f',
                                 unit = 'deg',
                                 config = 'ROBA 500 RoboterA.Caress_Object',
                                 coderoffset = 0,
                                 nameserver = '%s' % (nameservice,),
                                 abslimits = (-180, 180),
                                 absdev = False,
                                 speedmotor = 'robsr',
                                ),
                  precision = 0.1,
                  maxtries = 10,
                  lowlevel = True,
                 ),
    robb = device('nicos.devices.generic.Axis',
                  description = 'Robot B Axis',
                  motor = device('nicos_mlz.stressi.devices.robot.RobotMotor',
                                 fmtstr = '%.2f',
                                 unit = 'deg',
                                 config = 'ROBB 500 RoboterB.Caress_Object',
                                 coderoffset = 0,
                                 nameserver = '%s' % (nameservice,),
                                 abslimits = (-360, 360),
                                 absdev = False,
                                 speedmotor = 'robsr',
                                ),
                  precision = 0.1,
                  maxtries = 10,
                 ),
    robc = device('nicos.devices.generic.Axis',
                  description = 'Robot C Axis',
                  motor = device('nicos_mlz.stressi.devices.robot.RobotMotor',
                                 fmtstr = '%.2f',
                                 unit = 'deg',
                                 config = 'ROBC 500 RoboterC.Caress_Object',
                                 coderoffset = 0,
                                 nameserver = '%s' % (nameservice,),
                                 abslimits = (-720, 720),
                                 absdev = False,
                                 lowlevel = True,
                                 speedmotor = 'robsr',
                                ),
                  precision = 0.1,
                  maxtries = 10,
                  lowlevel = True,
                 ),

    # *** Roboter Joint ***
    robj1 = device('nicos.devices.generic.Axis',
                   description = 'Robot J1 Axis',
                   motor = device('nicos_mlz.stressi.devices.robot.RobotMotor',
                                  fmtstr = '%.2f',
                                  unit = 'deg',
                                  config = 'ROBJ1 500 RoboterJ1.Caress_Object',
                                  coderoffset = 0,
                                  nameserver = '%s' % (nameservice,),
                                  abslimits = (-160, 160),
                                  absdev = False,
                                  speedmotor = 'robsj',
                                 ),
                   precision = 0.1,
                   maxtries = 10,
                  ),
    robj2 = device('nicos.devices.generic.Axis',
                   description = 'Robot J2 Axis',
                   motor = device('nicos_mlz.stressi.devices.robot.RobotMotor',
                                  fmtstr = '%.2f',
                                  unit = 'deg',
                                  config = 'ROBJ2 500 RoboterJ2.Caress_Object',
                                  coderoffset = 0,
                                  nameserver = '%s' % (nameservice,),
                                  abslimits = (-137.5, 137.5),
                                  absdev = False,
                                  speedmotor = 'robsj',
                                 ),
                   precision = 0.1,
                   maxtries = 10,
                  ),
    robj3 = device('nicos.devices.generic.Axis',
                   description = 'Robot J2 Axis',
                   motor = device('nicos_mlz.stressi.devices.robot.RobotMotor',
                                  fmtstr = '%.2f',
                                  unit = 'deg',
                                  config = 'ROBJ3 500 RoboterJ3.Caress_Object',
                                  coderoffset = 0,
                                  nameserver = '%s' % (nameservice,),
                                  abslimits = (-150, 150),
                                  absdev = False,
                                  speedmotor = 'robsj',
                                 ),
                   precision = 0.1,
                   maxtries = 10,
                  ),
    robj4 = device('nicos_mlz.stressi.devices.robot.RobotMotor',
                   description = 'Robot J4',
                   fmtstr = '%.2f',
                   unit = 'deg',
                   config = 'ROBJ4 500 RoboterJ4.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (-270, 270),
                   absdev = False,
                   speedmotor = 'robsj',
                  ),
    robj5 = device('nicos_mlz.stressi.devices.robot.RobotMotor',
                   description = 'Robot J5',
                   fmtstr = '%.2f',
                   unit = 'deg',
                   config = 'ROBJ5 500 RoboterJ5.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (-105, 120),
                   absdev = False,
                   speedmotor = 'robsj',
                  ),
    robj6 = device('nicos_mlz.stressi.devices.robot.RobotMotor',
                   description = 'Robot J6',
                   fmtstr = '%.2f',
                   unit = 'deg',
                   config = 'ROBJ6 500 RoboterJ6.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (-15000, 15000),
                   absdev = False,
                   speedmotor = 'robsj',
                  ),
    # *** Roboter Tool Number ***
    robt = device('nicos.devices.vendor.caress.Motor',
                  description = 'Robot T (tool number)',
                  fmtstr = '%d',
                  unit = '',
                  config = 'ROBT 500 RoboterToolNumber.Caress_Object',
                  coderoffset = 0,
                  nameserver = '%s' % (nameservice,),
                  abslimits = (0, 1000),
                  absdev = False,
                 ),
    robs = device('nicos.devices.vendor.caress.Motor',
                  description = 'Robot S (sample number)',
                  fmtstr = '%d',
                  unit = '',
                  config = 'ROBS 500 RoboterSampleNumber.Caress_Object',
                  coderoffset = 0,
                  nameserver = '%s' % (nameservice,),
                  abslimits = (0, 100),
                  absdev = False,
                 ),
    robsj = device('nicos.devices.vendor.caress.Motor',
                   description = 'Robot SJ (% of maximum speed)',
                   fmtstr = '%.2f',
                   unit = '%',
                   config = 'ROBSJ 500 RoboterSpeedJoint.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (0, 20),
                   absdev = False,
                   lowlevel = True,
                  ),
    robsl = device('nicos.devices.vendor.caress.Motor',
                   description = 'Robot SL (linear speed)',
                   fmtstr = '%.2f',
                   unit = 'mm/s',
                   config = 'ROBSL 500 RoboterSpeedLinear.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (0, 1000),
                   absdev = False,
                   lowlevel = True,
                  ),
    robsr = device('nicos.devices.vendor.caress.Motor',
                   description = 'Robot SR (rotation speed)',
                   fmtstr = '%.2f',
                   unit = 'deg/s',
                   config = 'ROBSR 500 RoboterSpeedRotation.Caress_Object',
                   coderoffset = 0,
                   nameserver = '%s' % (nameservice,),
                   abslimits = (0, 1000),
                   absdev = False,
                   lowlevel = True,
                  ),
    # *** Roboter Standard Values ***
    omgs_r = device('nicos.devices.vendor.caress.Motor',
                    description = 'Robot OMGS',
                    fmtstr = '%.2f',
                    unit = 'deg',
                    nameserver = '%s' % (nameservice,),
                    coderoffset = 0.,
                    abslimits = (0, 140),
                    config = 'OMGR 500 OMGR.Caress_Object',
                    absdev = False,
                    lowlevel = True,
                   ),
    tths_r = device('nicos.devices.vendor.caress.Motor',
                    description = 'Robot TTHS',
                    fmtstr = '%.2f',
                    unit = 'deg',
                    nameserver = '%s' % (nameservice,),
                    config = 'TTHR 500 TTHR.Caress_Object',
                    coderoffset = 0.,
                    abslimits = (0, 140),
                    absdev = False,
                    lowlevel = True,
                   ),
    roba_t = device('nicos_mlz.stressi.devices.wavelength.TransformedMoveable',
                    description = 'Transformed roba device',
                    dev = 'roba',
                    informula = '180. - x',
                    outformula = '180. - x',
                    precision = 0.001,
                    lowlevel = True,
                   ),
)

alias_config = {
    'tths': {'dummyT': 200, 'tths_r': 100,},
    'omgs': {'dummyO': 200, 'omgs_r': 100,},
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
