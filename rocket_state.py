#!/usr/bin/python

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

    @property
    def coffeeCyclesSubtotal(self):
        return copy.deepcopy(self._coffeeCyclesSubtotal)

    @coffeeCyclesSubtotal.setter
    def coffeeCyclesSubtotal(self, x):
        print(x)
        print('Not writeable!?')

    @property
    def coffeeCyclesTotal(self):
        return copy.deepcopy(self._coffeeCyclesTotal)

    @coffeeCyclesTotal.setter
    def coffeeCyclesTotal(self, x):
        print('Not writeable!?')

    @property
    def pressureA(self):
        return copy.deepcopy(self._pressureA)

    @pressureA.setter
    def pressureA(self, profile):
        bValid, err = self._check_profile(profile)
        if bValid:
            self._pressureA = profile
        else:
            print(err)

    @property
    def pressureB(self):
        return copy.deepcopy(self._pressureB)

    @pressureB.setter
    def pressureB(self, profile):
        bValid, err = self._check_profile(profile)
        if bValid:
            self._pressureB = profile
        else:
            print(err)

    @property
    def pressureC(self):
        return copy.deepcopy(self._pressureC)

    @pressureC.setter
    def pressureC(self, profile):
        bValid, err = self._check_profile(profile)
        if bValid:
            self._pressureC = profile
        else:
            print(err)

    @property
    def activeProfile(self):
        return copy.deepcopy(self._activeProfile)

    @activeProfile.setter
    def activeProfile(self, x):
        if x in ActiveProfile:
            self._activeProfile = x
        else:
            print('"{}" is not valid. Choose one of: {}!'.format(x, ActiveProfile))

    @property
    def language(self):
        return copy.deepcopy(self._language)

    @language.setter
    def language(self, x):
        if x in Language:
            self._language = x
        else:
            print('"{}" is not valid. Choose one of: {}!'.format(x, Language))

    @property
    def isServiceBoilerOn(self):
        return copy.deepcopy(self._isServiceBoilerOn)

    @isServiceBoilerOn.setter
    def isServiceBoilerOn(self, x):
        if isinstance(x, bool):
            self._isServiceBoilerOn = x
        else:
            print('"{}" is not valid. Choose a bool!'.format(x))

    @property
    def isMachineInStandby(self):
        return copy.deepcopy(self._isMachineInStandby)

    @isMachineInStandby.setter
    def isMachineInStandby(self, x):
        if isinstance(x, bool):
            self._isMachineInStandby = x
        else:
            print('"{}" is not valid. Choose a bool!'.format(x))

    @property
    def waterSource(self):
        return copy.deepcopy(self._waterSource)

    @waterSource.setter
    def waterSource(self, x):
        if x in WaterSource:
            self._waterSource = x
        else:
            print('"{}" is not valid. Choose one of: {}!'.format(x, WaterSource))

    @property
    def temperatureUnit(self):
        return copy.deepcopy(self._temperatureUnit)

    @temperatureUnit.setter
    def temperatureUnit(self, x):
        if x in TemperatureUnit:
            self._temperatureUnit = x
        else:
            print('"{}" is not valid. Choose one of: {}!'.format(x, TemperatureUnit))

    @property
    def coffeeTemperature(self):
        return copy.deepcopy(self._coffeeTemperature)

    @coffeeTemperature.setter
    def coffeeTemperature(self, x):
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

    @property
    def steamTemperature(self):
        return copy.deepcopy(self._steamTemperature)

    @steamTemperature.setter
    def steamTemperature(self, x):
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

    @property
    def steamCleanTime(self):
        return copy.deepcopy(self._steamCleanTime)

    @steamCleanTime.setter
    def steamCleanTime(self, x):
        print('Not writeable!?')

    @property
    def coffeePID(self):
        return copy.deepcopy(self._coffeePID)

    @coffeePID.setter
    def coffeePID(self, x):
        print('Not writeable!?')

    @property
    def groupPID(self):
        return copy.deepcopy(self._groupPID)

    @groupPID.setter
    def groupPID(self, x):
        print('Not writeable!?')

    @property
    def mysteryPID(self):
        return copy.deepcopy(self._mysteryPID)

    @mysteryPID.setter
    def mysteryPID(self, x):
        print('Not writeable!?')

    @property
    def autoOnTime(self):
        return copy.deepcopy(self._autoOnTime)

    @autoOnTime.setter
    def autoOnTime(self, x):
        print('Not writeable!?')

    @property
    def autoStandbyTime(self):
        return copy.deepcopy(self._autoStandbyTime)

    @autoStandbyTime.setter
    def autoStandbyTime(self, x):
        print('Not writeable!?')

    @property
    def autoSkipDay(self):
        return copy.deepcopy(self._autoSkipDay)

    @autoSkipDay.setter
    def autoSkipDay(self, x):
        print('Not writeable!?')

    def __init__(self):
        """
        Setting default values...
        """
        self._coffeeCyclesSubtotal = []
        self._coffeeCyclesTotal = []

        # set default values
        self._pressureA = Default_pressureA
        self._pressureB = Default_pressureB
        self._pressureC = Default_pressureC
        self._activeProfile = 'A'

        self._language = 'German'
        self._isServiceBoilerOn = True
        self._isMachineInStandby = False
        self._waterSource = 'Tank'

        self._temperatureUnit = 'Celsius'
        self._coffeeTemperature = 105
        self._steamTemperature = 123
        self._steamCleanTime = []

        # PID vectors [proportional, integral, derivative]
        self._coffeePID = []
        self._groupPID = []
        self._mysteryPID = []

        self._autoOnTime = []
        self._autoStandbyTime = []
        self._autoSkipDay = []

    def evaluate_state(self):
        """
        Evaluate every setting...
        """
        # coffeeCyclesSubtotal
        # coffeeCyclesTotal

        # pressureA, pressureB, pressureC
        bValid, err = self._check_profile(self.pressureA)
        if not bValid:
            print(self.pressureA)
            print(err + ' Change to default.')
            self.pressureA = copy.deepcopy(Default_pressureA)

        bValid, err = self._check_profile(self.pressureB)
        if not bValid:
            print(self.pressureB)
            print(err + ' Change to default.')
            self.pressureB = copy.deepcopy(Default_pressureB)

        bValid, err = self._check_profile(self.pressureC)
        if not bValid:
            print(self.pressureC)
            print(err + ' Change to default.')
            self.pressureC = copy.deepcopy(Default_pressureC)

        # activeProfile

        # language
        if self.language not in Language:
            print('Selected lanuage not available! Change to default.')
            self.language = 'German'

        # isServiceBoilerOn
        # isMachineInStandby

        # waterSource
        if self.waterSource not in WaterSource:
            print('Selected water source not available! Change to default.')
            self.waterSource = 'Tank'

        # temperatureUnit
        if self.temperatureUnit not in TemperatureUnit:
            print('Selected temperature unit not available! Change to default.')
            self.temperatureUnit = 'Celsius'

        # coffeeTemperature
        if self.temperatureUnit == 'Celsius':
            bValid, err = self._check_range(self.coffeeTemperature,
                                            Coffee_temp_C)
        elif self.temperatureUnit == 'Fahrenheit':
            bValid, err = self._check_range(self.coffeeTemperature,
                                            Coffee_temp_F)
        if not bValid:
            print('Coffee boiler temperature ' + err + ' Change to default.')
            self.temperatureUnit = 'Celsius'
            self.coffeeTemperature = 105

        # steamTemperature
        if self.temperatureUnit == 'Celsius':
            bValid, err = self._check_range(self.steamTemperature,
                                            Steam_temp_C)
        elif self.temperatureUnit == 'Fahrenheit':
            bValid, err = self._check_range(self.steamTemperature,
                                            Steam_temp_F)
        if not bValid:
            print('Steam boiler temperature ' + err + ' Change to default.')
            self.temperatureUnit = 'Celsius'
            self.steamTemperature = 123

        # steamCleanTime
        # coffeePID
        # groupPID
        # mysteryPID
        # autoOnTime
        # autoStandbyTime
        # autoSkipDay

    # ### helper functions ###

    def _check_range(self, selected, min_max):
        if selected < min_max[0] or selected > min_max[1]:
            bValid = False
            err = 'value "{}" is out of range [{} ... {}]!'.format(
                selected, min_max[0], min_max[1])
        else:
            bValid = True
            err = ''
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


def f2c(self, f):
    c = (f - 32) * 5 / 9
    return round(c)


def c2f(self, c):
    f = (c * 9 / 5) + 32
    return round(f)
