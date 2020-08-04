#  -*- coding: utf-8 -*-

description = 'system setup for PUMA'

group = 'lowlevel'

sysconfig = dict(
    cache = 'pumahw.puma.frm2',
    instrument = 'puma',
    experiment = 'Exp',
    datasinks = ['conssink', 'filesink', 'daemonsink'],
    notifiers = ['email'],
)

modules = ['nicos.commands.standard']

includes = ['notifiers']

devices = dict(
    puma = device('nicos.devices.instrument.Instrument',
        description = 'DAS PUMA',
        instrument = 'PUMA',
        responsible = 'J. T. Park <jitae.park@frm2.tum.de>',
        doi = 'http://dx.doi.org/10.17815/jlsrf-1-36',
        website = 'http://www.mlz-garching.de/puma',
        operators = [
            u'Technische Universität München (TUM)',
            u'Institut für Physikalische Chemie, Georg-August-Universität '
            u'Göttingen',
        ],
    ),
    Exp = device('nicos_mlz.panda.devices.experiment.PandaExperiment',
        description = 'Experiment of PUMA',
        sample = 'Sample',
        dataroot = '/data',
        propdb = '/pumacontrol/propdb',
        managerights = dict(
            enableDirMode = 0o775,
            enableFileMode = 0o664,
            disableDirMode = 0o700,
            disableFileMode = 0o600,
            owner = 'nicd',
            group = 'puma'
        ),
        sendmail = True,
        zipdata = True,
        mailserver = 'mailhost.frm2.tum.de',
        mailsender = 'puma@frm2.tum.de',
        serviceexp = 'service',
    ),
    Sample = device('nicos.devices.tas.TASSample',
        description = 'Currently used sample',
    ),
    filesink = device('nicos.devices.datasinks.AsciiScanfileSink',
        description = 'metadevice storing the scanfiles',
        filenametemplate = [
            '%(proposal)s_%(scancounter)08d.dat',
            '/%(year)d/cycle_%(cycle)s/%(proposal)s_%(scancounter)08d.dat'
        ],
    ),
    conssink = device('nicos.devices.datasinks.ConsoleScanSink',
        description = 'handles console output',
    ),
    daemonsink = device('nicos.devices.datasinks.DaemonSink',
        description = 'handles I/O inside daemon',
    ),
    LogSpace = device('nicos.devices.generic.FreeSpace',
        description = 'Free space on the log drive',
        path = '/pumacontrol/log',
        lowlevel = True,
        warnlimits = (0.5, None),
    ),
)
