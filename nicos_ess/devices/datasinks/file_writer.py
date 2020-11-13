from time import time as currenttime

from nicos_ess.devices.kafka.consumer import KafkaSubscriber
from nicos.core import Readable, tupleof, Param, POLLER, status, MASTER
from nicos import session
from nicos.core.constants import SIMULATION


class FileWriterStatus(KafkaSubscriber, Readable):

    parameters = {
        'statustopic': Param(
            'Kafka topic where status messages are written',
            type=str, settable=False, preinit=True, mandatory=True,
            userparam=False,),
        'timeoutinterval': Param(
            'Time to wait (secs) before communication is considered lost',
            type=int, default=5, settable=True, userparam=False,),
        'curstatus': Param('Store the current device status',
            internal=True, type=tupleof(int, str), settable=True,),
        'nextupdate': Param('Time when the next message is expected',
            type=int, internal=True, settable=True, ),
        'statusinterval': Param(
            'Expected time (secs) interval for the status message updates',
            type=int, default=2, settable=True, internal=True, ),
    }

    def doPreinit(self, mode):
        KafkaSubscriber.doPreinit(self, mode)
        if session.sessiontype != POLLER and mode != SIMULATION:
            self.subscribe(self.statustopic)

        # Be pessimistic and assume the process is down, if the process
        # is up then the status will be remedied quickly.
        self._setROParam('nextupdate', currenttime())

        if self._mode == MASTER:
            self._setROParam(
                'curstatus', (status.WARN, 'Trying to connect...')
            )

    def doRead(self, maxage=0):
        return ''

    def doStatus(self, maxage=0):
        return self.curstatus

    def new_messages_callback(self, messages):
        self.log.warn('message received.')

    def no_messages_callback(self):
        # Check if the process is still running
        if self._mode == MASTER and not self.is_process_running():
            self._setROParam('curstatus', (status.ERROR, 'Disconnected'))

    def is_process_running(self):
        # Allow some leeway in case of message lag.
        if currenttime() > self.nextupdate + self.timeoutinterval:
            return False
        return True
