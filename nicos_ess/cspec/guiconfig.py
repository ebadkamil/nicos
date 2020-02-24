"""NICOS GUI default configuration."""

main_window = docked(
    vsplit(
        panel('nicos.clients.gui.panels.status.ScriptStatusPanel',
              stopcounting=True),
        # panel('nicos.clients.gui.panels.watch.WatchPanel'),
        panel('nicos.clients.gui.panels.console.ConsolePanel',
              watermark='nicos_ess/cspec/gui/logo-watermark.png'),
    ),
    ('NICOS devices',
     panel('nicos.clients.gui.panels.devices.DevicesPanel', icons=True,
           dockpos='right',),
    ),
    # ('Detector information',
    #  panel('nicos.clients.gui.panels.generic.GenericPanel',
    #        uifile='nicos_mlz/toftof/gui/ratespanel.ui'),
    # ),
    ('Experiment Information and Setup',
     panel('nicos.clients.gui.panels.expinfo.ExpInfoPanel')
    ),
)

windows = [
    window('Editor', 'editor',
        vsplit(
    #         panel('nicos.clients.gui.panels.scriptbuilder.CommandsPanel'),
            panel('nicos.clients.gui.panels.editor.EditorPanel',
                  tools = [
    #                 tool('Scan Generator',
    #                 'nicos.clients.gui.panels.tools.ScanTool'),
                  ],
            ),
        ),
    ),
    # window('Setup', 'setup',
    #     tabbed(('Experiment',
    #             panel('nicos.clients.gui.panels.setup_panel.ExpPanel')),
    #            ('Setups',
    #             panel('nicos.clients.gui.panels.setup_panel.SetupsPanel')),
    #            ('Detectors/Environment',
    #             panel('nicos.clients.gui.panels.setup_panel.DetEnvPanel')),
    #     )
    # ),
    window('Scans', 'plotter',
           panel('nicos.clients.gui.panels.scans.ScansPanel')),
    window('History', 'find',
           panel('nicos.clients.gui.panels.history.HistoryPanel'),),
    window('Logbook', 'table',
           panel('nicos.clients.gui.panels.elog.ELogPanel'),),
    window('Errors', 'errors',
           panel('nicos.clients.gui.panels.errors.ErrorPanel'),),
    window('Live data', 'live',
           panel('nicos.clients.gui.panels.live.LiveDataPanel',
                 instrument = 'toftof'),),
]

tools = [
    # tool('Downtime report', 'nicos.clients.gui.tools.downtime.DownTimeTool',
    #      receiver='f.carsughi@fz-juelich.de',
    #      mailserver='smtp.frm2.tum.de',
    #      sender='toftof@frm2.tum.de',
    #     ),
    tool('Calculator', 'nicos.clients.gui.tools.calculator.CalculatorTool'),
    tool('Neutron cross-sections',
         'nicos.clients.gui.tools.website.WebsiteTool',
         url='http://www.ncnr.nist.gov/resources/n-lengths/'),
    tool('Neutron activation', 'nicos.clients.gui.tools.website.WebsiteTool',
         url='https://webapps.frm2.tum.de/intranet/activation/'),
    tool('Neutron calculations',
         'nicos.clients.gui.tools.website.WebsiteTool',
         url='https://webapps.frm2.tum.de/intranet/neutroncalc/'),
    tool('Report NICOS bug or request enhancement',
         'nicos.clients.gui.tools.bugreport.BugreportTool'),
    tool('Emergency stop button',
         'nicos.clients.gui.tools.estop.EmergencyStopTool',
         runatstartup=False,),
]
