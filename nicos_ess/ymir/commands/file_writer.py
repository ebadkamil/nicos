from nicos.commands import helparglist, usercommand
from nicos import session

@usercommand
@helparglist('value')
def mulitple_by_2(value):
    session.log.warn(value * 2)

def start_writing():
    pass

def stop_writing():
    pass
