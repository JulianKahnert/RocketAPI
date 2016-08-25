#!/usr/bin/env python3

import copy


# parse DayOfWeek, Language, TemperatureUnit, WaterSource
Language = ['English', 'German', 'French', 'Italian']
DayOfWeek = ['Unknown', 'Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday', 'Sunday']
TemperatureUnit = ['Celsius', 'Fahrenheit']
WaterSource = ['PlumbedIn', 'Tank']
ActiveProfile = ['A', 'B', 'C']

# (kind of) proteced MIN/MAX values
Pressure = [0, 14]     # bars
Time = [0, 60]     # seconds
# coffee boiler in degree celsius
Coffee_temp_C = [85, 115]
# coffee boiler in degree fahrenheit
Coffee_temp_F = [185, 239]
# steam boiler in degree celsius
Steam_temp_C = [115, 125]
# steam boiler in degree fahrenheit
Steam_temp_F = [239, 257]

# pressure profiles (5x2) = [seconds, bars]
Default_pressureA = [
    [6, 4],
    [18, 9],
    [6, 5],
    [0, 0],
    [0, 0]]
Default_pressureB = [
    [8, 4],
    [22, 9],
    [0, 0],
    [0, 0],
    [0, 0]]
Default_pressureC = [
    [20, 9],
    [10, 5],
    [0, 0],
    [0, 0],
    [0, 0]]


