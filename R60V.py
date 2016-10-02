#!/usr/bin/env python3

from api import api
import argparse
import logging
from logging.handlers import RotatingFileHandler
import numpy as np
import os


# create logger with 'rocket'
logger = logging.getLogger('rocket')
logger.setLevel(logging.DEBUG)
# rotating session logs: perform a rollover before the next session begins
path = os.path.realpath(__file__).split(__file__)[0] + 'logs/session.log'
fh = RotatingFileHandler(path, mode='a', backupCount=10)                                                                                          
fh.doRollover()                                                                                                                                   
# create file handler which logs even debug messages
fh = RotatingFileHandler(path, mode='w', backupCount=10)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


class state:
    # BYTE 0: temperature unit
    TemperatureUnit = ['Celsius', 'Fahrenheit']
    
    def _set_temperatureUnit(self, x):
        if x not in self.TemperatureUnit:
            self.log.warning('"{}" is not valid. Choose one of: {}!'.format(x, self.TemperatureUnit))
        else:
            self.obj.write(0, self.TemperatureUnit.index(x))

    temperatureUnit = property(
        fset=_set_temperatureUnit,
        fget=lambda self: self.TemperatureUnit[self.obj.read(0)],
        fdel=None,
        doc='Unit of temperature: Celsius/Fahrenheit')

    # BYTE 1: language
    Language = ['English', 'German', 'French', 'Italian']
    
    def _set_language(self, x):
        if x not in self.Language:
            self.log.warning('"{}" is not valid. Choose one of: {}!'.format(x, self.Language))
        else:
            self.obj.write(1, self.Language.index(x))

    language = property(
        fset=_set_language,
        fget=lambda self: self.Language[self.obj.read(1)],
        fdel=None,
        doc='Selected language: English/German/French/Italian')

    # BYTE 2: coffee temperature
    # coffee boiler in degree celsius
    Coffee_temp_C = [85, 115]
    # coffee boiler in degree fahrenheit
    Coffee_temp_F = [185, 239]

    def _set_coffeeTemperature(self, x):
        if self.temperatureUnit == 'Celsius':
            bValid, err = self._check_range(x, self.Coffee_temp_C)
        elif self.temperatureUnit == 'Fahrenheit':
            bValid, err = self._check_range(x, self.Coffee_temp_F)
        else:
            bValid = False
            err = 'Unit has a wrong state "{}"'.format(self.temperatureUnit)

        if not bValid:
            self.log.warning('Temperature ' + err)
        else:
            self.obj.write(2, x)

    coffeeTemperature = property(
        fset=_set_coffeeTemperature,
        fget=lambda self: self.obj.read(2),
        fdel=None,
        doc='Temperature (in F or C) of coffee boiler: 85...115 °C')

    # BYTE 3: steam temperature
    # steam boiler in degree celsius
    Steam_temp_C = [115, 125]
    # steam boiler in degree fahrenheit
    Steam_temp_F = [239, 257]

    def _set_steamTemperature(self, x):
        if self.temperatureUnit == 'Celsius':
            bValid, err = self._check_range(x, self.Steam_temp_C)
        elif self.temperatureUnit == 'Fahrenheit':
            bValid, err = self._check_range(x, self.Steam_temp_F)
        else:
            bValid = False
            err = 'unit has a wrong state "{}"'.format(self.temperatureUnit)

        if not bValid:
            self.log.warning('Temperature ' + err)
        else:
            self.obj.write(3, x)

    steamTemperature = property(
        fset=_set_steamTemperature,
        fget=lambda self: self.obj.read(3),
        fdel=None,
        doc='Temperature (in F or C) of steam boiler: 115...125 °C')

    # BYTE 4: coffeePID     # 4-5, 10-11, 16-17
    coffeePID = property(
        fset=None,
        fget=None,
        fdel=None,
        doc='')

    # BYTE 6: groupPID      # 6-7, 12-13, 18-19
    groupPID = property(
        fset=None,
        fget=None,
        fdel=None,
        doc='')
    
    # BYTE 8: mysteryPID    # 8-9, 14-15, 20-21
    mysteryPID = property(
        fset=None,
        fget=None,
        fdel=None,
        doc='')

    # BYTE 22: pressure profile A       # 22-36
    def _set_pressureA(self, profile):
        bValid, err = self._check_profile(profile)
        if not bValid:
            self.log.warning(err)
        else:
            self._write_profile(22, profile)

    pressureA = property(
        fset=_set_pressureA,
        fget=lambda self: self._read_profile(22),
        fdel=None,
        doc='Pressure profile A - 5 times [seconds, bars]')
    # BYTE 38: pressure profile B       # 38-52
    # BYTE 54: pressure profile C       # 54-68
    
    # BYTE 70: water source
    WaterSource = ['PlumbedIn', 'Tank']
    
    def _set_waterSource(self, x):
        if x not in self.WaterSource:
            self.log.warning('"{}" is not valid. Choose one of: {}!'.format(x, self.WaterSource))
        else:
            self.obj.write(70, self.WaterSource.index(x))

    waterSource = property(
        fset=_set_waterSource,
        fget=lambda self: self.WaterSource[self.obj.read(70)],
        fdel=None,
        doc='Selected water source: "plumbed in" or "tank"')
    
    # BYTE 71: active profile
    ActiveProfile = ['A', 'B', 'C']

    def _set_activeProfile(self, x):
        if x not in self.ActiveProfile:
            self.log.warning('"{}" is not valid. Choose one of: {}!'.format(x, self.ActiveProfile))
        else:
            self.obj.write(71, self.ActiveProfile.index(x))
    
    activeProfile = property(
        fset=_set_activeProfile,
        fget=lambda self: self.ActiveProfile[self.obj.read(71)],
        fdel=None,
        doc='Selected profile for next run.')

    # BYTE 72: steam clean time
    # BYTE 73: is service boiler on
    def _set_isServiceBoilerOn(self, x):
        if not isinstance(x, bool):
            self.log.warning('"{}" is not valid. Choose a bool!'.format(x))
        else:
            self.obj.write(73, x)

    isServiceBoilerOn = property(
        fset=_set_isServiceBoilerOn,
        fget=lambda self: self.obj.read(73) == 1,
        fdel=None,
        doc='Status of steam (aka service) boiler: on/off')

    # BYTE 74: is machine in standby
    def _set_isMachineInStandby(self, x):
        if not isinstance(x, bool):
            self.log.warning('"{}" is not valid. Choose a bool!'.format(x))
        else:
            self.obj.write(74, x)            

    isMachineInStandby = property(
        fset=_set_isMachineInStandby,
        fget=lambda self: self.obj.read(74) == 1,
        fdel=None,
        doc='Standby mode of R60V: on/off')

    # BYTE 75: NOT TESTED coffee cycles subtotal   # 75-76
    coffeeCyclesSubtotal = property(
        fset=None,
        fget=lambda self: [self.obj.read(75), self.obj.read(76)],
        fdel=None,
        doc='')

    # BYTE 77: NOT TESTED coffee cycles total      # 77-80
    coffeeCyclesTotal = property(
        fset=None,
        fget=lambda self: [self.obj.read(idx) for idx in range(77, 81)],
        fdel=None,
        doc='')

    # BYTE 81: NOT TESTED auto on time     # 81-82
    autoOnTime = property(
        fset=None,
        fget=lambda self: [self.obj.read(81), self.obj.read(82)],
        fdel=None,
        doc='')

    # BYTE 83: NOT TESTED auto standby time    # 83-84
    autoStandbyTime = property(
        fset=None,
        fget=lambda self: [self.obj.read(83), self.obj.read(84)],
        fdel=None,
        doc='')

    # BYTE 85: NOT TESTED auto skip day
    autoSkipDay = property(
        fset=None,
        fget=lambda self: self.obj.read(85),
        fdel=None,
        doc='')


    # ### helper functions ###
    def __init__(self, machine_ip='192.168.1.1', machine_port=1774):
        # create logger
        self.logger = logging.getLogger('rocket.state')

        # create connection to machine
        self.obj = api(machine_ip=machine_ip, machine_port=machine_port)

    def __del__(self):
        del self.obj

    def _check_range(self, selected, min_max):
        if min_max[0] <= selected <= min_max[1]:
            bValid = True
            err = ''

        else:
            bValid = False
            err = 'value "{}" is out of range [{} ... {}]!'.format(
                selected, min_max[0], min_max[1])
            
        return bValid, err
    
    def _check_profile(self, profile):
        # set default values
        err = []
        bValid = True
        # (kind of) proteced MIN/MAX values
        Pressure = [0, 14]  # bars
        Time = [0, 60]      # seconds
        # look at each of the 5 settings
        for num in [0, 1, 2, 3, 4]:
            # check temperature
            bValid, err = self._check_range(profile[num][0], Time)
            if not bValid:
                err = 'Time ' + err
                break
            # check pressure
            bValid, err = self._check_range(profile[num][1], Pressure)
            if not bValid:
                err = 'Pressure ' + err
                break
        return bValid, err

    def _read_profile(self, offset):
        profile = []
        profile.append([self.obj.read(offset + 0), self.obj.read(offset + 10)])
        profile.append([self.obj.read(offset + 2), self.obj.read(offset + 11)])
        profile.append([self.obj.read(offset + 4), self.obj.read(offset + 12)])
        profile.append([self.obj.read(offset + 6), self.obj.read(offset + 13)])
        profile.append([self.obj.read(offset + 8), self.obj.read(offset + 14)])
        return np.array(profile) / 10

    def _write_profile(self, offset, profile):
        p = np.array(profile) * 10
        self.obj.write(offset + 0, p[0][0]), self.obj.write(offset + 10, p[0][1])
        self.obj.write(offset + 2, p[1][0]), self.obj.write(offset + 11, p[1][1])
        self.obj.write(offset + 4, p[2][0]), self.obj.write(offset + 12, p[2][1])
        self.obj.write(offset + 6, p[3][0]), self.obj.write(offset + 13, p[3][1])
        self.obj.write(offset + 8, p[4][0]), self.obj.write(offset + 14, p[4][1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Commandline tool to read and write data from R60V.')
    
    parser.add_argument('-on', '--on',
                        dest='on',
                        action='store_true',
                        help='start the machine')

    parser.add_argument('-off', '--off',
                        dest='off',
                        action='store_true',
                        help='shut down the machine')

    parser.add_argument('-r', '--read',
                        dest='read',
                        action='store',
                        help='read machine state')

    parser.add_argument('-s', '--set',
                        dest='setting',
                        nargs=2,
                        action='store',
                        help='change settings with a key-value pair')
    args = parser.parse_args()
    obj = state()
    if args.on:
        print('Start the machine ...')
        obj.isMachineInStandby = False

    if args.off:
        print('Shutting down the machine ...')
        obj.isMachineInStandby = True

    if args.read:
        print(getattr(obj, args.read))

    if args.setting:
        prop = args.setting[0]
        val = args.setting[1]
        if prop in dir(state):
            if prop in ['coffeeTemperature', 'isMachineInStandby', 'isServiceBoilerOn', 'steamTemperature']:
                val = int(val)
            print('Setting attribute "{}"" to "{}".'.format(prop, val))
            setattr(obj, args.setting[0], args.setting[1])
        else:
            print('ERROR: property not in machine state.')
    
    del obj