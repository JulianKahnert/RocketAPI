#!/usr/bin/python

import numpy as np
import copy
import socket


class R60V:
    def __init__(self, machine_ip='192.168.1.1', machine_port=1774):
        """
        Documentation would be nice...
        """
        # connection to Rocket
        self.machine_ip = machine_ip
        self.machine_port = machine_port

    def send(self):
        """
        Documentation would be nice...
        """
        print('send data')

    def recieve(self):
        """
        Documentation would be nice...
        """
        print('get data')

    def parse(self):
        """
        Documentation would be nice...
        """
        print('python => bytes')

    def open(self):
        """
        Documentation would be nice...
        """
        message = self.cs_attach('r00000001')

        # from first connection attempt
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.machine_ip, self.machine_port))

        # DOUBLE CHECK THE REST:
        sock.write(message)

        conn, addr = sock.accept()
        print('Connection address:', addr)
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            print("received data:", data)
            conn.send(data)  # echo
        conn.close()

    def close(self):
        """
        Documentation would be nice...
        """
        print('close tcp connection')

    def update(self):
        """
        Documentation would be nice...
        """
        print('update properties')

    def checksum(self, raw):
        """
        CHECKSUM

        calculate function from:
        nodejs/src/protocol/Checksum.ts
        nodejs/src/protocol/Checksum.unit.ts
        """
        value = 0
        for sz in raw:
            value += ord(sz)
        value_hex = hex(value & 255)[2:].upper()
        if len(value_hex) < 2:
            value_hex = '0' + value_hex
        return value_hex

    def cs_attach(self, message):
        message += self.checksum(message)

    def cs_verify(self, raw):
        # checksum max length 2 digits!?
        message_actual = raw[:-2]
        cs_actual = raw[-2:]
        cs_expected = self.checksum(message_actual)

        return cs_actual == cs_expected


class machine_state:
    # (kind of) proteced MIN/MAX values
    __pressure = {'min': 0, 'max': 14}     # bars
    __time = {'min': 0, 'max': 60}     # seconds
    # coffee boiler in degree celsius
    __coffee_temp_c = {'min': 85, 'max': 115}
    # coffee boiler in degree fahrenheit
    __coffee_temp_f = {'min': 185, 'max': 239}
    # steam boiler in degree celsius
    __steam_temp_c = {'min': 115, 'max': 125}
    # steam boiler in degree fahrenheit
    __steam_temp_f = {'min': 239, 'max': 257}

    # parse DayOfWeek, Language, TemperatureUnit, WaterSource
    __DayOfWeek = {
        'Unknown': 0,
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6,
        'Sunday': 7}
    __Language = {
        'English': 0,
        'German': 1,
        'French': 2,
        'Italian': 3}
    __TemperatureUnit = {
        'Celsius': 0,
        'Fahrenheit': 1}
    __WaterSource = {
        'PlumbedIn': 0,
        'Tank': 1}

    # pressure profiles (5x2) = [seconds, bars]
    __default_pressure_profile_A = [
        [6, 4],
        [18, 9],
        [6, 5],
        [0, 0],
        [0, 0]]
    __default_pressure_profile_B = [
        [8, 4],
        [22, 9],
        [0, 0],
        [0, 0],
        [0, 0]],
    __default_pressure_profile_C = [
        [20, 9],
        [10, 5],
        [0, 0],
        [0, 0],
        [0, 0]]

    # ### METHODS ###

    def __init__(self):
        # set default values
        self._pressure_profile_A = self.__default_pressure_profile_A
        self._pressure_profile_B = self.__default_pressure_profile_B
        self._pressure_profile_C = self.__default_pressure_profile_C

    # ### pressure profile properties ###

    @property
    def pressure_profile_A(self):
        return copy.deepcopy(self._pressure_profile_A)

    @pressure_profile_A.setter
    def pressure_profile_A(self, profile):
        bValid, err = self.check_profile(profile)
        if not bValid:
            print(err)
        else:
            print('save')
            self._pressure_profile_A = profile

    @property
    def pressure_profile_B(self):
        return copy.deepcopy(self._pressure_profile_B)

    @pressure_profile_B.setter
    def pressure_profile_B(self, profile):
        bValid, err = self.check_profile(profile)
        if not bValid:
            print(err)
        else:
            print('save')
            self._pressure_profile_B = profile

    @property
    def pressure_profile_C(self):
        return copy.deepcopy(self._pressure_profile_C)

    @pressure_profile_C.setter
    def pressure_profile_C(self, profile):
        bValid, err = self.check_profile(profile)
        if not bValid:
            print(err)
        else:
            print('save')
            self._pressure_profile_C = profile

    # ### helper functions ###

    def check_profile(self, profile):
        # set default values
        err = []
        bValid = True
        # look at each of the 5 settings
        for num in np.arange(5):
            tmp = profile[num]
            if tmp[0] < self.__time['min'] or tmp[0] > self.__time['max']:
                err = 'Time values are out of range [{} ... {}s]!'.format(
                    self.__time['min'], self.__time['max'])
                bValid = False
                break

            elif tmp[1] < self.__pressure['min'] or tmp[1] > self.__pressure['max']:
                err = 'Pressure values are out of range [{} ... {}bar]!'.format(
                    self.__pressure['min'], self.__pressure['max'])
                bValid = False
                break

        return bValid, err
