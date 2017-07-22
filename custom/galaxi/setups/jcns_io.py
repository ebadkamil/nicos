# -*- coding: utf-8 -*-

description = 'GALAXI digital in- and outputs'

group = 'optional'

includes = []

tango_base = 'tango://localhost:10000/galaxi/'
tango_digital = tango_base + 'fzjdp_digital/'
tango_analog  = tango_base + 'fzjdp_analog/'

devices = dict(

    vacuumtube1  = device('nicos.devices.tango.AnalogInput',
                          description = 'Vacuum tube 1',
                          tangodevice = tango_analog + 'VacuumTube1',
                         ),
    vacuumtube2  = device('nicos.devices.tango.AnalogInput',
                          description = 'Vacuum tube 2',
                          tangodevice = tango_analog + 'VacuumTube2',
                         ),
    vacuumtube3  = device('nicos.devices.tango.AnalogInput',
                          description = 'Vacuum tube 3',
                          tangodevice = tango_analog + 'VacuumTube3',
                         ),
    pump02       = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Pump 2',
                          tangodevice = tango_digital + 'Pumpe2',
                          mapping = dict(on=1, off=2),
                          fmtstr = '%s',
                         ),
    pump03       = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Pump 3',
                          tangodevice = tango_digital + 'Pumpe3',
                          mapping = dict(on=1, off=2),
                          fmtstr = '%s',
                         ),
    detectorpos  = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Detectorposition',
                          tangodevice = tango_digital + 'DetectorPos',
                          mapping = dict(pos1=1, pos2=2, pos3=4,
                                         pos4=8, pos5=16),
                          fmtstr = '%s',
                          lowlevel = True,
                         ),
    detectube01  = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Detectortube 1',
                          tangodevice = tango_digital + 'DetectorTube1',
                          mapping = dict(up=1, down=2),
                          fmtstr = '%s',
                         ),
    detectube02  = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Detectortube 2',
                          tangodevice = tango_digital + 'DetectorTube2',
                          mapping = dict(up=1, down=2),
                          fmtstr = '%d',
                         ),
    detectube03  = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Detectortube 3',
                          tangodevice = tango_digital + 'DetectorTube3',
                          mapping = dict(up=1, down=2),
                          fmtstr = '%d',
                         ),
    detectube04  = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Detectortube 4',
                          tangodevice = tango_digital + 'DetectorTube4',
                          mapping = dict(up=1, down=2),
                          fmtstr = '%d',
                         ),
    detdistance  = device('nicos_mlz.galaxi.devices.distance.DetectorDistance',
                          description = 'Pilatus detector distance',
                          detectubes = ['detectube01','detectube02',
                                        'detectube03','detectube04'],
                          offset = 831,
                          unit = 'mm',
                          fmtstr = '%d',
                         ),
    vavalve01    = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Vacuumvalve 1',
                          tangodevice = tango_digital + 'VacuumValve1',
                          mapping = dict(open=0, close=1),
                          fmtstr = '%s',
                         ),
    vavalve02    = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Vacuumvalve 2',
                          tangodevice = tango_digital + 'VacuumValve2',
                          mapping = dict(open=0, close=1),
                          fmtstr = '%s',
                         ),
    vavalve03    = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Vacuumvalve 2',
                          tangodevice = tango_digital + 'VacuumValve2',
                          mapping = dict(open=0, close=1),
                          fmtstr = '%s',
                         ),
    vavalve04    = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Vacuumvalve 4',
                          tangodevice = tango_digital + 'VacuumValve4',
                          mapping = dict(open=0, close=1),
                          fmtstr = '%s',
                         ),
    vavalve05    = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Vacuumvalve 5',
                          tangodevice = tango_digital + 'VacuumValve5',
                          mapping = dict(open=0, close=1),
                          fmtstr = '%s',
                         ),
    vavalve06    = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Vacuumvalve 6',
                          tangodevice = tango_digital + 'VacuumValve6',
                          mapping = dict(open=0, close=1),
                          fmtstr = '%s',
                         ),
    vevalve01    = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Ventilationvalve 1',
                          tangodevice = tango_digital + 'VentilationValve1',
                          mapping = dict(open=0, close=1),
                          fmtstr = '%s',
                         ),
    vevalve02    = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Ventilationvalve 2',
                          tangodevice = tango_digital + 'VentilationValve2',
                          mapping = dict(open=0, close=1),
                          fmtstr = '%s',
                         ),
    vevalve03    = device('nicos.devices.tango.NamedDigitalInput',
                          description = 'Ventilationvalve 3',
                          tangodevice = tango_digital + 'VentilationValve3',
                          mapping = dict(open=0, close=1),
                          fmtstr = '%s',
                         ),
)
