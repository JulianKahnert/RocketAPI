#!/usr/bin/env python3

from api import api
from api import critical
import argparse
import logging
from logging.handlers import RotatingFileHandler
import numpy as np
import os
import re
import sys
import time


# create logger with 'rocket'
logger = logging.getLogger('rocket')
logger.setLevel(logging.DEBUG)
# create path of log file
path = os.path.dirname(os.path.realpath(__file__)) + '/logs/session.log'
# rotating session logs: perform a rollover before the next session begins
fh = RotatingFileHandler(path, mode='a', backupCount=10)
fh.doRollover()
# create file handler which logs even debug messages
fh = RotatingFileHandler(path, mode='w', backupCount=10)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
sh = logging.StreamHandler(stream=sys.stdout)
sh.setLevel(logging.WARNING)
# create formatters and add them to the handlers
form_fh = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%H:%M:%S')
form_sh = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
fh.setFormatter(form_fh)
sh.setFormatter(form_sh)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(sh)

# set default pressure profiles
DefaultProfileA = np.array([[6, 4], [18, 9], [6, 5], [0, 0], [0, 0]])
DefaultProfileC = np.array([[20, 9], [10, 5], [0, 0], [0, 0], [0, 0]])
DefaultProfileB = np.array([[8, 4], [22, 9], [0, 0], [0, 0], [0, 0]])

