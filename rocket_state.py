#!/usr/bin/python

import copy


# parse DayOfWeek, Language, TemperatureUnit, WaterSource
Language = ['English', 'German', 'French', 'Italian']
DayOfWeek = ['Unknown', 'Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday', 'Sunday']
TemperatureUnit = ['Celsius', 'Fahrenheit']
WaterSource = ['PlumbedIn', 'Tank']

# (kind of) proteced MIN/MAX values
Pressure = {'min': 0, 'max': 14}     # bars
Time = {'min': 0, 'max': 60}     # seconds
# coffee boiler in degree celsius
Coffee_temp_C = {'min': 85, 'max': 115}
# coffee boiler in degree fahrenheit
Coffee_temp_F = {'min': 185, 'max': 239}
# steam boiler in degree celsius
Steam_temp_C = {'min': 115, 'max': 125}
# steam boiler in degree fahrenheit
Steam_temp_F = {'min': 239, 'max': 257}

# pressure profiles (5x2) = [seconds, bars]
Default_pressure_profile_A = [
    [6, 4],
    [18, 9],
    [6, 5],
    [0, 0],
    [0, 0]]
Default_pressure_profile_B = [
    [8, 4],
    [22, 9],
    [0, 0],
    [0, 0],
    [0, 0]]
Default_pressure_profile_C = [
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

    def __init__(self):
        """
        Setting default values...
        """
        self.coffeeCyclesSubtotal = []
        self.coffeeCyclesTotal = []

        # set default values
        self.pressureA = copy.deepcopy(Default_pressure_profile_A)
        self.pressureB = copy.deepcopy(Default_pressure_profile_B)
        self.pressureC = copy.deepcopy(Default_pressure_profile_C)
        self.activeProfile = 0

        self.language = 'German'
        self.isServiceBoilerOn = None
        self.isMachineInStandby = None
        self.waterSource = 'Tank'

        self.temperatureUnit = 'Celsius'
        self.coffeeTemperature = 105
        self.steamTemperature = 123
        self.steamCleanTime = []

        # PID vectors [proportional, integral, derivative]
        self.coffeePID = []
        self.groupPID = []
        self.mysteryPID = []

        self.autoOnTime = []
        self.autoStandbyTime = []
        self.autoSkipDay = []

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
            self.pressureA = copy.deepcopy(Default_pressure_profile_A)

        bValid, err = self._check_profile(self.pressureB)
        if not bValid:
            print(self.pressureB)
            print(err + ' Change to default.')
            self.pressureB = copy.deepcopy(Default_pressure_profile_B)

        bValid, err = self._check_profile(self.pressureC)
        if not bValid:
            print(self.pressureC)
            print(err + ' Change to default.')
            self.pressureC = copy.deepcopy(Default_pressure_profile_C)

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
        if temp < min_max['min'] or temp > min_max['max']:
            bValid = False
            err = 'value "{}" is out of range [{} ... {}]!'.format(
                temp, min_max['min'], min_max['max'])
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
