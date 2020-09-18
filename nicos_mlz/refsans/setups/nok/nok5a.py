description = 'NOK5a using Beckhoff controllers'

group = 'lowlevel'



instrument_values = configdata('instrument.values')
showcase_values = configdata('cf_showcase.showcase_values')
optic_values = configdata('cf_optic.optic_values')
tango_base = instrument_values['tango_base']
code_base = instrument_values['code_base']

index_r = 2
index_s = 3

devices = {
    '%s' % setupname : device(code_base + 'beckhoff.nok.DoubleMotorBeckhoffNOK',
        description = '%s layer optic' % setupname,
        tangodevice = tango_base + 'optic/io/modbus',
        addresses = [0x3020+index_r*10, 0x3020+index_s*10],
        ruler = [267.689, 279.73], # abs enc! 79.6439,
        nok_start = 2418.50,
        nok_end = 4137.70,
        nok_gap = 1.0,
        nok_motor = [3108.00, 3888.00],
        unit = 'mm, mm',
        fmtstr = '%.2f, %.2f',
        inclinationlimits = (-9.99, 9.99),
        masks = {
            'ng': optic_values['ng'],
            'rc': optic_values['ng'],
            'vc': optic_values['vc'],
            'fc': optic_values['fc'],
            # 'pola': showcase_values['pola'],
        },
    ),
}
