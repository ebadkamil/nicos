description = 'system setup'

group = 'lowlevel'

sysconfig = dict(
    cache='localhost',
    instrument=None,
    experiment='Exp',
    datasinks=['conssink', 'filesink', 'daemonsink', 'jbi_liveview', ],
)

modules = ['nicos.commands.standard', 'nicos_ess.commands.epics', 'nicos_ess.ymir.commands.file_writer']

devices = dict(
    Skeleton=device('nicos.devices.instrument.Instrument',
                    description='instrument object',
                    instrument='ymir',
                    responsible='M. Clarke <matt.clarke@ess.eu>',
                    ),

    Sample=device('nicos.devices.sample.Sample',
                  description='The currently used sample',
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
               description='The just-bin-it histogrammer', hist_topic='nicos1',
               data_topic='event_data', brokers=['172.30.242.20:9092'],
               unit='evts', command_topic='hist_commands',
               response_topic='hist_responses'),

    jbi_liveview=device('nicos.devices.datasinks.LiveViewSink', ),

    FileWriter=device(
        'nicos_ess.devices.datasinks.file_writer.FileWriterStatus',
        description='Status for file-writer',
        broker=['192.168.0.36:9092'],
        statustopic='UTGARD_writerCommandStatus',
        unit='',
    ),

    FileWriterParameters=device(
        'nicos_ess.devices.datasinks.file_writer.FileWriterParameters',
        description='File-writer parameters',
        broker=['192.168.0.36:9092'],
        command_topic='UTGARD_writerCommandStatus',
        nexus_config_path='nicos_ess/ymir/commands/nexus_config.json',
        lowlevel=True,
    ),

)

startupcode = '''
SetDetectors(det)
'''
