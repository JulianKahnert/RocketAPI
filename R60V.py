#!/usr/bin/env python3

import socket
import time


class api:
    def __init__(self, machine_ip='192.168.1.1', machine_port=1774):
        """
        Contructor
        """
        # connection to Rocket
        self.machine_ip = machine_ip
        self.machine_port = machine_port

        self.buffer_size = 128

        # establishing the connection
        self.s = socket.create_connection((self.machine_ip, self.machine_port), 10)

        # get first "hello" from machine
        print(self.s.recv(self.buffer_size))

        # waiting time seems to be important here
        time.sleep(1)

    def __del__(self):
        """
        Destructor
        """
        self.s.close()

    def read(self, idx):
        """
        Read data
        """
        # generate message
        request = self._cs_attach('r' + format(idx, '04X') + format(1, '04X'))
        request = bytes(request, 'utf-8')
        
        # send request
        #print('-> {}'.format(request))
        self.s.send(request)

        # recieve data
        raw = self.s.recv(self.buffer_size)
        #print('<- {}'.format(raw))

        # get date from message
        if self._cs_verify(raw):
            # cut request and checksum
            data = raw.split(request[:-2])[1][:-2]
            value = int(data, 16)
        else:
            print('ERROR IN CHECKSUM!')
            value = []

        # not very nice, but more reliable:
        time.sleep(0.1)

        return value

    def write(self, idx, value):
        """
        write data on machine...
        """
        ## off
        ## request = self._cs_attach('w' + format(idx, '04X') + format(1, '04X') + '01')
        ## on
        ## request = self._cs_attach('w' + format(idx, '04X') + format(1, '04X') + '00')
        
        # create request
        request = self._cs_attach('w' + format(idx, '04X') + format(1, '04X') + format(value, '02X'))
        request = bytes(request, 'utf-8')

        # send request
        self.s.send(request)

    def _checksum(self, raw):
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

    def _cs_attach(self, message_tmp):
        message_tmp += self._checksum(message_tmp)
        return message_tmp

    def _cs_verify(self, raw):
        raw = raw.decode('utf-8')
        # checksum max length 2 digits
        message_actual = raw[:-2]
        cs_actual = raw[-2:]
        cs_expected = self._checksum(message_actual)

        return cs_actual == cs_expected



class state:
    # create connection to machine
    obj = api(machine_ip='192.168.1.1', machine_port=1774)


    # BYTE 0: temperature unit
    TemperatureUnit = ['Celsius', 'Fahrenheit']
    
    def _set_temperatureUnit(self, x):
        if x not in self.TemperatureUnit:
            print('"{}" is not valid. Choose one of: {}!'.format(x, self.TemperatureUnit))
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
            print('"{}" is not valid. Choose one of: {}!'.format(x, self.Language))
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
            print('Temperature ' + err)
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
            print('Temperature ' + err)
        else:
            self.obj.write(3, x)

    steamTemperature = property(
        fset=_set_steamTemperature,
        fget=lambda self: self.obj.read(3),
        fdel=None,
        doc='Temperature (in F or C) of steam boiler: 115...125 °C')

    # BYTE 4: xxPID     # 4-5, 10-11, 16-17
    # BYTE 6: xxPID     # 6-7, 12-13, 18-19
    # BYTE 8: xxPID     # 8-9, 14-15, 20-21
    # BYTE 22: pressure profile A       # 22-36
    # BYTE 38: pressure profile B       # 38-52
    # BYTE 54: pressure profile C       # 54-68
    
    # BYTE 70: water source
    WaterSource = ['PlumbedIn', 'Tank']
    
    def _set_waterSource(self, x):
        if x not in self.WaterSource:
            print('"{}" is not valid. Choose one of: {}!'.format(x, self.WaterSource))
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
            print('"{}" is not valid. Choose one of: {}!'.format(x, self.ActiveProfile))
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
            print('"{}" is not valid. Choose a bool!'.format(x))
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
            print('"{}" is not valid. Choose a bool!'.format(x))
        else:
            self.obj.write(74, x)            

    isMachineInStandby = property(
        fset=_set_isMachineInStandby,
        fget=lambda self: self.obj.read(74) == 1,
        fdel=None,
        doc='Standby mode of R60V: on/off')

    # BYTE 75: coffee cycles subtotal   # 75-76
    # BYTE 77: coffee cycles total      # 77-80
    # BYTE 81: auto on time     # 81-82
    # BYTE 83: auto standby time    # 83-84
    # BYTE 85: auto skip day


    # ### helper functions ###

    def _check_range(self, selected, min_max):
        if min_max[0] <= selected <= min_max[1]:
            bValid = True
            err = ''

        else:
            bValid = False
            err = 'value "{}" is out of range [{} ... {}]!'.format(
                selected, min_max[0], min_max[1])
            
        return bValid, err

