description = 'setup for the execution daemon'
group = 'special'

import hashlib

devices = dict(
    Auth   = device('services.daemon.auth.ListAuthenticator',
                    hashing = 'sha1',
                    # first entry is the user name, second the hashed password, third the user level
                    passwd = [('guest', '', 'guest'),
                              ('user', hashlib.sha1('user').hexdigest(), 'user'),
                              ('admin', hashlib.sha1('admin').hexdigest(), 'admin')],
                   ),
    Daemon = device('services.daemon.NicosDaemon',
                    server = 'localhost',
                    authenticators = ['Auth'],
                    loglevel = 'debug',
                   ),
)
