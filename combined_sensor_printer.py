class CombinedSensorPrinter:
    """
    Combines sensor data it receives from two Pis. Should run on the server.
    """

    def on_sensor_data_changed(self, reading):
        """
        Call when data was read on the server
        """
        print('Server: ' + str(reading))

        return True

    def on_sensor_data_received(self, reading):
        """
        Call when data was received from the client
        """
        print('Client: ' + str(reading))

        return True
