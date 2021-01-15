from time import time as currenttime
from nicos.core import Readable, Param, status, Device, host, listof
from streaming_data_types import deserialise_x5f2
import json
from nicos_ess.devices.kafka.status_handler import KafkaStatusHandler


class FileWriterStatus(KafkaStatusHandler, Readable):

    def new_messages_callback(self, messages):
        key = max(messages.keys())
        if messages[key][4:8] == b"x5f2":
            result = deserialise_x5f2(messages[key])
            _status = json.loads(result.status_json)
            self._setROParam(
                'statusinterval', result.update_interval // 1000
            )
            if _status['state'] == 'idle':
                self.curstatus = status.OK, _status['state']
            else:
                self.curstatus = status.BUSY, _status['state']
            next_update = currenttime() + self.statusinterval
            if next_update > self.nextupdate:
                self._setROParam('nextupdate', next_update)


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
