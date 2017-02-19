import threading

from receiver import SocketReceiver
from sensor_printer import SensorPrinter
from sensor_reader import SensorReader


def start_loop_server(args):
    sensor_reader = SensorReader(enabled_sensors=SensorReader.ACC)
    sensor_reader.set_sensor_listener(SensorPrinter('Server'))
    t = threading.Thread(target=sensor_reader.start_reading)
    t.start()

    receiver = SocketReceiver()
    receiver.set_listener(SensorPrinter('Layton'))
    receiver.start_listening()