from socket import socket, AF_INET, SOCK_STREAM
import multiprocessing
from multiprocessing import Queue

stop = multiprocessing.Value("i", 0)


class SocketSender:
    """
    Concurrently sends sensor data to server
    """

    def __init__(self, nth_sample=1, server_name='192.168.43.95', port=5000):
        """

        :param nth_sample: Only every nth sample is sent. Use 1 to print every single sample.
        """

        self.server_name = server_name
        self.port = port

        # for multiprocessing
        self.__buffer = Queue()
        self.nth_sample = nth_sample

        # defining socket to commmunicate through
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        # testing connection
        self.server_socket.connect((self.server_name, self.port))

    def on_sensor_data_changed(self, data_point):
        """
        Passes data to the consumer (consumer/producer architecture). Runs on producer process.
        :returns If the sender has been stopped
        """

        global stop

        if stop.value != 0:
            return False
        else:
            self.__buffer.put(data_point)
            return True

    def _send_sample(self, sample):
        """
        :param sample: Send a DataPoint to the server
        :return:
        """

        self.server_socket.send(str(sample) + '\n')

    def start_send_loop(self):
        """
        Starts consumer loop that sends data points to the server. Runs on consumer process.
        """

        global stop
        stop.value = 0

        count = 0

        while True:
            # This obviously is a very naive implementation of the consumer (while loop instead of lock).
            # However, this already achieves the maximum sampling rate because the I2C communication with
            # the sensors is the bottleneck.
            if not self.__buffer.empty():
                data_point = self.__buffer.get()
                if count % self.nth_sample == 0:
                    self._send_sample(data_point)
                count += 1
