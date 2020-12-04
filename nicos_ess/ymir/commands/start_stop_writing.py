from nicos import session
from file_writer_control.WorkerCommandChannel import WorkerCommandChannel
from file_writer_control.WriteJob import WriteJob
from file_writer_control.JobHandler import JobHandler
from datetime import datetime

from nicos_ess.utilities.managers import wait_until_true


class StartFileWriter:
    """
    The class for starting a write job in ESS File Writer (FW).
    It assumes a corresponding Kafka broker is up and running along with FW.
    """
    def __init__(self):

        self.device = session.getDevice('FileWriterParameters')
        self.host = self.device.broker[0]
        self.config = self.device.nexus_config_path
        self.topic = self.device.command_topic

        self.command_channel = WorkerCommandChannel(f'{self.host}/{self.topic}')
        self.job_handler = JobHandler(worker_finder=self.command_channel)
        self.write_job = None
        self.job_id = None

    def start_job(self):
        with open(self.config, "r") as f:
            nexus_structure = f.read()
        self.write_job = WriteJob(
            nexus_structure,
            "{0:%Y}-{0:%m}-{0:%d}_{0:%H}{0:%M}.nxs".format(datetime.now()),
            self.host,
            datetime.now(),
        )
        start_handler = self.job_handler.start_job(self.write_job)
        self.job_id = self.write_job.job_id
        wait_until_true([start_handler.is_done()])
        session.log.info('Write job is started.')

    def get_handler(self):
        return self.job_handler

    def get_job_id(self):
        return self.job_id


class StopFileWriter:
    """
    The class to stop an ongoing write job specified with the corresponding
    write-job handler.
    """
    def __init__(self, handler):
        self.job_handler = handler

    def stop_job(self):
        stop_handler = self.job_handler.stop_now()
        wait_until_true([stop_handler.is_done(),
                        self.job_handler.is_done()])
        session.log.info('Write job is stopped.')
