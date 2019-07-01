description = 'system setup'

group = 'lowlevel'

sysconfig = dict(
    cache='localhost',
    instrument=None,
    experiment='Exp',
    datasinks=['conssink', 'filesink', 'daemonsink', 'jbi_liveview'],
)

modules = ['nicos.commands.standard', 'nicos_ess.commands.epics']

devices = dict(
    Skeleton=device('nicos.devices.instrument.Instrument',
                    description='instrument object',
                    instrument='essiip',
                    responsible='M. Wedel <michael.wedel@esss.se>',
                    ),

    Sample=device('nicos.devices.sample.Sample',
                  description='The current used sample',
                  ),

    Exp=device('nicos.devices.experiment.Experiment',
               description='experiment object',
               dataroot='/opt/nicos-data',
               sendmail=True,
               serviceexp='p0',
               sample='Sample',
               ),

    filesink=device('nicos.devices.datasinks.AsciiScanfileSink',
                    ),

    conssink=device('nicos.devices.datasinks.ConsoleScanSink',
                    ),

    daemonsink=device('nicos.devices.datasinks.DaemonSink',
                      ),

    Space=device('nicos.devices.generic.FreeSpace',
                 description='The amount of free space for storing data',
                 path=None,
                 minfree=5,
                 ),

    det=device('nicos_ess.devices.datasources.just_bin_it.JustBinItDetector',
               description="The just-bin-it histogrammer", hist_topic="nicos1",
               data_topic="LOQ_events", brokers=["172.30.242.20:9092"], unit="evts",
               command_topic="hist_commands"),

    jbi_liveview=device('nicos.devices.datasinks.LiveViewSink',
                        ),
)

startupcode = "SetDetectors(det)"