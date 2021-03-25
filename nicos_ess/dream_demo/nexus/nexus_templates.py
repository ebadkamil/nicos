from nicos_ess.nexus import EventStream

dream_default = {
    "entry-01:NXentry": {
        "instrument:NXinstrument": {
            "ExtSensor1:NXsample": {
                "TEST_sampleEnv": EventStream(
                    "Motor_Topic",
                    "IOC:m2.RBV",
                    "localhost:9092",
                    mod="f142",
                    dtype="double",
                ),
            }
        }
    }
}


# template = {
#         "entry1:NXentry": {
#             "INST:NXinstrument": {
#                 "name": NXDataset("Instrument"),
#                 "detector:NXdetector": {
#                     "data": EventStream(topic="EventTopic", source="SrcName")
#                 },
#             },
#             "sample:NXsample": {
#                 "height": DeviceDataset('dev'),
#                 "property": DeviceDataset('dev', 'param', unit='K'),
#             },
#         }
#     }