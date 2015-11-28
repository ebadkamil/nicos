# This setup file configures the nicos poller service.

description = 'setup for the poller'
group = 'special'

sysconfig = dict(
    # use only 'localhost' if the cache is really running on the same machine,
    # otherwise use the official computer name
    cache = 'localhost'
)

devices = dict(
    Poller = device('services.poller.Poller',
                    # setups that should be polled regardless if loaded
                    alwayspoll = ['gedet'],
                    neverpoll = [],  # setups that should not be polled even if loaded
                    blacklist = [],  # DEVICES that should never be polled
                                     # (usually detectors or devices that have problems
                                     # with concurrent access from processes)
                   ),
)
