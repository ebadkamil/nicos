# description: Description of the setup (detailed)
description = 'system setup'

# group: Group of the setup. The following groups are recognized:
# - basic
#       Basic setup for the instrument, of which only one should be
#       loaded (e.g. "twoaxis" or "threeaxis"). These setups can be
#       presented to the user.
# - optional
#       Optional setup, of which as many as needed can be loaded.
#       These setups can be presented to the user for multiple
#       selection. This is the default.
# - lowlevel
#       Low-level setup, which will be included by others, but should
#       not be presented to users.
# - special
#       The setup is not a setup of instrument devices, but configures
#       e.g. a NICOS service. For each service, there is one special
#       setup (e.g. "cache", "poller", "daemon").
group = 'lowlevel'

# sysconfig: A dictionary with basic system configuration values.
# Possible values:
#   - cache
#       A string giving the hostname[:port] of the cache server,
#       the default port is 14869.
#       If this value is omitted, no caching will be available.
#   - instrument
#       The name of the instrument device, defined somewhere in a
#       devices dictionary. The class for this device must be
#       nicos.devices.instrument.Instrument or an instrument-specific
#       subclass.
#   - experiment
#       The name of the experiment "device", defined somewhere in a
#       devices dictionary. The class for this device must be
#       nicos.devices.experiment.Experiment or an instrument-specific
#       subclass.
#   - datasinks
#       A list of names of "data sinks", i.e. special devices that
#       process measured data. These devices must be defined somewhere
#       in a devices dictionary and be of class
#       nicos.devices.datasinks.DataSink or a subclass.
#   - notifiers
#       A list of names of "notifiers", i.e. special devices that can
#       notify the user or instrument responsibles via various channels
#       (e.g. email). These devices must be defined somewhere in a
#       devices dictionary and be of class
#       nicos.devices.notifiers.Notifier or a subclass.

sysconfig = dict(
    cache='localhost',
    instrument='Amor',
    experiment='Exp',
    datasinks=['conssink', 'dmnsink', 'NexusDataSink', 'HistogramDataSink'],
)

modules = ['nicos.commands.standard', 'nicos_ess.commands.file_writing',
           'nicos_sinq.amor.commands', 'nicos_sinq.commands.sics']

includes = ['laser']

# devices: Contains all device definitions.
# A device definition consists of a call like device(classname, parameters).
# The class name is fully qualified (i.e., includes the package/module name).
# The parameters are given as keyword arguments.
devices = dict(
    Amor=device('nicos.devices.instrument.Instrument',
                description='instrument object',
                instrument='SINQ AMOR',
                responsible='Jochen Stahn <jochen.stahn@psi.ch>',
                operators=['Paul-Scherrer-Institut (PSI)'],
                facility='SINQ, PSI',
                website='https://www.psi.ch/sinq/amor/amor'
                ),

    Sample=device('nicos.devices.sample.Sample',
                  description='The current used sample',
                  ),

    # Configure dataroot here (usually /data).
    Exp=device('nicos_sinq.amor.devices.experiment.AmorExperiment',
               description='experiment object',
               dataroot='/home/amor/',
               sample='Sample'
               ),

    Space=device('nicos.devices.generic.FreeSpace',
                 description='The amount of free space for storing data',
                 path=None,
                 minfree=5,
                 ),

    Shutter=device('nicos_sinq.amor.devices.sps_switch.AmorShutter',
                   description='Shutter controlled by SPS',
                   epicstimeout=3.0,
                   readpv='SQ:AMOR:SPS1:DigitalInput',
                   commandpv='SQ:AMOR:SPS1:Push',
                   commandstr="S0000",
                   byte=4,
                   bit=0,
                   brokenbyte=4,
                   brokenbit=3,
                   mapping={'CLOSED': False, 'OPEN': True}),

    SpinFlipper=device('nicos_sinq.amor.devices.sps_switch.SpsSwitch',
                       description='Spin flipper RF controlled by SPS',
                       epicstimeout=3.0,
                       readpv='SQ:AMOR:SPS1:DigitalInput',
                       commandpv='SQ:AMOR:SPS1:Push',
                       commandstr="S0007",
                       byte=12,
                       bit=7,
                       mapping={'SPIN DOWN': False,
                                'SPIN UP': True}),

    KafkaForwarder=device(
        'nicos_ess.devices.forwarder.EpicsKafkaForwarder',
        description="Configures commands to forward-epics-to-kafka",
        cmdtopic="AMOR_forwarderCommands",
        statustopic="AMOR_forwarderStatus",
        instpvtopic="AMOR_metadata",
        instpvschema='f142',
        brokers=configdata('special/config.KAFKA_BROKERS'),
    ),

    conssink=device('nicos.devices.datasinks.ConsoleScanSink'),

    dmnsink=device('nicos.devices.datasinks.DaemonSink'),

    NexusDataSink=device(
        'nicos_sinq.devices.datasinks.SinqNexusFileSink',
        description="Sink for NeXus file writer (kafka-to-nexus)",
        brokers=configdata('special/config.KAFKA_BROKERS'),
        filenametemplate=['amor%(year)sn%(pointcounter)06d.hdf'],
        cmdtopic="AMOR_filewriterCommands",
        status_provider='NexusFileWriter',
        templatesmodule='nicos_sinq.amor.nexus.nexus_templates',
        templatename='amor_default'
    ),

    HistogramDataSink=device(
        'nicos_sinq.amor.devices.datasinks.ImageKafkaWithLiveViewDataSink',
        brokers=configdata('special/config.KAFKA_BROKERS'),
        channeltostream={
            'area_detector': ('AMOR_areaDetector', 'area.tof'),
            'single_det1': ('AMOR_singleDetector1', 'single.tof'),
            'single_det2': ('AMOR_singleDetector2', 'single.tof'),
        },
    ),

    NexusFileWriter=device(
        'nicos_ess.devices.datasinks.nexussink.NexusFileWriterStatus',
        description="Status for nexus file writing",
        brokers=configdata('special/config.KAFKA_BROKERS'),
        statustopic="AMOR_filewriterStatus",
        timeout=30,
    ),

    Distances = device(
        'nicos_sinq.amor.devices.component_handler.DistancesHandler',
        description='Device to handle distance calculation in AMOR',
        components={
            'polariser': (-232, 0),
            'slit2': (302, 0),
            'slit3': (-22, 0),
            'slit4': (306, 0),
            'sample': (-310, 0),
            'detector': (326, 0),
            'selene': (-726, 0),
            'analyser': (310, 0)
        },
        fixedcomponents={
            'chopper': 9906,
            'filter': 8609,
            'slit1': 9010,
        },
        order=['chopper', 'slit1', 'filter', 'polariser', 'slit2', 'selene',
               'slit3', 'sample', 'slit4', 'analyser', 'detector'],
        switch='laser_switch',
        positioner='laser_positioner',
        dimetix='dimetix'
    )
)
