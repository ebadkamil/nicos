description = 'setup for the NICOS watchdog'
group = 'special'

# The entries in this list are dictionaries. Possible keys:
#
# 'setup' -- setup that must be loaded (default '' to mean all setups)
# 'condition' -- condition for warning (a Python expression where cache keys
#    can be used: t_value stands for t/value etc.
# 'gracetime' -- time in sec allowed for the condition to be true without
#    emitting a warning (default 5 sec)
# 'message' -- warning message to display
# 'type' -- for defining different types of warnings; this corresponds to the
#     configured notifiers (default 'default')
#     type '' does not emit warnings (useful together with 'pausecount'
#     for conditions that should block counting but are not otherwise errors)
# 'pausecount' -- if True, the count loop should be paused on the condition
#     (default False)
# 'action' -- code to execute if condition is true (default no code is executed)

watchlist = [
    dict(condition = 't_value > 300',
         message = 'Temperature too high (exceeds 300 K)',
         type = 'critical',
         gracetime = 1,
         action = 'maw(T, 290)'),
    dict(condition = 'phi_value > 100 and mono_value > 2.5',
         message = 'phi angle too high for current mono setting',
         gracetime = 5),
    dict(condition = 'tbefilter_value > 75',
         pausecount = True,
         message = 'Beryllium filter temperature too high',
         gracetime = 0),
    dict(condition = 'shutter_value == "closed"',
         type = '',
         pausecount = True,
         message = 'Instrument shutter is closed',
         gracetime = 0),
]


# The Watchdog device has two lists of notifiers, one for priority 1 and
# one for priority 2.

devices = dict(

    notifier = device('demo.notifier.DBusNotifier'),

    Watchdog = device('services.watchdog.Watchdog',
                      cache = 'localhost:14869',
                      notifiers = {'default': [], 'critical': ['notifier']},
                      watch = watchlist,
                     ),
)
