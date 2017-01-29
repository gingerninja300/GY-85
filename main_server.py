from receiver import SocketReceiver
from sensor_printer import SensorPrinter
from sensor_reader import SensorReader


def start_loop_server(args):
    # sensor_reader = SensorReader(enabled_sensors=SensorReader.ACC)
    listener = SensorPrinter()
    # sensor_reader.set_sensor_listener(listener)

    receiver = SocketReceiver()
    receiver.set_listener(listener)
    receiver.start_listening()