class state:
    # BYTE 0: temperature unit
    __TemperatureUnit = ['Celsius', 'Fahrenheit']

    def _set_temperatureUnit(self, x):
        if x not in self.__TemperatureUnit:
            self._log.warning('"{}" is not valid. Choose one of: {}!'.format(x, self.__TemperatureUnit))
        else:
            self._api.write(0, self.__TemperatureUnit.index(x))

    temperatureUnit = property(
        fset=_set_temperatureUnit,
        fget=lambda self: self.__TemperatureUnit[self._api.read(0)],
        fdel=None,
        doc='Unit of temperature: Celsius/Fahrenheit')

    # BYTE 1: language
    __Language = ['English', 'German', 'French', 'Italian']

    def _set_language(self, x):
        if x not in self.__Language:
            self._log.warning('"{}" is not valid. Choose one of: {}!'.format(x, self.__Language))
        else:
            self._api.write(1, self.__Language.index(x))

    language = property(
        fset=_set_language,
        fget=lambda self: self.__Language[self._api.read(1)],
        fdel=None,
        doc='Selected language: English/German/French/Italian')

    # BYTE 2: coffee temperature
    # coffee boiler in degree Celsius
    __Coffee_temp_C = [85, 115]
    # coffee boiler in degree Fahrenheit
    __Coffee_temp_F = [185, 239]

    def _set_coffeeTemperature(self, x):
        unit = self.temperatureUnit
        if unit == 'Celsius':
            self._check_range(x, self.__Coffee_temp_C, 'Temperature ')
        elif unit == 'Fahrenheit':
            self._check_range(x, self.__Coffee_temp_F, 'Temperature ')
        else:
            self._log.error('Temperature unit has a wrong state "{}"'.format(unit))
            return
        self._api.write(2, x)

    coffeeTemperature = property(
        fset=_set_coffeeTemperature,
        fget=lambda self: self._api.read(2),
        fdel=None,
        doc='Temperature (in F or C) of coffee boiler: 85...115 °C')

    # BYTE 3: steam temperature
    # steam boiler in degree Celsius
    __Steam_temp_C = [115, 125]
    # steam boiler in degree Fahrenheit
    __Steam_temp_F = [239, 257]

    def _set_steamTemperature(self, x):
        unit = self.temperatureUnit
        if unit == 'Celsius':
            self._check_range(x, self.__Steam_temp_C, 'Temperature ')
        elif unit == 'Fahrenheit':
            self._check_range(x, self.__Steam_temp_F, 'Temperature ')
        else:
            self._log.error('Temperature unit has a wrong state "{}"'.format(unit))
            return
        self._api.write(3, x)

    steamTemperature = property(
        fset=_set_steamTemperature,
        fget=lambda self: self._api.read(3),
        fdel=None,
        doc='Temperature (in F or C) of steam boiler: 115...125 °C')

    # BYTE 4: coffeePID     # 4-5, 10-11, 16-17
    coffeePID = property(
        fset=None,
        fget=lambda self: self._read_PID(4),
        fdel=None,
        doc='')

    # BYTE 6: groupPID      # 6-7, 12-13, 18-19
    groupPID = property(
        fset=None,
        fget=lambda self: self._read_PID(6),
        fdel=None,
        doc='')

    # BYTE 8: mysteryPID    # 8-9, 14-15, 20-21
    mysteryPID = property(
        fset=None,
        fget=lambda self: self._read_PID(8),
        fdel=None,
        doc='')

    # BYTE 22: pressure profile A       # 22-36
    def _set_pressureA(self, profile):
        self._check_profile(profile)
        self._write_profile(22, profile)

    pressureA = property(
        fset=_set_pressureA,
        fget=lambda self: self._read_profile(22),
        fdel=None,
        doc='Pressure profile A - 5 times [seconds, bars]')

    # BYTE 38: pressure profile B       # 38-52
    def _set_pressureB(self, profile):
        self._check_profile(profile)
        self._write_profile(38, profile)

    pressureB = property(
        fset=_set_pressureB,
        fget=lambda self: self._read_profile(38),
        fdel=None,
        doc='Pressure profile B - 5 times [seconds, bars]')

    # BYTE 54: pressure profile C       # 54-68
    def _set_pressureC(self, profile):
        self._check_profile(profile)
        self._write_profile(54, profile)

    pressureC = property(
        fset=_set_pressureC,
        fget=lambda self: self._read_profile(54),
        fdel=None,
        doc='Pressure profile C - 5 times [seconds, bars]')

    # BYTE 70: water source
    __WaterSource = ['PlumbedIn', 'Tank']

    def _set_waterSource(self, x):
        if x not in self.__WaterSource:
            self._log.warning('"{}" is not valid. Choose one of: {}!'.format(x, self.__WaterSource))
        else:
            self._api.write(70, self.__WaterSource.index(x))

    waterSource = property(
        fset=_set_waterSource,
        fget=lambda self: self.__WaterSource[self._api.read(70)],
        fdel=None,
        doc='Selected water source: "plumbed in" or "tank"')

    # BYTE 71: active profile
    __ActiveProfile = ['A', 'B', 'C']

    def _set_activeProfile(self, x):
        if x not in self.__ActiveProfile:
            self._log.warning('"{}" is not valid. Choose one of: {}!'.format(x, self.__ActiveProfile))
        else:
            self._api.write(71, self.__ActiveProfile.index(x))

    activeProfile = property(
        fset=_set_activeProfile,
        fget=lambda self: self.__ActiveProfile[self._api.read(71)],
        fdel=None,
        doc='Selected profile for next run.')

    # BYTE 72: steam clean time
    steamCleanTime = property(
        fset=None,
        fget=lambda self: self._api.read(72),
        fdel=None,
        doc='')

    # BYTE 73: is service boiler on
    def _set_isServiceBoilerOn(self, x):
        if not isinstance(x, bool):
            self._log.warning('"{}" is not valid. Choose a boolean!'.format(x))
        else:
            self._api.write(73, x)

    isServiceBoilerOn = property(
        fset=_set_isServiceBoilerOn,
        fget=lambda self: self._api.read(73) == 1,
        fdel=None,
        doc='Status of steam (aka service) boiler: on/off')

    # BYTE 74: is machine in standby
    def _set_isMachineInStandby(self, x):
        if not isinstance(x, bool):
            self._log.warning('"{}" is not valid. Choose a boolean!'.format(x))
        else:
            self._api.write(74, x)

    isMachineInStandby = property(
        fset=_set_isMachineInStandby,
        fget=lambda self: self._api.read(74) == 1,
        fdel=None,
        doc='Standby mode of R60V: on/off')

    # BYTE 75: NOT TESTED coffee cycles subtotal   # 75-76
    coffeeCyclesSubtotal = property(
        fset=None,
        fget=lambda self: [self._api.read(75), self._api.read(76)],
        fdel=None,
        doc='')

    # BYTE 77: NOT TESTED coffee cycles total      # 77-80
    coffeeCyclesTotal = property(
        fset=None,
        fget=lambda self: [self._api.read(idx) for idx in range(77, 81)],
        fdel=None,
        doc='')

    # BYTE 81: NOT TESTED auto on time     # 81-82
    autoOnTime = property(
        fset=None,
        fget=lambda self: [self._api.read(81), self._api.read(82)],
        fdel=None,
        doc='')

    # BYTE 83: NOT TESTED auto standby time    # 83-84
    autoStandbyTime = property(
        fset=None,
        fget=lambda self: [self._api.read(83), self._api.read(84)],
        fdel=None,
        doc='')

    # BYTE 85: NOT TESTED auto skip day
    autoSkipDay = property(
        fset=None,
        fget=lambda self: self._api.read(85),
        fdel=None,
        doc='')

    def __init__(self, machine_ip='192.168.1.1', machine_port=1774):
        # create logger
        self._log = logging.getLogger('rocket.state')

        # check if RocketEspresso SSID is available
        if re.search('RocketEspresso', os.popen('iwlist wlan0 scan').read()) is not None:
            self._log.debug('SSID "RocketEspresso" found')
        else:
            critical(self._log, 'SSID "RocketEspresso" not found')

        # ip address from DHCP server of R60V?
        if os.popen('ifconfig | grep "192.168.1."').read():
            self._log.debug('ip address from DHCP server of R60V available')
        else:
            critical(self._log, 'no ip address from DHCP server of R60V available')

        # create connection to machine
        self._api = api(machine_ip=machine_ip, machine_port=machine_port)

    def __del__(self):
        self._log.info('run destructor')
        self._api.close()

    # ### helper functions ###
    def _check_range(self, selected, min_max, pre):
        if not(min_max[0] <= selected <= min_max[1]):
            critical(self._log, '{}value "{}" is out of range [{} ... {}]!'.format(
                pre, selected, min_max[0], min_max[1]))

    def _check_profile(self, profile):
        # set default values
        err = []
        bValid = True
        # (kind of) protected MIN/MAX values
        Pressure = [0, 14]  # bars
        Time = [0, 60]      # seconds
        # look at each of the 5 settings
        for num in range(5):
            # check temperature
            self._check_range(profile[num][0], Time, 'Time ')
            # check pressure
            self._check_range(profile[num][1], Pressure, 'Pressure ')

    def _read_profile(self, offset):
        profile = np.array([
            [self._api.read(offset + 0), self._api.read(offset + 10)],
            [self._api.read(offset + 2), self._api.read(offset + 11)],
            [self._api.read(offset + 4), self._api.read(offset + 12)],
            [self._api.read(offset + 6), self._api.read(offset + 13)],
            [self._api.read(offset + 8), self._api.read(offset + 14)]])
        self._log.info('received profile (offset={}): {}'.format(offset, profile))
        profile = profile / 10  # decisecond => second, decibar => bar
        return profile

    def _write_profile(self, offset, profile):
        p = np.array(profile) * 10
        self._api.write(offset + 0, p[0][0]), self._api.write(offset + 10, p[0][1])
        self._api.write(offset + 2, p[1][0]), self._api.write(offset + 11, p[1][1])
        self._api.write(offset + 4, p[2][0]), self._api.write(offset + 12, p[2][1])
        self._api.write(offset + 6, p[3][0]), self._api.write(offset + 13, p[3][1])
        self._api.write(offset + 8, p[4][0]), self._api.write(offset + 14, p[4][1])

    def _read_PID(self, offset):
        profile = np.array([
            self._api.read(offset + 0),
            self._api.read(offset + 6),
            self._api.read(offset + 12)])
        return profile

