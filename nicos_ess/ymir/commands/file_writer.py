from file_writer_control.JobStatus import JobState

from nicos import session
from nicos.commands import usercommand
from nicos_ess.utilities.managers import wait_after, wait_before
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


class StartStopWriting(SetGetHandler):
    """
    Base Class for Nicos interface of FileWriter. Any extensions to start-stop
    user commands should be done here.
    """
    def __init__(self):
        super().__init__()

    def start(self):
        """
        Starts the write job and sets JobHandler and JobId.
        """
        if not self.get_handler() is None:
            session.log.warning(
                'A write process is already running. To start a new'
                'job, please stop the current one.')
            return
        writer = StartFileWriter()
        _start = writer.start_job()
        if _start:
            # Set the handler which is to be used to stop the write job.
            self.set_handler(writer.get_handler())
            # Set the job id.
            self.set_id(writer.get_job_id())
            # Wait five seconds to validate. This magic time should be
            # optimized and be made proper.
            with wait_before(5):
                # Validate once if the FileWriter indeed started.
                if not self._validate_write_process():
                    session.log.error('Write job could not be validated.')
                    # We do not wanna disturb other parts of the script or
                    # series of commands if writing cannot be validated. Thus
                    # if that is the case we shall just return after the
                    # warning.
                    return

    def stop(self):
        """
        Stops the write job and update the handler status so that a new job can
        be started without an issue.
        """
        _stop = StopFileWriter(self.get_handler(), self.get_id())
        # Stop the write process.
        _stop.stop_job()
        # Update the status so that File Writer can be restarted for a new job.
        self.set_handler(_stop.get_status())

    def _validate_write_process(self):
        handler = self.get_handler()
        if not handler.get_state() == JobState.WRITING:
            return False
        return True


ss_writing = StartStopWriting()


@usercommand
def start_writing():
    ss_writing.start()


@usercommand
def stop_writing():
    ss_writing.stop()
