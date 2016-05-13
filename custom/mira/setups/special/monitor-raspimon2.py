description = 'setup for the right status monitor'
group = 'special'

_column1 = Column(
    Block('Heater long-term', [
        BlockRow(Field(plot='TPower', dev='t/heaterpower', width=40, height=30, plotwindow=24*3600)),
        ],
        setups='htf01',
    ),
    Block('Heater short-term', [
        BlockRow(Field(plot='TPower2', dev='t/heaterpower', width=40, height=25, plotwindow=1800)),
        ],
        setups='htf01',
    ),
    Block('MIEZE', [
        BlockRow(Field(name='Setting', dev='mieze', item=0, istext=True, width=5),
                 Field(name='tau', dev='mieze', item=1, unit='ps', width=7),
                 Field(name='Tuning', key='mieze/tuning', istext=True, width=10)),
        BlockRow('dc1', 'freq1', 'amp1', 'coilamp1'),
        BlockRow('dc2', 'freq2', 'amp2', 'coilamp2'),
        BlockRow('fp1', 'fp2', 'rp1', 'rp2'),
        BlockRow('cc1', 'cc2', 'freq3', 'amp3'),
        ],
        setups='mieze'
    ),
    Block('TAS display', [
        BlockRow(Field(widget='nicos.demo.monitorwidgets.VTas', width=30, height=18,
                       mthdev='m2th', mttdev='m2tt', sthdev='sth', sttdev='stt',
                       athdev='ath', attdev='att')),
        ],
        setups='tas',
    ),
    Block('MIRA Magnet', [
        BlockRow('I', 'B'),
        BlockRow(Field(name='T1', dev='miramagnet_T1', width=6, format='%d'),
                 Field(name='T2', dev='miramagnet_T2', width=6, format='%d')),
        BlockRow(Field(name='T3', dev='miramagnet_T3', width=6, format='%d'),
                 Field(name='T4', dev='miramagnet_T4', width=6, format='%d')),
        ],
        setups='miramagnet',
    ),
    Block('Garfield Magnet', [
        BlockRow(Field(name='on/off', dev='garfield_onoff')),
        BlockRow('I_garfield'),
        ],
        setups='garfield',
    ),
    Block('FRM Magnet', [
        BlockRow('B', # Field(name='sth', dev='sth_m7T5_stick'),
                 Field(name='T1', dev='m7T5_T1', width=6),
                 Field(name='T2', dev='m7T5_T2', width=6)),
        BlockRow(Field(name='T3', dev='m7T5_T3', width=6),
                 Field(name='T4', dev='m7T5_T4', width=6),
                 Field(name='T8', dev='m7T5_T8', width=6)),
        ],
        setups='magnet75',
    ),
    Block('SANS-1 Magnet', [
        BlockRow('B', Field(name='T2', dev='m5T_T2', width=6),
                 Field(name='T3', dev='m5T_T3', width=6)),
        BlockRow(Field(name='T4', dev='m5T_T4', width=6),
                 Field(name='T5', dev='m5T_T5', width=6),
                 Field(name='T6', dev='m5T_T6', width=6)),
        ],
        setups='magnet5',
    ),
    Block('HTS Magnet', [
        BlockRow(Field(dev='B_ccmhts01', name='I'))
        ],
        setups='ccmhts01',
    ),
    Block('3He cell', [
        BlockRow(Field(name='Polarization', dev='pol', width=7),
                 Field(name='Guide field', dev='He_GF')),
        ],
        setups='helios',
    ),
    Block('Y-Z table axes', [
        BlockRow('dty', 'dtz')
        ],
        setups='yztable',
    ),
    Block('Auxiliary currents', [
        BlockRow('Ipol1', 'Ipol2')
        ],
        setups='hpesupply',
    ),

    Block('TTi + Huber', [
        BlockRow('dct1', 'dct2', Field(dev='flip', width=5)),
        BlockRow('tbl1', 'tbl2'),
        ],
        setups='mezeiflip',
    ),
    Block('TTi + Huber 2', [
        BlockRow('dct3', 'dct4', Field(dev='flipx', width=5)),
        ],
        setups='mezeiflip2',
    ),
    Block('Guidefield coil', [
        BlockRow('dct5', 'dct6'),
        ],
        setups='gfcoil',
    ),
    Block('HV Stick', [
        BlockRow('HV')
        ],
        setups='hvstick',
    ),
    Block('Gas pressure cell', [
        BlockRow('diptron3plus', 'sentronicplus')
        ],
        setups='gascell',
    ),
)

