from data_point import DataPoint


class CombinedSensorPrinter:
    """
    Combines sensor data it receives from two Pis. Should run on the server.

    IMPORTANT: Assumes that
    1) The values from the server arrive faster than the ones from the client
    2) The sampling rate on the server is faster than the one on the client
    3) acc on the server and both acc and emg on the client
    """

    def __init__(self):
        self.server_acc = []
        self.server_i = 0
        self.last_client_acc_reading = None
        self.f = open('combined_out.txt', 'w')

    def on_sensor_data_changed(self, reading):
        """
        Call when data was read on the server
        """

        assert reading.sensor_type == 'acc'

        # print('Server: ' + str(reading))

        self.server_acc.append(reading)

        return True

    def on_sensor_data_received(self, client_reading):
        """
        Call when data was received from the client
        """
        # print('Client: ' + str(reading))

        if client_reading.sensor_type == 'acc':
            self.last_client_acc_reading = client_reading
        else:
            if self.last_client_acc_reading is None:
                return True

            # look for the latest acc reading on the server that is earlier than the client reading.
            # note that the last server reading could be used multiple times, but that's unlikely since
            # the sampling rate on the server is much higher
            last_acc_reading_server = None

            # average values of skipped accelerometer points
            skipped_acc_sum = DataPoint()
            skipped_acc_i = 0

            while self.server_i < len(self.server_acc):
                if self.server_acc[self.server_i].time > client_reading.time:
                    if self.server_i > 0:
                        last_acc_reading_server = self.server_acc[self.server_i - 1]
                    break
                elif self.server_i == len(self.server_acc) - 1:
                    last_acc_reading_server = self.server_acc[self.server_i]
                    skipped_acc_sum.x += self.server_acc[self.server_i].x
                    skipped_acc_sum.y += self.server_acc[self.server_i].y
                    skipped_acc_sum.z += self.server_acc[self.server_i].z
                    skipped_acc_i += 1
                else:
                    skipped_acc_sum.x += self.server_acc[self.server_i].x
                    skipped_acc_sum.y += self.server_acc[self.server_i].y
                    skipped_acc_sum.z += self.server_acc[self.server_i].z
                    skipped_acc_i += 1

                self.server_i += 1

            # algorithm should always find last reading unless server data is empty
            # but sometimes doesn't, that's why this line is commented out haha
            # assert len(self.server_acc) == 0 or last_acc_reading_server is not None

            if last_acc_reading_server is not None:
                if skipped_acc_i != 0:
                    last_acc_reading_server.x = skipped_acc_sum.x / float(skipped_acc_i)
                    last_acc_reading_server.y = skipped_acc_sum.y / float(skipped_acc_i)
                    last_acc_reading_server.z = skipped_acc_sum.z / float(skipped_acc_i)

                s = 'Combined sample:\n\tServer acc: ' + str(last_acc_reading_server) \
                    + '\n\tClient acc: ' + str(self.last_client_acc_reading) \
                    + '\n\tClient emg: ' + str(client_reading)

                self.f.write(s + '\n')

        return True
