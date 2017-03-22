import threading

from combined_sensor_printer import CombinedSensorPrinter
from receiver import SocketReceiver
from sensor_printer import SensorPrinter
from sensor_reader import SensorReader


def start_loop_server(args):
    combined = CombinedSensorPrinter()

    sensor_reader = SensorReader(enabled_sensors=SensorReader.ACC | SensorReader.GYR | SensorReader.COMP)
    sensor_reader.set_sensor_listener(combined)
    t = threading.Thread(target=sensor_reader.start_reading)
    t.start()

    receiver = SocketReceiver()
    receiver.set_listener(combined)
    receiver.start_listening()
