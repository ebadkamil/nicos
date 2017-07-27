# -*- coding: utf-8 -*-

description = 'system setup'
group = 'lowlevel'
display_order = 80

sysconfig = dict(
    cache = 'localhost',
    instrument = 'KWS1',
    experiment = 'Exp',
    datasinks = ['conssink', 'filesink', 'daemonsink'],
    notifiers = ['email'],
)

includes = ['notifiers']

modules = ['nicos.commands.standard']

devices = dict(
    KWS1     = device('nicos.devices.instrument.Instrument',
                      description = 'KWS-1 instrument',
                      instrument = 'KWS-1',
                      doi = 'http://dx.doi.org/10.17815/jlsrf-1-26',
                      responsible = 'H. Frielinghaus <h.frielinghaus@fz-juelich.de>',
                     ),

    Sample   = device('nicos_mlz.kws1.devices.sample.KWSSample',
                      description = 'Sample object',
                     ),

    Exp      = device('nicos_mlz.frm2.devices.experiment.Experiment',
                      description = 'experiment object',
                      dataroot = '/data',
                      sendmail = True,
                      mailsender = 'kws1@frm2.tum.de',
                      mailserver = 'mailhost.frm2.tum.de',
                      serviceexp = 'maintenance',
                      sample = 'Sample',
                      propdb = '/home/jcns/.nicos_proposaldb',
                      managerights = dict(enableDirMode=0o775,
                                          enableFileMode=0o664,
                                          disableDirMode=0o500,
                                          disableFileMode=0o400,
                                          owner='jcns', group='games'),
                     ),

    filesink = device('nicos.devices.datasinks.AsciiScanfileSink',
                      lowlevel = True,
                     ),

    conssink = device('nicos.devices.datasinks.ConsoleScanSink',
                      lowlevel = True,
                     ),

    daemonsink = device('nicos.devices.datasinks.DaemonSink',
                        lowlevel = True,
                       ),

    Space    = device('nicos.devices.generic.FreeSpace',
                      description = 'The amount of free space for storing data',
                      path = None,
                      minfree = 5,
                     ),
)