_column2 = Column(
    Block('Eulerian cradle', [
        BlockRow('echi', 'ephi'),
    #   BlockRow(Field(dev='ec', name='Scattering plane', width=20, istext=True)),
        ],
        setups='euler',
    ),
    Block('Sample rotation (newport03', [
        BlockRow(Field(dev='sth_newport03')),
        ],
        setups='newport03',
    ),
    Block('Cryostat (CCR5)', [
        BlockRow(Field(name='Setpoint', key='T_ccr5/setpoint', unitkey='T_ccr5/unit', format='%.2f'),
                 Field(name='A', dev='T_ccr5_A'), Field(name='B', dev='T_ccr5_B'),
                 Field(name='C', dev='T_ccr5_C')),
        BlockRow(Field(name='P', key='t/p'), Field(name='I', key='t/i'),
                 Field(name='D', key='t/d'), Field(name='p', dev='ccr5_p1')),
        ],
        setups='ccr5',
    ),
    Block('Cryostat (CCR11)', [
        BlockRow(Field(name='Setpoint', key='t/setpoint', unitkey='t/unit', format='%.2f'),
                 Field(name='Control', dev='T'), Field(dev='Ts', name='Sample')),
        BlockRow(Field(name='A', dev='T_ccr11_A'), Field(name='B', dev='T_ccr11_B'),
                 Field(name='C', dev='T_ccr11_C'), Field(name='D', dev='T_ccr11_D')),
        BlockRow(Field(name='P', key='t/p'), Field(name='I', key='t/i'),
                 Field(name='D', key='t/d'), Field(name='p', dev='ccr11_p1')),
        ],
        setups='ccr11',
    ),
    Block('Cryostat (CCR21)', [
        BlockRow(Field(name='Setpoint', key='t/setpoint', unitkey='t/unit', format='%.2f'),
                 Field(name='Control', dev='T'), Field(dev='Ts', name='Sample')),
        BlockRow(Field(name='A', dev='T_ccr21_A'), Field(name='B', dev='T_ccr21_B'),
                 Field(name='C', dev='T_ccr21_C'), Field(name='D', dev='T_ccr21_D')),
        BlockRow(Field(name='P', key='t/p'), Field(name='I', key='t/i'),
                 Field(name='D', key='t/d'), Field(name='p', dev='ccr21_p1')),
        ],
        setups='ccr21',
    ),
    Block('Furnace (HTF01)', [
        BlockRow(Field(name='Setpoint', key='t_htf01/setpoint', unitkey='t_htf01/unit', format='%.2f'),
                 Field(name='Temp', dev='T_htf01')),
        BlockRow(Field(name='P', key='t_htf01/p'), Field(name='I', key='t_htf01/i'),
                 Field(name='D', key='t_htf01/d')),
        BlockRow(Field(name='Heater power', key='t_htf01/heaterpower', unit='%', format='%.2f'),
                 Field(name='Vacuum', dev='htf01_p')),
        ],
        setups='htf01',
    ),
    Block('Furnace (HTF03)', [
        BlockRow(Field(name='Setpoint', key='t_htf03/setpoint', unitkey='t_htf03/unit', format='%.2f'),
                 Field(name='Temp', dev='T_htf03')),
        BlockRow(Field(name='P', key='t_htf03/p'), Field(name='I', key='t_htf03/i'),
                 Field(name='D', key='t_htf03/d')),
        BlockRow(Field(name='Heater power', key='t_htf03/heaterpower', unit='%', format='%.2f'),
                 Field(name='Vacuum', dev='htf03_p')),
        ],
        setups='htf03',
    ),
    Block('Furnace (IRF01)', [
        BlockRow(Field(name='Setpoint', key='t_irf01/setpoint', unitkey='t_irf01/unit', format='%.2f'),
                 Field(name='Temp', dev='T_irf01')),
        BlockRow(Field(name='P', key='t_irf01/p'), Field(name='I', key='t_irf01/i'),
                 Field(name='D', key='t_irf01/d')),
        BlockRow(Field(name='Heater power', key='t_irf01/heaterpower', unit='%', format='%.2f')),
        ],
        setups='irf01',
    ),
    Block('3He insert (cci3he2)', [
        BlockRow(Field(name='Setpoint', key='T_cci3he2/setpoint', unitkey='T_cci3he2/unit', format='%.2f'),
                 Field(name='T', dev='T'), Field(name='Ts', dev='Ts')),
        BlockRow(Field(name='P', key='t/p', width=4), Field(name='I', key='t/i', width=4),
                 Field(name='D', key='t/d', width=4),
                 Field(name='turbo', dev='cci3he2_p1'),
                 Field(name='cycle', dev='cci3he2_p4'),
                 ),
        ],
        setups='cci3he2',
    ),
    Block('3He-4He insert (ccidu1)', [
        BlockRow(Field(name='Setpoint', key='t/setpoint', unitkey='t/unit', format='%.2f'),
                 Field(name='T', dev='T'), Field(name='Ts', dev='Ts')),
        BlockRow(Field(name='P', key='t/p', width=4), Field(name='I', key='t/i', width=4),
                 Field(name='D', key='t/d', width=4),
                 Field(name='turbo', dev='ccidu1_p1'),
                 Field(name='cycle', dev='ccidu1_p4'),
                 ),
        ],
        setups='ccidu1',
    ),
    Block('3He-4He insert (ccidu2)', [
        BlockRow(Field(name='Setpoint', key='t/setpoint', unitkey='t/unit', format='%.2f'),
                 Field(name='T', dev='T'), Field(name='Ts', dev='Ts')),
        BlockRow(Field(name='P', key='t/p', width=4), Field(name='I', key='t/i', width=4),
                 Field(name='D', key='t/d', width=4),
                 Field(name='turbo', dev='ccidu2_p1'),
                 Field(name='cycle', dev='ccidu2_p4'),
                 ),
        ],
        setups='ccidu2',
    ),
    Block('3He insert (cci3he1)', [
        BlockRow(Field(name='Setpoint', key='T_cci3he1/setpoint', unitkey='T_cci3he1/unit', format='%.2f'),
                 Field(name='T', dev='T'), Field(name='Ts', dev='Ts')),
        BlockRow(Field(name='P', key='t/p', width=4), Field(name='I', key='t/i', width=4),
                 Field(name='D', key='t/d', width=4),
                 Field(name='turbo', dev='cci3he1_p1'),
                 Field(name='cycle', dev='cci3he1_p4'),
                 ),
        ],
        setups='cci3he1',
    ),
    Block('3He insert (cci3he3)', [
        BlockRow(Field(name='Setpoint', key='t/setpoint', unitkey='t/unit', format='%.2f'),
                 Field(name='T', dev='T'), Field(name='Ts', dev='Ts')),
        BlockRow(Field(name='P', key='t/p', width=4), Field(name='I', key='t/i', width=4),
                 Field(name='D', key='t/d', width=4),
                 Field(name='turbo', dev='cci3he3_p1'),
                 Field(name='cycle', dev='cci3he3_p4'),
                 ),
        ],
        setups='cci3he3',
    ),
)

_column3 = Column(
#    Block('Temperature long-term', [
#        BlockRow(Field(plot='TT', dev='T', width=40, height=30, plotwindow=24*3600),
#                 Field(plot='TT', dev='Ts'),
#                 Field(plot='TT', key='t/setpoint')),
#        ],
#    ),
#    Block('Temperature short-term', [
#        BlockRow(Field(plot='TT2', dev='T', width=40, height=25, plotwindow=1800),
#                 Field(plot='TT2', dev='Ts'),
#                 Field(plot='TT2', key='t/setpoint')),
#        ],
#    ),
)

devices = dict(
    Monitor = device('services.monitor.qt.Monitor',
                     title = 'MIRA Sample environment',
                     loglevel = 'info',
                     cache = 'mira1:14869',
                     prefix = 'nicos/',
                     font = 'Luxi Sans',
                     valuefont = 'Consolas',
                     fontsize = 22,
                     padding = 5,
                     layout = [[_column1, _column2, _column3]])
)
