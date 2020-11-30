from nicos.commands import usercommand
from nicos_ess.ymir.commands.start_stop_writing import StartFileWriter,\
    StopFileWriter


class SetGetHandler:
    """
    An auxiliary class for setting and getting the file writer handler
    object. This class is needed as the corresponding class of starting a write
    job should be instantiated only once.
    """
    def __init__(self):
        self.handler = None

    def set_handler(self, handler_value):
        self.handler = handler_value

    def get_handler(self):
        return self.handler


# Global initialisation is required to not to override the handler value via a
# stop write job call.
sg_handler = SetGetHandler()


@usercommand
def start_writing():
    writer = StartFileWriter()
    writer.start_job()
    # Set the handler which is to be used to stop the write job.
    sg_handler.set_handler(writer.get_handler())
    print('Write job is started.')


@usercommand
def stop_writing():
    StopFileWriter(sg_handler.get_handler()).stop_job()
    print('Write job is stopped.')
