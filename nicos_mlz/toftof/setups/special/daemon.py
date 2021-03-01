description = 'setup for the execution daemon'

group = 'special'

devices = dict(
    Auth = device('nicos.services.daemon.auth.list.Authenticator',
        hashing = 'md5',
        # first entry is the user name, second the hashed password, third the user level
        passwd = [
            ('guest', '', 'guest'),
            ('user', 'ee11cbb19052e40b07aac0ca060c23ee', 'user'),
            ('root', 'f88868f6f9fe65b21dadc685ef6ad99f', 'admin'),
        ],
    ),
    Daemon = device('nicos.services.daemon.NicosDaemon',
        server = 'tofhw.toftof.frm2',
        authenticators = ['Auth'],
        loglevel = 'info',
    ),
)
