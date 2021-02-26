from nicos import session
from file_writer_control.WorkerCommandChannel import WorkerCommandChannel
from file_writer_control.WriteJob import WriteJob
from file_writer_control.JobHandler import JobHandler
from datetime import datetime

from nicos_ess.utilities.managers import wait_until_true, wait_after


class WriterBase:
    def __init__(self):
        self.device = session.getDevice('FileWriterParameters')
        self.host = self.device.broker[0]
        self.config = self.device.nexus_config_path
        self.topic = self.device.command_topic
        self.command_channel = WorkerCommandChannel(f'{self.host}/{self.topic}')


class StartFileWriter(WriterBase):
    """
    The class for starting a write job in ESS File Writer (FW).
    It assumes a corresponding Kafka broker is up and running along with FW.
    """
    def __init__(self):
        super().__init__()

        self.job_handler = JobHandler(worker_finder=self.command_channel)
        self.write_job = None
        self.job_id = ""

    def start_job(self):
        with open(self.config, "r") as f:
            # Get the nexus structure from config.
            nexus_structure = f.read()
        # Initialise the write job.
        self.write_job = WriteJob(
            nexus_structure,
            "{0:%Y}-{0:%m}-{0:%d}_{0:%H}{0:%M}.nxs".format(datetime.now()),
            self.host,
            datetime.now(),
        )
        # Start.
        start_handler = self.job_handler.start_job(self.write_job)
        self.job_id = self.write_job.job_id
        # Send the acquired job identifier to the Nicos Cache.
        self.device.set_job_id(self.job_id)
        wait_until_true([start_handler.is_done()])
        session.log.info(f'Write job with <<ID: {self.job_id}>> is started.')
        return True

    def get_handler(self):
        return self.job_handler

    def get_job_id(self):
        return self.job_id


class StopFileWriter(WriterBase):
    """
    The class to stop an ongoing write job specified with the corresponding
    write-job handler. The class does not inherit from StartFileWriter
    to prevent any false initiations of write job.
    """
    def __init__(self, handler, _id):
        super().__init__()
        self.job_handler = handler
        self.job_id = _id

    def stop_job(self):
        if self.job_handler is None:
            # This can happen if Nicos is restarted while a write job is in
            # process. In that case we retrieve the ID from the cache and
            # then create a new handler for it.
            with wait_after(5):
                # We shall wait five seconds after the creation of
                # a new handler to ensure proper communication between
                # FileWriter and the Control Library.
                self.job_handler = JobHandler(
                    worker_finder=self.command_channel, job_id=self.job_id)
        stop_handler = self.job_handler.stop_now()
        wait_until_true([stop_handler.is_done(),
                        self.job_handler.is_done()])
        session.log.info(f'Write job with job <<ID: {self.job_id}>> '
                         f'is stopped. Wait for confirmation'
                         f' to start a new job.')
        return True

    def get_status(self):
        return self.command_channel.get_job_status(self.job_id)
