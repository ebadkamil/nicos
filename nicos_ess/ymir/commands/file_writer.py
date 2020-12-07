from nicos import session
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
        self.id = None

    def set_handler(self, handler_value):
        self.handler = handler_value

    def get_handler(self):
        return self.handler

    def set_id(self, job_id):
        self.id = job_id

    def get_id(self):
        return self.id


# Global initialisation is required to not to override the handler value via a
# stop write job call.
sg_handler = SetGetHandler()


@usercommand
def start_writing():
    if not sg_handler.get_handler() is None:
        session.log.warning('A write process is already running. To start a new'
                            'job, please stop the current one.')
        return
    writer = StartFileWriter()
    writer.start_job()
    # Set the handler which is to be used to stop the write job.
    sg_handler.set_handler(writer.get_handler())
    # Set the job id in case it is needed.
    sg_handler.set_id(writer.get_job_id())


@usercommand
def stop_writing():
    _stop = StopFileWriter(sg_handler.get_handler(), sg_handler.get_id())
    # Stop the write process.
    _stop.stop_job()
    # Update the status so that File Writer can be restarted for a new job.
    sg_handler.set_handler(_stop.get_status())
