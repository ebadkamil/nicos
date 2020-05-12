#  -*- coding: utf-8 -*-

description = 'Eulerian cradle'

group = 'lowlevel'

includes = ['system', 'motorbus1', 'motorbus2', 'motorbus5']
excludes = ['euler']

devices = dict(
    st_echi = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus2',
        addr = 61,
        slope = 200,
        unit = 'deg',
        abslimits = (-1000000, 1000000),
        zerosteps = 500000,
        lowlevel = True,
    ),
    co_echi = device('nicos.devices.vendor.ipc.Coder',
        bus = 'motorbus1',
        addr = 130,
        slope = -8192,
        # zerosteps = 5334445,
        zerosteps = 0,
        unit = 'deg',
        circular = -360,
        lowlevel = True,
    ),
    echi = device('nicos.devices.generic.Axis',
        description = 'euler cradle rotation',
        motor = 'st_echi',
        coder = 'co_echi',
        # offset = -189.99926762282576,
        offset = 0,
        maxtries = 10,
        precision = 0.01,
        loopdelay = 1,
    ),
    st_echi1 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus2',
        addr = 61,
        slope = 1,
        unit = 'deg',
        abslimits = (1, 999999),
        zerosteps = 0,
        lowlevel = True,
    ),
    echi1 = device('nicos.devices.generic.Axis',
        description = 'euler cradle rotation',
        motor = 'st_echi1',
        # offset = -189.99926762282576,
        abslimits = (1, 999999),
        offset = 0,
        maxtries = 10,
        precision = 0.01,
        loopdelay = 1,
    ),
    st_ephi = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus5',
        addr = 84,
        slope = -100,
        unit = 'deg',
        abslimits = (-1000000, 1000000),
        zerosteps = 500000,
        lowlevel = True,
    ),
    co_ephi = device('nicos.devices.vendor.ipc.Coder',
        bus = 'motorbus1',
        addr = 136,
        slope = 4096,
        zerosteps = 0,
        unit = 'deg',
        circular = -360,
        lowlevel = True,
        confbyte = 148,
    ),
    ephi = device('nicos.devices.generic.Axis',
        description = 'euler cradle rotation',
        motor = 'st_ephi',
        coder = 'co_ephi',
        offset = 0,
        maxtries = 10,
        precision = 0.01,
        loopdelay = 1,
    ),
    st_ephi1 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus5',
        addr = 84,
        slope = 1,
        unit = 'deg',
        abslimits = (1, 999999),
        zerosteps = 0,
        lowlevel = True,
    ),
    ephi1 = device('nicos.devices.generic.Axis',
        description = 'euler cradle rotation',
        motor = 'st_ephi1',
        offset = 0,
        maxtries = 10,
        precision = 0.01,
        loopdelay = 1,
    ),
    ec = device('nicos.devices.tas.ecradle.EulerianCradle',
        description = 'Eulerian cradle',
        cell = 'Sample',
        tas = 'puma',
        chi = 'echi',
        omega = 'ephi'
    ),
)
