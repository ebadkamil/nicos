from file_writer_control.JobStatus import JobState

from nicos import session
from nicos.commands import usercommand
from nicos_ess.utilities.managers import wait_before
from nicos_ess.ymir.commands.start_stop_writing import StartFileWriter,\
    StopFileWriter


class StartStopWriting:
    """
    Base Class for Nicos interface of FileWriter. Any extensions to start-stop
    user commands should be done here.
    """
    def __init__(self):
        super().__init__()
        self.handler = None
        self.job_id = ""

    def _set_handler(self, handler_value):
        self.handler = handler_value

    def _get_handler(self):
        return self.handler

    def _set_id(self, job_id):
        self.job_id = job_id

    def _get_id(self):
        return self.job_id

    def start(self):
        """
        Starts the write job and sets JobHandler and JobId.
        """
        device = session.getDevice('FileWriterParameters')
        self._set_id(device.get_job_id())
        if not self._get_id() is "":
            session.log.warning(
                'A write process is already running. To start a new'
                'job, please stop the current one.')
            return
        writer = StartFileWriter()
        _start = writer.start_job()
        if _start:
            # Set the handler which is to be used to stop the write job.
            self._set_handler(writer.get_handler())
            # Set the job id.
            self._set_id(writer.get_job_id())
            # Wait five seconds to validate. This magic time should be
            # optimized and be made proper.
            with wait_before(5):
                # Validate once if the FileWriter indeed started.
                if not self._validate_write_process():
                    session.log.error('Write job could not be validated. '
                                      'Please check if FileWriter is up and '
                                      'running.')
                    # We do not wanna disturb other parts of the script or
                    # series of commands if writing cannot be validated. Thus
                    # if that is the case we shall just return after the
                    # warning. However, in case (highly probably) a job
                    # identifier is provided by FileWriterControl, we would like
                    # reset it to empty string as the job is not successfully
                    # started. To that end, we shall do a stop call.
                    self.stop()
                    return

    def stop(self):
        """
        Stops the write job and update the handler status so that a new job can
        be started without an issue.
        """
        job_id = self._get_id()
        if job_id == "":
            session.log.error('There is no write job in process. Nothing to '
                              'stop.')
            return
        _stop = StopFileWriter(self._get_handler(), self._get_id())
        # Stop the write process.
        stop_call = _stop.stop_job()
        if stop_call:
            # Update the status so that File Writer can be restarted for
            # a new job.
            device = session.getDevice('FileWriterParameters')
            if _stop.get_status() is None:
                # By default, if there is no write job, the FileWriterControl
                # returns a None, validating we have successfully stopped,
                # so we can safely assign an empty string to the cache.
                device.set_job_id("")
                # Set it internally as a direct call to stop does not
                # communicate with the device.
                self._set_id("")

    def _validate_write_process(self):
        handler = self._get_handler()
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
