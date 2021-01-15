description = 'setup for the status monitor'
group = 'special'

_testblock = Block('HTF03', [
    BlockRow(
        Field(gui='nicos_mlz/sans1/gui/htf03.ui')),
    ],
)

_testcolumn = Column(_testblock)

devices = dict(
    Monitor = device('nicos.services.monitor.qt.Monitor',
        title = 'SANS-1 status monitor',
        # loglevel = 'debug',
        loglevel = 'info',
        cache = 'sans1ctrl.sans1.frm2',
        prefix = 'nicos/',
        font = 'Luxi Sans',
        valuefont = 'Consolas',
        fontsize = 12,
        padding = 3,
        layout = [Row(_testcolumn)],
    ),
)
