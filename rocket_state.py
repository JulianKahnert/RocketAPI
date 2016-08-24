#!/usr/bin/python

import copy


# parse DayOfWeek, Language, TemperatureUnit, WaterSource
Language = ['English', 'German', 'French', 'Italian']
DayOfWeek = ['Unknown', 'Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday', 'Sunday']
TemperatureUnit = ['Celsius', 'Fahrenheit']
WaterSource = ['PlumbedIn', 'Tank']

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
    currently possible states:
    * language
    * temperatureUnit
    * waterSource
    * pressureA
    * pressureB
    * pressureC
    """

    @property
    def coffeeCyclesSubtotal(self):
        return self._coffeeCyclesSubtotal

    @coffeeCyclesSubtotal.setter
    def coffeeCyclesSubtotal(self, x):
        print(x)
        print('Not writeable!?')

    @property
    def coffeeCyclesTotal(self):
        return self._coffeeCyclesTotal

    @coffeeCyclesTotal.setter
    def coffeeCyclesTotal(self, x):
        print('Not writeable!?')

    @property
    def pressureA(self):
        return self._pressureA

    @pressureA.setter
    def pressureA(self, profile):
        bValid, err = self._check_profile(profile)
        if bValid:
            self._pressureA = profile
        else:
            print(err)

    @property
    def pressureB(self):
        return self._pressureB

    @pressureB.setter
    def pressureB(self, profile):
        bValid, err = self._check_profile(profile)
        if bValid:
            self._pressureB = profile
        else:
            print(err)

    @property
    def pressureC(self):
        return self._pressureC

    @pressureC.setter
    def pressureC(self, profile):
        bValid, err = self._check_profile(profile)
        if bValid:
            self._pressureC = profile
        else:
            print(err)

    def __init__(self):
        """
        Setting default values...
        """
        self._coffeeCyclesSubtotal = []
        self._coffeeCyclesTotal = []

        # set default values
        self._pressureA = copy.deepcopy(Default_pressureA)
        self._pressureB = copy.deepcopy(Default_pressureB)
        self._pressureC = copy.deepcopy(Default_pressureC)
        self._activeProfile = 0

        self._language = 'German'
        self._isServiceBoilerOn = None
        self._isMachineInStandby = None
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

    def _check_range(self, temp, min_max):
        if temp < min_max[0] or temp > min_max[1]:
            bValid = False
            err = 'value "{}" is out of range [{} ... {}]!'.format(
                temp, min_max[0], min_max[1])
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
