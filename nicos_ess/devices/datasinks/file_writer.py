#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2021 by the NICOS contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   AÜC Hardal <umit.hardal@ess.eu>
#
# *****************************************************************************

import json
from datetime import datetime
from time import time as currenttime

from file_writer_control.JobHandler import JobHandler
from file_writer_control.WorkerCommandChannel import WorkerCommandChannel
from file_writer_control.WriteJob import WriteJob
from streaming_data_types import deserialise_x5f2

from nicos import session
from nicos.commands.basic import sleep
from nicos.core import ADMIN, Device, Param, host, listof, requires, status

from nicos_ess.devices.kafka.status_handler import KafkaStatusHandler


class FileWriterStatus(KafkaStatusHandler):

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


class FileWriterControl(Device):
    parameters = {
        'broker': Param('List of kafka hosts to be connected',
            type=listof(host(defaultport=9092)), mandatory=True, preinit=True,
            userparam=False
        ),
        'command_topic': Param(
            'Kafka topic where status messages are written',
            type=str, settable=False, preinit=True, mandatory=True,
            userparam=False,
        ),
        'nexus_config_path': Param('NeXus configuration file (full-path)',
            type=str, mandatory=True, userparam=False,),
        'job_id': Param('Writer job identification',
            type=str, mandatory=False, userparam=False,
            internal=True
        ),
        'ack_timeout': Param('How long to wait for timeout on acknowledgement',
            type=int, default=5, unit='s', userparam=False,
            settable=False,
        ),
    }

    command_channel = None
    job_handler = None

    def doPreinit(self, mode):
        self._set_job_id(self._cache.get(self.name, "job_id", default=''))
        self.command_channel = \
            WorkerCommandChannel(f'{self.broker[0]}/{self.command_topic}')
        # If there is a job_id then this means the file-writer is currently
        # writing
        self.job_handler = JobHandler(worker_finder=self.command_channel,
                                      job_id=self.job_id)

    def doStart(self):
        self.log.warning("doStart")
        if self.job_id:
            session.log.warning(
                'A write job is already running. To start a new '
                'job, please stop the current one.')
            return

        with open(self.nexus_config_path, "r") as f:
            nexus_structure = f.read()

        # Initialise the write job.
        write_job = WriteJob(
            nexus_structure,
            "{0:%Y}-{0:%m}-{0:%d}_{0:%H}{0:%M}.nxs".format(datetime.now()),
            self.broker[0],
            datetime.now(),
        )

        start_handler = self.job_handler.start_job(write_job)
        self._set_job_id(write_job.job_id)

        while not start_handler.is_done():
            # TODO: timeout
            sleep(10)

        session.log.info(f'Writing job with ID {self.job_id} has started.')

    def doStop(self):
        self.log.warning("doStop")
        if not self.job_id:
            self.log.warning(
                "Cannot stop file-writer job because the ID is unknown")
            return

        stop_handler = self.job_handler.stop_now()

        while not stop_handler.is_done() and not self.job_handler.is_done():
            # TODO: timeout
            sleep(1)
        session.log.info(f'Writing job with ID {self.job_id} has stopped')
        self._set_job_id('')

    @requires(level=ADMIN)
    def reset_job_id(self, value=''):
        self._set_job_id(value)

    def _set_job_id(self, value):
        self._setROParam('job_id', value)


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
        'job_id': Param('Writer job identification',
                        type=str, mandatory=False, userparam=False,),
    }

    def set_job_id(self, val):
        self._setROParam('job_id', val)

    def get_job_id(self):
        return self.job_id
