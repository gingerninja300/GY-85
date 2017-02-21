class CombinedSensorPrinter:
    """
    Combines sensor data it receives from two Pis. Should run on the server.

    IMPORTANT: Assumes that
    1) The values from the server arrive faster than the ones from the client
    2) The sampling rate on the server is faster than the one on the client
    3) acc on the server and both acc and emg on the client
    """

    def __init__(self):
        self.server_data = []
        self.last_client_acc_reading = None

    def on_sensor_data_changed(self, reading):
        """
        Call when data was read on the server
        """
        # print('Server: ' + str(reading))

        self.server_data.append(reading)

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

            # look for the latest acc reading on the server that is earlier than the client reading
            last_acc_reading_server = None

            for i in range(len(self.server_data) - 1, -1, -1):
                if self.server_data[i].time < client_reading.time and self.server_data[i].sensor_type == 'acc':
                    last_acc_reading_server = self.server_data[i]
                    break

            # print('Combined sample:\n\tServer acc: ' + str(last_acc_reading_server)
            #       + '\n\tClient acc: ' + str(self.last_client_acc_reading)
            #       + '\n\tClient emg: ' + str(client_reading))

        return True
