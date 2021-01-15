#  -*- coding: utf-8 -*-
description = 'NICOS system setup'

group = 'lowlevel'

sysconfig = dict(
    cache = 'tofhw.toftof.frm2',
    instrument = 'TOFTOF',
    experiment = 'Exp',
    datasinks = [
        'conssink', 'filesink', 'dmnsink', 'livesink', 'tofsink', 'nxsink'
    ],
    notifiers = ['emailer', 'smser'],
)

modules = ['nicos.commands.standard']

includes = ['notifiers']

devices = dict(
    TOFTOF = device('nicos.devices.instrument.Instrument',
        description = 'The famous TOFTOF instrument',
        responsible = 'W. Lohstroh <wiebke.lohstroh@frm2.tum.de>',
        instrument = 'TOFTOF',
        doi = 'http://dx.doi.org/10.17815/jlsrf-1-40',
        website = 'http://www.mlz-garching.de/toftof',
        operators = ['Technische Universität München (TUM)'],
    ),
    Sample = device('nicos.devices.sample.Sample',
        description = 'The currently used sample',
    ),
    Exp = device('nicos_mlz.toftof.devices.experiment.Experiment',
        description = 'The currently running experiment',
        dataroot = '/data',
        sample = 'Sample',
        serviceexp = '0',
        propprefix = '',
        sendmail = True,
        mailsender = 'toftof@frm2.tum.de',
        propdb = '/toftofcontrol/propdb',
        managerights = dict(
            enableDirMode = 0o775,
            enableFileMode = 0o664,
            disableDirMode = 0o550,
            disableFileMode = 0o440,
            owner = 'toftof',
            group = 'toftof',
        ),
        errorbehavior = 'abort',
        elog = True,
        counterfile = 'counter',
    ),
    filesink = device('nicos.devices.datasinks.AsciiScanfileSink'),
    conssink = device('nicos.devices.datasinks.ConsoleScanSink'),
    dmnsink = device('nicos.devices.datasinks.DaemonSink'),
    livesink = device('nicos_mlz.toftof.devices.datasinks.ToftofLiveViewSink'),
    tofsink = device('nicos_mlz.toftof.devices.datasinks.TofImageSink',
        filenametemplate = ['%(pointcounter)08d_0000.raw'],
    ),
    nxsink = device('nicos_mlz.toftof.devices.datasinks.TofNeXuS',
        filenametemplate = ['TOFTOF%(pointcounter)08d.nxs'],
        lowlevel = True,
    ),
    Space = device('nicos.devices.generic.FreeSpace',
        description = 'The amount of free space for storing data',
        path = '/data',
        minfree = 5,
    ),
    LogSpace = device('nicos.devices.generic.FreeSpace',
        description = 'Free space on the log drive',
        path = '/toftofcontrol/log',
        lowlevel = True,
        warnlimits = (0.5, None),
    ),
)
