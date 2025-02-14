description = 'Selene1 mover motors'

pvprefix = 'PSI-ESTIARND:MC-MCU-01:'

devices = dict(
    mover_fl_re_us = device('nicos_ess.devices.epics.motor.EpicsMotor',
        epicstimeout = 3.0,
        description = 'M1 Selene1 1-Mover FL-RE-US',
        motorpv = f'{pvprefix}m1',
        errormsgpv = f'{pvprefix}m1-MsgTxt',
        errorbitpv = f'{pvprefix}m1-Err',
        reseterrorpv = f'{pvprefix}m1-ErrRst',
        unit = 'degree',
    ),
    mover_pr_re_ds = device('nicos_ess.devices.epics.motor.EpicsMotor',
        epicstimeout = 3.0,
        description = 'M2 Selene1 1-Mover PR-RE-DS',
        motorpv = f'{pvprefix}m2',
        errormsgpv = f'{pvprefix}m2-MsgTxt',
        errorbitpv = f'{pvprefix}m2-Err',
        reseterrorpv = f'{pvprefix}m2-ErrRst',
        unit = 'degree',
    ),
    mover_pr_li_ds = device('nicos_ess.devices.epics.motor.EpicsMotor',
        epicstimeout = 3.0,
        description = 'M3 Selene1 1-Mover PR-LI-DS',
        motorpv = f'{pvprefix}m3',
        errormsgpv = f'{pvprefix}m3-MsgTxt',
        errorbitpv = f'{pvprefix}m3-Err',
        reseterrorpv = f'{pvprefix}m3-ErrRst',
        unit = 'degree',
    ),
    mover_pr_li_us1 = device('nicos_ess.devices.epics.motor.EpicsMotor',
        epicstimeout = 3.0,
        description = 'M4 Selene1 2-Mover PR-LI-US-1',
        motorpv = f'{pvprefix}m4',
        errormsgpv = f'{pvprefix}m4-MsgTxt',
        errorbitpv = f'{pvprefix}m4-Err',
        reseterrorpv = f'{pvprefix}m4-ErrRst',
        unit = 'degree',
    ),
    mover_pr_li_us2 = device('nicos_ess.devices.epics.motor.EpicsMotor',
        epicstimeout = 3.0,
        description = 'M5 Selene1 2-Mover PR-LI-US-2',
        motorpv = f'{pvprefix}m5',
        errormsgpv = f'{pvprefix}m5-MsgTxt',
        errorbitpv = f'{pvprefix}m5-Err',
        reseterrorpv = f'{pvprefix}m5-ErrRst',
        unit = 'degree',
    ),
)
