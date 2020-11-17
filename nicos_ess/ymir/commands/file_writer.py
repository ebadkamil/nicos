from nicos.commands import helparglist, usercommand
from file_writer_control.WorkerCommandChannel import WorkerCommandChannel
from file_writer_control.WriteJob import WriteJob
from file_writer_control.JobHandler import JobHandler
from datetime import datetime, timedelta

import time
import os
import json

nexus_structure = json.dumps({
  "children": [
    {
      "type": "group",
      "name": "entry-01",
      "attributes": {
        "NX_class": "NXentry"
      },
      "children": [
        {
          "type": "group",
          "name": "m1_RBV",
          "children": [
            {
              "type": "stream",
              "stream": {
                "topic": "Ymir_motion",
                "source": "SES-SCAN:MC-MCU-001:m1.RBV",
                "writer_module": "f142"
              }
            }
          ]
        },
        {
          "type": "group",
          "name": "m2_RBV",
          "children": [
            {
              "type": "stream",
              "stream": {
                "topic": "Ymir_motion",
                "source": "SES-SCAN:MC-MCU-001:m2.RBV",
                "writer_module": "f142"
              }
            }
          ]
        },
        {
          "type": "group",
          "name": "m3_RBV",
          "children": [
            {
              "type": "stream",
              "stream": {
                "topic": "Ymir_motion",
                "source": "SES-SCAN:MC-MCU-001:m3.RBV",
                "writer_module": "f142"
              }
            }
          ]
        },
        {
          "type": "group",
          "name": "freia_events",
          "children": [
            {
              "type": "stream",
              "stream": {
                "topic": "FREIA_detector",
                "source": "multiblade",
                "writer_module": "ev42"
              }
            }
          ]
        }
      ]
    }
  ]
}
)


def _prepare_write_job(host, topic, config, start_time):
    command_channel = WorkerCommandChannel(f'{host}/{topic}')
    job_handler = JobHandler(worker_finder=command_channel)
    # with open(config, "r") as f:
    #     nexus_structure = f.read()
    write_job = WriteJob(
        nexus_structure,
        "{0:%Y}-{0:%m}-{0:%d}_{0:%H}{0:%M}.nxs".format(start_time),
        host,
        start_time,
    )
    return job_handler, write_job


@usercommand
@helparglist(['kafka_host', 'nxs_config'])
def start_writing(kafka_host='dmsc-kafka01:9092', topic='UTGARD_writerCommand',
                  nxs_config=None):

    if nxs_config is None:
        # This path will most likely will change. It should be more
        # general anyway.
        config = os.path.join(os.getcwd(),
                              'nicos_ess/ymir/commands/nexus_config.json')
    else:
        config = nxs_config

    if topic == '':
        raise ValueError('Please provide a valid topic.')

    _time = datetime.now()
    handler, job = _prepare_write_job(kafka_host, topic, config, _time)

    print("Starting write job")
    start_handler = handler.start_job(job)
    while not start_handler.is_done():
        time.sleep(1)
    stop_time = _time + timedelta(seconds=60)
    stop_handler = handler.set_stop_time(stop_time)
    while not stop_handler.is_done():
        time.sleep(1)
    while not handler.is_done():
        time.sleep(1)
    print("Write job is done")


def stop_writing():
    pass
