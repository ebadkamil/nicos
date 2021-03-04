description = 'JustBinIt histogrammer.'

devices = dict(
    det=device('nicos_ess.devices.datasources.just_bin_it.JustBinItDetector',
               description='Just Bin it histogrammer',
               hist_topic='hist_topic', data_topic='fake_events',
               brokers=['localhost:9092'], unit='evts',
               command_topic='hist_commands', response_topic='output_topic',
               hist_type='2-D TOF'),
)

startupcode = '''
SetDetectors(det)
'''