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
#        The setup is not a setup of instrument devices, but configures
#        e.g. a NICOS service. For each service, there is one special
#        setup (e.g. "cache", "poller", "daemon").
group = 'lowlevel'

# sysconfig: A dictionary with basic system configuration values.
# Possible values:
#   - cache
#       A string giving the hostname of the cache server (or
#       hostname:port, if the cache runs on a port other than 14869).
#       If this is omitted, no caching will be available.
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
    cache = 'localhost',
    instrument = 'biodiff',
    experiment = 'Exp',
    datasinks = ['conssink', 'filesink', 'daemonsink'],
    notifiers = ['mailer', 'smser'],
)

modules = ['nicos.commands.standard', 'biodiff.scan']

# devices: Contains all device definitions.
# A device definition consists of a call like device(classname, parameters).
# The class name is fully qualified (i.e., includes the package/module name).
# The parameters are given as keyword arguments.
devices = dict(
    Sample   = device('devices.sample.Sample',
                      description = 'Sample under investigation'),

    # Configure dataroot here (usually /data).
    Exp      = device('devices.experiment.Experiment',
                      description = 'Experiment device',
                      dataroot = '~/data',
                      managerights = dict( enableDirMode=0775,
                                           enableFileMode=0644,
                                           disableDirMode=0700,
                                           disableFileMode=0400 ),
                      localcontact = "Tobias Schrader <t.schrader@fz-juelich.de>",
                      sendmail = False,
                      zipdata = False,
                      serviceexp = 'service',
                      sample = 'Sample',
                     ),

    biodiff = device('devices.instrument.Instrument',
                     description = 'Single crystal DIFFractometer '
                                   'for BIOlogical macromolecules',
                     instrument = "BIODIFF",
                     responsible = "Tobias Schrader <t.schrader@fz-juelich.de>",
                    ),

    filesink = device('devices.datasinks.AsciiDatafileSink',
                      description = 'Device storing scanfiles in Ascii output format.',
                     ),

    conssink = device('devices.datasinks.ConsoleSink',
                      description = 'Device storing console output.',
                     ),

    daemonsink = device('devices.datasinks.DaemonSink',
                        description = 'Device storing deamon output.',
                       ),

    Space    = device('devices.generic.FreeSpace',
                      description = 'The amount of free space for storing data',
                      path = None,
                      minfree = 5,
                     ),

    # Configure source and copy addresses to an existing address.
    mailer    = device('devices.notifiers.Mailer',
                       description = 'E-Mail notifier',
                       sender = 'biodiff@frm2.tum.de',
                       copies = [('t.schrader@fz-juelich.de', 'all'),
                                 ('andreas.ostermann@frm2.tum.de', 'all'),
                                 ('c.felder@fz-juelich.de', 'important'),
                                 ('alerts.sw.zea2@fz-juelich.de', 'important'),
                                ],
                       subject = '[NICOS] BIODIFF',
                      ),

    # Configure SMS receivers if wanted and registered with IT.
    smser    = device('devices.notifiers.SMSer',
                      description = 'SMS notifier',
                      server = 'triton.admin.frm2',
                     ),
)
