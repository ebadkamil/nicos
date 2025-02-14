description = 'setup for the execution daemon'
group = 'special'

devices = dict(
    LDAPAuth = device('nicos.services.daemon.auth.ldap.Authenticator',
        uri = 'ldap://phaidra.admin.frm2',
        userbasedn = 'ou=People,dc=frm2,dc=de',
        groupbasedn = 'ou=Group,dc=frm2,dc=de',
        grouproles = {
            'reseda': 'admin',
            'ictrl': 'admin',
            'se': 'user',
        },
    ),
    UserDBAuth = device('nicos_mlz.devices.ghost.Authenticator',
         description = 'FRM II user office authentication',
         instrument = 'RESEDA',
         ghosthost = 'ghost.mlz-garching.de',
         loglevel = 'info',
    ),
    Daemon = device('nicos.services.daemon.NicosDaemon',
        server = '0.0.0.0',
        authenticators = [
            'LDAPAuth',
            'UserDBAuth',
        ],
    ),
)
