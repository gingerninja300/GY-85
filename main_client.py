from multiprocessing import Process

import sys
import argparse

import sender
from sender import SocketSender
from sensor_reader import SensorReader


def start_loop_client(args):
    sensor_reader = SensorReader(enabled_sensors=SensorReader.ACC | SensorReader.EMG | SensorReader.GYR | SensorReader.COMP)
    if args.nth is not None:
        socket_sender = SocketSender(args.nth)
    else:
        socket_sender = SocketSender()
    sensor_reader.set_sensor_listener(socket_sender)

    # Consumer/producer architecture: the SensorReader is the producer, reading data from sensors,
    # and the SocketSender is the consumer.
    # We use multiprocessing.Process instead of threading.Thread because the latter would also cause
    # the other thread to slow down due to Global Interpreter Lock.

    # reset this because sensor_reader.start_reading() might execute before sender.start_send_loop()
    sender.stop.value = 0
    process = Process(target=socket_sender.start_send_loop)
    process.start()

    sensor_reader.start_reading()
