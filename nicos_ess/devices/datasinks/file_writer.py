from time import time as currenttime

from nicos_ess.devices.kafka.consumer import KafkaSubscriber
from nicos.core import Readable, tupleof, Param, POLLER, status, MASTER, Device, host, listof
from nicos import session
from nicos.core.constants import SIMULATION

from streaming_data_types import deserialise_x5f2

import json


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
        key = max(messages.keys())
        if messages[key][4:8] == b"x5f2":
            result = deserialise_x5f2(messages[key])
            _status = json.loads(result.status_json)
            if _status['state'] == 'idle':
                self.curstatus = status.OK, _status['state']
            else:
                self.curstatus = status.BUSY, _status['state']

    def no_messages_callback(self):
        # Check if the process is still running
        # if self._mode == MASTER and not self.is_process_running():
        #     self._setROParam('curstatus', (status.ERROR, 'Disconnected'))
        # TODO: not urgent but make it work like status_handler.py
        pass

    def is_process_running(self):
        # Allow some leeway in case of message lag.
        if currenttime() > self.nextupdate + self.timeoutinterval:
            return False
        return True


class FileWriterParameters(Device):
    parameters = {
        'broker': Param('List of kafka hosts to be connected to',
            type=listof(host(defaultport=9092)),
            default=['localhost'], preinit=True, userparam=False),
        'command_topic': Param(
            'Kafka topic where status messages are written',
            type=str, settable=False, preinit=True, mandatory=True,
            userparam=False,),
        'nexus_config_path': Param('NeXus configuration file (full-path)',
            type=str, mandatory=True, userparam=False,),
    }
