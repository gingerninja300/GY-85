from _socket import gethostbyname, socket, AF_INET, SOCK_DGRAM, SOCK_STREAM

from data_point import DataPoint


class SocketReceiver:
    """
    Producer in producer/consumer architecture.
    Receives data points from sender over socket connection and passes them to a consumer.
    """

    def __init__(self, port=5000):
        self.port = port
        self.__stopped = True

    def set_listener(self, listener):
        self.listener = listener

    def start_listening(self):
        self.__stopped = False

        self.host_name = gethostbyname('0.0.0.0')
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.host_name, self.port))

        self.sock.listen(1)
        conn, addr = self.sock.accept()

        print ("Test server listening on port {0}".format(self.port))

        while not self.__stopped:
            data = conn.recv(32768).decode("ascii")
            first = True
            last_truncated = None
            for line in data.split('\n'):
                if len(line) == 0:
                    continue
                decoded = DataPoint.from_str(line)
                if first:
                    first = False
                    if decoded:
                        print('Received and decoded, t={}'.format(decoded.time))
                if decoded is None:
                    # it might be none because sometimes the chunks that are received don't align with
                    # the samples that were read, so for a sample, only the first part might be included
                    # in the buffer and the rest of it in the next buffer
                    if last_truncated is None:
                        last_truncated = line
                        continue
                    else:
                        try:
                            decoded = DataPoint.from_str(last_truncated + line)
                        except ValueError:
                            decoded = None
                        # assert decoded is not None
                        last_truncated = None

                # pass to consumer
                if decoded and not self.listener.on_sensor_data_received(decoded):
                    self.__stopped = True
                    print("Stopping sensor reader")

    def stop(self):
        self.__stopped = True

    def is_stopped(self):
        return self.__stopped
