#!/usr/bin/python

import numpy as np

class R60V:
    def __init__():
        """
        Documentation would be nice...
        """
        print('constructor')

        # from MachineState.ts
        pressure = {'min': 0, 'max': 14.0}  # bars
        time = {'min': 0, 'max': 60.0}      # seconds
        # TBC: PressureProfiles
        temperature_unit = {'Celsius': 0, 'Fahrenheit': 1}
        water_source = {'PlumbedIn': 0, 'Tank': 1}

        # this might be protected!?
        coffee_temp_c = {'min':  85, 'max': 115}
        coffee_temp_f = {'min': 185, 'max': 239}
        steam_temp_c = {'min': 115, 'max': 125}
        steam_temp_f = {'min': 239, 'max': 257}

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
        print('open tcp connection, Port: 1774 !?')

    def close(self):
        """
        Documentation would be nice...
        """
        print('close tcp connection')

    def checksumming(self):
        """
        Documentation would be nice...
        """
        print('checksum data')

    def update(self):
        """
        Documentation would be nice...
        """
        print('update properties')
