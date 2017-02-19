class SensorPrinter:
    """
    Simply prints samples that it receives
    """

    def __init__(self, tag):
        self.tag = tag

    def on_sensor_data_changed(self, reading):
        print(self.tag + ': ' + str(reading))

        return True
