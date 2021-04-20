description = 'The motion stages for alignment in the YMIR cave'

devices = dict(
    mX=device(
        'nicos_ess.devices.epics.pva.EpicsMotor',
        epicstimeout=3.0,
        precision=0.1,
        description='Single axis positioner',
        motorpv='SES-SCAN:MC-MCU-001:m1',
        errormsgpv='SES-SCAN:MC-MCU-001:m1-MsgTxt',
        errorbitpv='SES-SCAN:MC-MCU-001:m1-Err',
        reseterrorpv='SES-SCAN:MC-MCU-001:m1-ErrRst',
        error_severity_pv='SES-SCAN:MC-MCU-001:m1.SEVR',
        error_status_pv='SES-SCAN:MC-MCU-001:m1.STAT',
    ),
    mY=device(
        'nicos_ess.devices.epics.pva.EpicsMotor',
        epicstimeout=3.0,
        precision=0.1,
        description='Single axis positioner',
        motorpv='SES-SCAN:MC-MCU-001:m2',
        errormsgpv='SES-SCAN:MC-MCU-001:m2-MsgTxt',
        errorbitpv='SES-SCAN:MC-MCU-001:m2-Err',
        reseterrorpv='SES-SCAN:MC-MCU-001:m2-ErrRst',
        error_severity_pv='SES-SCAN:MC-MCU-001:m2.SEVR',
        error_status_pv='SES-SCAN:MC-MCU-001:m2.STAT',
    ),
    mZ=device(
        'nicos_ess.devices.epics.pva.EpicsMotor',
        epicstimeout=3.0,
        precision=0.1,
        description='Single axis positioner',
        motorpv='SES-SCAN:MC-MCU-001:m3',
        errormsgpv='SES-SCAN:MC-MCU-001:m3-MsgTxt',
        errorbitpv='SES-SCAN:MC-MCU-001:m3-Err',
        reseterrorpv='SES-SCAN:MC-MCU-001:m3-ErrRst',
        error_severity_pv='SES-SCAN:MC-MCU-001:m3.SEVR',
        error_status_pv='SES-SCAN:MC-MCU-001:m3.STAT',
    ),
)
