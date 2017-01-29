from _socket import gethostbyname, socket, AF_INET, SOCK_DGRAM

from data_point import DataPoint


class SocketReceiver:
    """
    Producer in producer/consumer architecture.
    Receives data points from sender over socket connection and passes them to a consumer.
    """

    def __init__(self, port=80):
        self.port = port
        self.__stopped = True

    def set_listener(self, listener):
        self.listener = listener

    def start_listening(self):
        self.__stopped = False

        self.host_name = gethostbyname('0.0.0.0')
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind((self.host_name, self.port))

        print ("Test server listening on port {0}".format(self.port))

        while not self.__stopped:
            (data, addr) = self.sock.recvfrom(1024)
            # pass to consumer
            if not self.listener.on_sensor_data_changed(data):
                self.__stopped = True
                print("Stopping sensor reader")

    def stop(self):
        self.__stopped = True

    def is_stopped(self):
        return self.__stopped
