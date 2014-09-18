#  -*- coding: utf-8 -*-

description = 'Atenuator and PGFilter'

group = 'lowlevel'

includes = ['system', 'motorbus6', 'motorbus8']

devices = dict(

   att_sw = device('devices.vendor.ipc.Input',
                bus = 'motorbus8',
                addr = 104,
                first = 0,
                last = 9,
                lowlevel = True,
                unit = ''),
   att_press = device('devices.vendor.ipc.Input',
                bus = 'motorbus8',
                addr = 103,
                first = 13,
                last = 13,
                lowlevel = True,
                unit = ''),
   att_set = device('devices.vendor.ipc.Output',
                bus = 'motorbus8',
                addr = 114,
                first = 3,
                last = 7,
                lowlevel = True,
                unit = ''),

   atn = device('puma.attenuator.Attenuator',
                description = 'Sample attenuator, width=0..38mm',
                io_status = 'att_sw',
                io_set = 'att_set',
                io_press = 'att_press',
                abslimits = (0, 38),
                unit = 'mm'),

   fpg_sw = device('devices.vendor.ipc.Input',
                bus = 'motorbus6',
                addr = 111,
                first = 12,
                last = 13,
                lowlevel = True,
                unit = ''),

   fpg_set = device('devices.vendor.ipc.Output',
                bus = 'motorbus6',
                addr = 103,
                first = 0,
                last = 0,
                lowlevel = True,
                unit = ''),

   fpg1 = device('puma.pgfilter.PGFilter',
                description = 'automated pg filter',
                io_status = 'fpg_sw',
                io_set = 'fpg_set',
                unit = ''),

   uni_sw = device('devices.vendor.ipc.IPCSwitches',
                description = 'Switches of the lift axis card',
                bus = 'motorbus6',
                addr = 70,
                fmtstr = '%d',
#                lowlevel = True,
                ),

   uni_st = device('devices.vendor.ipc.Motor',
                bus = 'motorbus6',
                addr = 70,
                slope = 1,
                unit = 'mm',
                abslimits = (0, 999999),
                zerosteps = 0,
#                lowlevel = True,
                ),

   fpg2 = device('puma.senseswitch.SenseSwitch',
                description = 'Second PG filter',
                moveable = 'uni_st',
                readable = 'uni_sw',
                mapping = { 'in'  : (500000, 1),
                            'out' : (535900, 2),
                          },
                precision = [100, 0],
                blockingmove = True,
                timeout = 300,
                ),
)