if __name__ == "__main__":
    # create logger and set level
    log = logging.getLogger('rocket.cli')
    # create console handler with a higher log level
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setLevel(logging.INFO)
    # create formatters and add them to the handlers
    form_sh = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(form_sh)
    # add the handlers to the logger
    log.addHandler(sh)

    parser = argparse.ArgumentParser(
        description='Command-line tool to read and write data from R60V.',
        epilog="""
List of all R60V properties and their possible values ([] means: not writable):
    * activeProfile             [A/B/C]
    * autoOnTime                []
    * autoSkipDay               []
    * autoStandbyTime           []
    * coffeeCyclesSubtotal      []
    * coffeeCyclesTotal         []
    * coffeePID                 []
    * coffeeTemperature         [105], e.g. 85...115 C or 185...239 F
    * groupPID                  []
    * isMachineInStandby        [True/False]
    * isServiceBoilerOn         [True/False]
    * language                  [English/German/French/Italian]
    * mysteryPID                []
    * pressureA                 default: [[ 6, 4], [18, 9], [6, 5], [0, 0], [0, 0]]
    * pressureB                 default: [[20, 9], [10, 5], [0, 0], [0, 0], [0, 0]]
    * pressureC                 default: [[ 8, 4], [22, 9], [0, 0], [0, 0], [0, 0]]
    * steamCleanTime            []
    * steamTemperature          [124], e.g. 115...125 C or 239...257 F
    * temperatureUnit           [Celsius/Fahrenheit]
    * waterSource               [PlumbedIn/Tank]

All pressure profiles contain 5 steps with [0...60 seconds, 0...14 bars] in decisecond/-bar precision.
        """,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-da', '--defaultA',
                        dest='defaultA',
                        action='store_true',
                        help='set pressure profile A to defaults')

    parser.add_argument('-db', '--defaultB',
                        dest='defaultB',
                        action='store_true',
                        help='set pressure profile B to defaults')

    parser.add_argument('-dc', '--defaultC',
                        dest='defaultC',
                        action='store_true',
                        help='set pressure profile C to defaults')

    parser.add_argument('-on', '--on',
                        dest='on',
                        action='store_true',
                        help='start the machine')

    parser.add_argument('-off', '--off',
                        dest='off',
                        action='store_true',
                        help='shut down the machine')

    parser.add_argument('-p', '--profile',
                        dest='profile',
                        action='store',
                        help='set active profile to A, B or C')

    parser.add_argument('-r', '--read',
                        dest='read',
                        action='store',
                        help='read machine state, see properties below')

    parser.add_argument('-s', '--set',
                        dest='setting',
                        nargs=2,
                        action='store',
                        help='change settings with a key-value pair, see properties below')

    args = parser.parse_args()

    # print help when script is called without any argument
    if len(sys.argv) < 2:
        parser.print_help()
        parser.exit(1)

    else:
        obj = state()
        time.sleep(0.2)
        if args.defaultA:
            log.info('Set pressure profile A to defaults:')
            log.info(DefaultProfileA)
            obj.pressureA = DefaultProfileA

        if args.defaultB:
            log.info('Set pressure profile B to defaults:')
            log.info(DefaultProfileB)
            obj.pressureB = DefaultProfileB

        if args.defaultC:
            log.info('Set pressure profile C to defaults:')
            log.info(DefaultProfileC)
            obj.pressureC = DefaultProfileC

        if args.on:
            log.info('Start the machine ...')
            obj.isMachineInStandby = False

        if args.off:
            log.info('Shutting down the machine ...')
            obj.isMachineInStandby = True

        if args.profile:
            log.info('Setting profile to "{}"'.format(args.profile))
            obj.activeProfile = args.profile

        if args.read:
            log.info('received: {} = {}'.format(args.read, getattr(obj, args.read)))

        if args.setting:
            prop = args.setting[0]
            val = args.setting[1]
            if prop in dir(state):
                if prop in ['coffeeTemperature', 'isMachineInStandby', 'isServiceBoilerOn', 'steamTemperature']:
                    val = int(val)
                log.info('Setting attribute "{}"" to "{}".'.format(prop, val))
                setattr(obj, args.setting[0], args.setting[1])
            else:
                log.error('ERROR: property not in machine state.')

        del obj