class machine_state:
    """
    Documentation would be nice ...
    """
    # DEFAULT PROPERTIES
    _coffeeCyclesSubtotal = []
    _coffeeCyclesTotal = []

    # set default values
    _pressureA = Default_pressureA
    _pressureB = Default_pressureB
    _pressureC = Default_pressureC
    _activeProfile = 'A'

    _language = 'German'
    _isServiceBoilerOn = True
    _isMachineInStandby = False
    _waterSource = 'Tank'

    _temperatureUnit = 'Celsius'
    _coffeeTemperature = 105
    _steamTemperature = 123
    _steamCleanTime = []

    # PID vectors [proportional, integral, derivative]
    _coffeePID = []
    _groupPID = []
    _mysteryPID = []

    _autoOnTime = []
    _autoStandbyTime = []
    _autoSkipDay = []

    # SETTER FUNCTIONS
    def _set_pressureA(self, profile):
        bValid, err = self._check_profile(profile)
        if bValid:
            self._pressureA = profile
        else:
            print(err)

    def _set_pressureB(self, profile):
        bValid, err = self._check_profile(profile)
        if bValid:
            self._pressureB = profile
        else:
            print(err)

    def _set_pressureC(self, profile):
        bValid, err = self._check_profile(profile)
        if bValid:
            self._pressureC = profile
        else:
            print(err)

    def _set_activeProfile(self, x):
        if x in ActiveProfile:
            self._activeProfile = x
        else:
            print('"{}" is not valid. Choose one of: {}!'.format(x, ActiveProfile))

    def _set_language(self, x):
        if x in Language:
            self._language = x
        else:
            print('"{}" is not valid. Choose one of: {}!'.format(x, Language))

    def _set_isServiceBoilerOn(self, x):
        if isinstance(x, bool):
            self._isServiceBoilerOn = x
        else:
            print('"{}" is not valid. Choose a bool!'.format(x))

    def _set_isMachineInStandby(self, x):
        if isinstance(x, bool):
            self._isMachineInStandby = x
        else:
            print('"{}" is not valid. Choose a bool!'.format(x))

    def _set_waterSource(self, x):
        if x in WaterSource:
            self._waterSource = x
        else:
            print('"{}" is not valid. Choose one of: {}!'.format(x, WaterSource))

    def _set_temperatureUnit(self, x):
        if x in TemperatureUnit:
            self._temperatureUnit = x
        else:
            print('"{}" is not valid. Choose one of: {}!'.format(x, TemperatureUnit))

    def _set_coffeeTemperature(self, x):
        if self.temperatureUnit == 'Celsius':
            bValid, err = self._check_range(x, Coffee_temp_C)
        elif self.temperatureUnit == 'Fahrenheit':
            bValid, err = self._check_range(x, Coffee_temp_F)
        else:
            bValid = False
            err = 'Unit has a wrong state "{}"'.format(self.temperatureUnit)

        if bValid:
            self._coffeeTemperature = x
        else:
            print('Temperature ' + err)

    def _set_steamTemperature(self, x):
        if self.temperatureUnit == 'Celsius':
            bValid, err = self._check_range(x, Steam_temp_C)
        elif self.temperatureUnit == 'Fahrenheit':
            bValid, err = self._check_range(x, Steam_temp_F)
        else:
            bValid = False
            err = 'unit has a wrong state "{}"'.format(self.temperatureUnit)

        if bValid:
            self._steamTemperature = x
        else:
            print('Temperature ' + err)

    # PROPERTY FUNCTIONS
    coffeeCyclesSubtotal = property(
        fget=lambda self: copy.deepcopy(self._coffeeCyclesSubtotal),
        fset=None,
        fdel=None,
        doc='')

    coffeeCyclesTotal = property(
        fget=lambda self: copy.deepcopy(self._coffeeCyclesTotal),
        fset=None,
        fdel=None,
        doc='')

    pressureA = property(
        fget=lambda self: copy.deepcopy(self._pressureA),
        fset=_set_pressureA,
        fdel=None,
        doc='Pressure profile A - 5 times [seconds, bars]')

    pressureB = property(
        fget=lambda self: copy.deepcopy(self._pressureB),
        fset=_set_pressureB,
        fdel=None,
        doc='Pressure profile B - 5 times [seconds, bars]')

    pressureC = property(
        fget=lambda self: copy.deepcopy(self._pressureC),
        fset=_set_pressureC,
        fdel=None,
        doc='Pressure profile C - 5 times [seconds, bars]')

    activeProfile = property(
        fget=lambda self: copy.deepcopy(self._activeProfile),
        fset=_set_activeProfile,
        fdel=None,
        doc='Selected profile for next run.')

    language = property(
        fget=lambda self: copy.deepcopy(self._language),
        fset=_set_language,
        fdel=None,
        doc='Selected language: English/German/French/Italian')

    isServiceBoilerOn = property(
        fget=lambda self: copy.deepcopy(self._isServiceBoilerOn),
        fset=_set_isServiceBoilerOn,
        fdel=None,
        doc='Status of steam (aka service) boiler: on/off')

    isMachineInStandby = property(
        fget=lambda self: copy.deepcopy(self._isMachineInStandby),
        fset=_set_isMachineInStandby,
        fdel=None,
        doc='Standby mode of R60V: on/off')

    waterSource = property(
        fget=lambda self: copy.deepcopy(self._waterSource),
        fset=_set_waterSource,
        fdel=None,
        doc='Status of steam (aka service) boiler: on/off')

    temperatureUnit = property(
        fget=lambda self: copy.deepcopy(self._temperatureUnit),
        fset=_set_temperatureUnit,
        fdel=None,
        doc='Unit of temperature: Celsius/Fahrenheit')

    coffeeTemperature = property(
        fget=lambda self: copy.deepcopy(self._coffeeTemperature),
        fset=_set_coffeeTemperature,
        fdel=None,
        doc='Temperature (in F or C) of coffee boiler: 85...115 °C')

    steamTemperature = property(
        fget=lambda self: copy.deepcopy(self._steamTemperature),
        fset=_set_steamTemperature,
        fdel=None,
        doc='Temperature (in F or C) of steam boiler: 115...125 °C')

    steamCleanTime = property(
        fget=lambda self: copy.deepcopy(self._steamCleanTime),
        fset=None,
        fdel=None,
        doc='')

    coffeePID = property(
        fget=lambda self: copy.deepcopy(self._coffeePID),
        fset=None,
        fdel=None,
        doc='')

    groupPID = property(
        fget=lambda self: copy.deepcopy(self._groupPID),
        fset=None,
        fdel=None,
        doc='')

    mysteryPID = property(
        fget=lambda self: copy.deepcopy(self._mysteryPID),
        fset=None,
        fdel=None,
        doc='')

    autoOnTime = property(
        fget=lambda self: copy.deepcopy(self._autoOnTime),
        fset=None,
        fdel=None,
        doc='')

    autoStandbyTime = property(
        fget=lambda self: copy.deepcopy(self._autoStandbyTime),
        fset=None,
        fdel=None,
        doc='')

    autoSkipDay = property(
        fget=lambda self: copy.deepcopy(self._autoSkipDay),
        fset=None,
        fdel=None,
        doc='')

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

    def _check_profile(self, profile):
        # set default values
        err = []
        bValid = True
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
