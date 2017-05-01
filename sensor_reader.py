import random
import time
from adxl345.i2c import ADXL345
from data_point import DataPoint
from adc.adc import ADC
from hmc5883l.HMC5883L import HMC5883L
from itg3200.ITG3200 import ITG3200


class SensorReader:
    """
    Reads data from accelerometer, gyroscope and compass
    """

    ACC = 1
    GYR = 2
    COMP = 4
    EMG = 8
    PRESS = 16  # pressure sensor

    def __init__(self, enabled_sensors=ACC | GYR | COMP | EMG | PRESS):
        """

        :param enabled_sensors: Which sensor to read from (default all)
        """
        self.__stopped = True
        self.samples_per_sec = 0

        self.VERBOSE = True

        self.sensor_list = []

        if enabled_sensors & self.ACC:
            self.accelerometer = ADXL345(alternate=True)
            self.accelerometer.set_data_rate(800)
            self.accelerometer.set_range(16, True)
            self.sensor_list.append('acc')

        if enabled_sensors & self.GYR:
            self.gyroscope = ITG3200()
            self.sensor_list.append('gyr')

        if enabled_sensors & self.COMP:
            self.compass = HMC5883L()
            self.sensor_list.append('comp')

        if enabled_sensors & self.EMG:
            self.emg0 = ADC(0)
            self.emg1 = ADC(1)
            self.sensor_list.append('emg0')
            self.sensor_list.append('emg1')

        if enabled_sensors & self.PRESS:
            self.press0 = ADC(2)
            self.press1 = ADC(3)
            self.sensor_list.append('press0')
            self.sensor_list.append('press1')

    def set_sensor_listener(self, listener):
        self.listener = listener

    def start_reading(self):
        self.accelerometer.power_on()

        self.__stopped = False
        self.last_sec = self.current_sec()
        self.__samples_in_sec = 0
        self.started_ms = self.current_millis_frac()
        self.read_samples = 0

        while not self.__stopped:

            sensor = self.__sensor_to_read()
            if sensor == 'gyr':
                reading = self.__read_gyroscope()
            elif sensor == 'comp':
                reading = self.__read_compass()
            elif sensor == 'acc':
                reading = self.__read_accelerometer()
            elif sensor == 'emg0':
                reading = self.__read_emg_0()
            elif sensor == 'emg1':
                reading = self.__read_emg_1()
            elif sensor == 'press0':
                reading = self.__read_pressure_0()
            else:
                reading = self.__read_pressure_1()

            curr_sec = self.current_sec()
            if self.last_sec != curr_sec:
                secs = curr_sec - self.last_sec
                if self.VERBOSE:
                    print('Samples read: ' + str(
                        self.read_samples) + ' (samples/sec: ' +
                          str(self.samples_per_sec) + ")")
                self.samples_per_sec = self.__samples_in_sec / secs
                self.__samples_in_sec = 0
                self.last_sec = curr_sec

            self.__samples_in_sec += 1

            self.read_samples += 1

            # pass to consumer
            if not self.listener.on_sensor_data_changed(reading):
                self.__stopped = True
                print("Stopping sensor reader")

    def __read_accelerometer(self):
        acc_reading = DataPoint()
        acc_reading.sensor_type = 'acc'
        acc = self.accelerometer.read_data()
        acc_reading.x = acc[0]
        acc_reading.y = acc[1]
        acc_reading.z = acc[2]
        acc_reading.time = time.time()
        return acc_reading

    def __read_emg_0(self):
        reading = DataPoint()
        reading.sensor_type = 'emg0'
        reading.x = self.emg0.read_adc()
        reading.time = time.time()
        return reading

    def __read_emg_1(self):
        reading = DataPoint()
        reading.sensor_type = 'emg1'
        reading.x = self.emg1.read_adc()
        reading.time = time.time()
        return reading

    def __read_pressure_0(self):
        reading = DataPoint()
        reading.sensor_type = 'press0'
        reading.x = self.press0.read_adc()
        reading.time = time.time()
        print(reading)
        return reading

    def __read_pressure_1(self):
        reading = DataPoint()
        reading.sensor_type = 'press1'
        reading.x = self.press1.read_adc()
        reading.time = time.time()
        print(reading)
        return reading

    def __read_gyroscope(self):
        gyr_reading = DataPoint()
        gyr_reading.sensor_type = 'gyr'
        gyr = self.gyroscope.read_data()
        gyr_reading.x = gyr[0]
        gyr_reading.y = gyr[1]
        gyr_reading.z = gyr[2]
        gyr_reading.time = time.time()
        return gyr_reading

    def __read_compass(self):
        comp_reading = DataPoint()
        comp_reading.sensor_type = 'comp'
        comp = self.compass.read_data()
        comp_reading.x = comp[0]
        comp_reading.y = comp[1]
        comp_reading.z = comp[2]
        comp_reading.time = time.time()
        return comp_reading

    def __sensor_to_read(self):
        """

        :return: Which sensor to read from in the current iteration (based on read_samples)
        """
        remainder = self.read_samples % len(self.sensor_list)
        return self.sensor_list[remainder]

    @staticmethod
    def current_millis_frac():
        return time.time() * 1000

    def current_sec(self):
        return int(round(time.time()))

    def stop(self):
        self.__stopped = True

    def is_stopped(self):
        return self.__stopped
