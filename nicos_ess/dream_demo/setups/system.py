description = 'system setup'

group = 'lowlevel'

sysconfig = dict(
    cache='localhost',
    instrument='DREAM',
    experiment='Exp',
    datasinks=['conssink', 'filesink', 'daemonsink', 'liveview'],
)

modules = ['nicos.commands.standard', 'nicos_ess.commands.epics']

devices = dict(
    DREAM=device('nicos.devices.instrument.Instrument',
        description='instrument object',
        instrument='DREAM',
        responsible='Ebad Kamil <ebad.kamil@ess.eu>',
    ),

    Sample=device('nicos.devices.sample.Sample',
        description='The currently used sample',
    ),

    Exp=device('nicos.devices.experiment.Experiment',
        description='experiment object',
        dataroot='/opt/nicos-data',
        sendmail=False,
        serviceexp='p0',
        sample='Sample',
    ),

    filesink=device('nicos.devices.datasinks.AsciiScanfileSink',),

    conssink=device('nicos.devices.datasinks.ConsoleScanSink',),

    daemonsink=device('nicos.devices.datasinks.DaemonSink',),
    liveview=device('nicos.devices.datasinks.LiveViewSink', ),

    Space=device('nicos.devices.generic.FreeSpace',
        description='The amount of free space for storing data',
        path=None,
        minfree=5,
    ),

    KafkaForwarderStatus=device(
        'nicos_ess.devices.forwarder.EpicsKafkaForwarder',
        description='Monitors the status of the Forwarder',
        statustopic="status_topic",
        forwarder_control="KafkaForwarderControl",
        brokers=["localhost"],
    ),

    KafkaForwarderControl=device(
        'nicos_ess.devices.forwarder.EpicsKafkaForwarderControl',
        description='Controls the Forwarder',
        cmdtopic="TEST_forwarderConfig",
        instpvtopic="pv_topic",
        brokers=["localhost"],
    ),
)

startupcode = '''
'''
