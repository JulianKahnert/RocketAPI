#!/usr/bin/env python3

import unittest
import copy
import random
from rocket_state import machine_state

# import static variables from rocket_state.py
from rocket_state import Language
from rocket_state import DayOfWeek
from rocket_state import TemperatureUnit
from rocket_state import WaterSource
from rocket_state import ActiveProfile
from rocket_state import Pressure
from rocket_state import Time
from rocket_state import Coffee_temp_C
from rocket_state import Coffee_temp_F
from rocket_state import Steam_temp_C
from rocket_state import Steam_temp_F

Default_profile = [[6, 4], [18, 9], [6, 5], [0, 0], [0, 0]]


class test_R60V(unittest.TestCase):
    # def test_coffeeCyclesSubtotal(self):
    # def test_coffeeCyclesTotal(self):

    def test_pressureA_min(self):
        state = machine_state()

        # time
        old = state.pressureA
        tmp = copy.deepcopy(old)
        tmp[random.randint(0, len(tmp) - 1)][0] = Time[0] - 1
        state.pressureA = tmp
        new = state.pressureA
        self.assertEqual(old, new)

        # pressure
        old = state.pressureA
        tmp = copy.deepcopy(old)
        tmp[random.randint(0, len(tmp) - 1)][0] = Pressure[0] - 1
        state.pressureA = tmp
        new = state.pressureA
        self.assertEqual(old, new)

    def test_pressureA_max(self):
        state = machine_state()

        # time
        old = state.pressureA
        tmp = copy.deepcopy(old)
        tmp[random.randint(0, len(tmp) - 1)][0] = Time[1] + 1
        state.pressureA = tmp
        new = state.pressureA
        self.assertEqual(old, new)

        # pressure
        old = state.pressureA
        tmp = copy.deepcopy(old)
        tmp[random.randint(0, len(tmp) - 1)][1] = Pressure[1] + 1
        state.pressureA = tmp
        new = state.pressureA
        self.assertEqual(old, new)

    def test_pressureB_min(self):
        state = machine_state()

        # time
        old = state.pressureB
        tmp = copy.deepcopy(old)
        tmp[random.randint(0, len(tmp) - 1)][0] = Time[0] - 1
        state.pressureB = tmp
        new = state.pressureB
        self.assertEqual(old, new)

        # pressure
        old = state.pressureB
        tmp = copy.deepcopy(old)
        tmp[random.randint(0, len(tmp) - 1)][0] = Pressure[0] - 1
        state.pressureB = tmp
        new = state.pressureB
        self.assertEqual(old, new)

    def test_pressureB_max(self):
        state = machine_state()

        # time
        old = state.pressureB
        tmp = copy.deepcopy(old)
        tmp[random.randint(0, len(tmp) - 1)][0] = Time[1] + 1
        state.pressureB = tmp
        new = state.pressureB
        self.assertEqual(old, new)

        # pressure
        old = state.pressureB
        tmp = copy.deepcopy(old)
        tmp[random.randint(0, len(tmp) - 1)][1] = Pressure[1] + 1
        state.pressureB = tmp
        new = state.pressureB
        self.assertEqual(old, new)

    def test_pressureC_min(self):
        state = machine_state()

        # time
        old = state.pressureC
        tmp = copy.deepcopy(old)
        tmp[random.randint(0, len(tmp) - 1)][0] = Time[0] - 1
        state.pressureC = tmp
        new = state.pressureC
        self.assertEqual(old, new)

        # pressure
        old = state.pressureC
        tmp = copy.deepcopy(old)
        tmp[random.randint(0, len(tmp) - 1)][0] = Pressure[0] - 1
        state.pressureC = tmp
        new = state.pressureC
        self.assertEqual(old, new)

    def test_pressureC_max(self):
        state = machine_state()

        # time
        old = state.pressureC
        tmp = copy.deepcopy(old)
        tmp[random.randint(0, len(tmp) - 1)][0] = Time[1] + 1
        state.pressureC = tmp
        new = state.pressureC
        self.assertEqual(old, new)

        # pressure
        old = state.pressureC
        tmp = copy.deepcopy(old)
        tmp[random.randint(0, len(tmp) - 1)][1] = Pressure[1] + 1
        state.pressureC = tmp
        new = state.pressureC
        self.assertEqual(old, new)

    def test_activeProfile(self):
        state = machine_state()
        old = state.activeProfile
        for tmp in ['D', random.randint(0, 100)]:
            state.activeProfile = tmp
            new = state.activeProfile
            self.assertEqual(old, new)

    def test_activeProfile_possilble(self):
        state = machine_state()
        for tmp in ActiveProfile:
            state.activeProfile = tmp
            new = state.activeProfile
            self.assertEqual(tmp, new)

    def test_language(self):
        state = machine_state()
        old = state.language
        for tmp in ['test_lang', random.randint(0, 100)]:
            state.language = tmp
            new = state.language
            self.assertEqual(old, new)

    def test_language_possilble(self):
        state = machine_state()
        for tmp in Language:
            state.language = tmp
            new = state.language
            self.assertEqual(tmp, new)

    def test_isServiceBoilerOn(self):
        state = machine_state()
        old = state.isServiceBoilerOn
        for tmp in ['test_lang', random.randint(0, 100)]:
            state.isServiceBoilerOn = tmp
            new = state.isServiceBoilerOn
            self.assertEqual(old, new)

    def test_isServiceBoilerOn_possilble(self):
        state = machine_state()
        for tmp in [True, False]:
            state.isServiceBoilerOn = tmp
            new = state.isServiceBoilerOn
            self.assertEqual(tmp, new)

    def test_isMachineInStandby(self):
        state = machine_state()
        old = state.isMachineInStandby
        for tmp in ['test_lang', random.randint(0, 100)]:
            state.isMachineInStandby = tmp
            new = state.isMachineInStandby
            self.assertEqual(old, new)

    def test_isMachineInStandby_possilble(self):
        state = machine_state()
        for tmp in [True, False]:
            state.isMachineInStandby = tmp
            new = state.isMachineInStandby
            self.assertEqual(tmp, new)

    def test_waterSource(self):
        state = machine_state()
        old = state.waterSource
        for tmp in ['test_lang', random.randint(0, 100)]:
            state.waterSource = tmp
            new = state.waterSource
            self.assertEqual(old, new)

    def test_waterSource_possilble(self):
        state = machine_state()
        for tmp in WaterSource:
            state.waterSource = tmp
            new = state.waterSource
            self.assertEqual(tmp, new)

    def test_temperatureUnit(self):
        state = machine_state()
        old = state.temperatureUnit
        for tmp in ['test_lang', random.randint(0, 100)]:
            state.temperatureUnit = tmp
            new = state.temperatureUnit
            self.assertEqual(old, new)

    def test_temperatureUnit_possilble(self):
        state = machine_state()
        for tmp in TemperatureUnit:
            state.temperatureUnit = tmp
            new = state.temperatureUnit
            self.assertEqual(tmp, new)

    def test_coffeeTemperature_min(self):
        state = machine_state()
        old = state.coffeeTemperature
        tmp = copy.deepcopy(old)

        if state.temperatureUnit == 'Celsius':
            tmp = Coffee_temp_C[0] - 1
        elif state.temperatureUnit == 'Fahrenheit':
            tmp = Coffee_temp_F[0] - 1

        state.coffeeTemperature = tmp
        new = state.coffeeTemperature
        self.assertEqual(old, new)

    def test_coffeeTemperature_max(self):
        state = machine_state()
        old = state.coffeeTemperature
        tmp = copy.deepcopy(old)

        if state.temperatureUnit == 'Celsius':
            tmp = Coffee_temp_C[1] + 1
        elif state.temperatureUnit == 'Fahrenheit':
            tmp = Coffee_temp_F[1] + 1

        state.coffeeTemperature = tmp
        new = state.coffeeTemperature
        self.assertEqual(old, new)

    def test_steamTemperature_min(self):
        state = machine_state()
        old = state.steamTemperature
        tmp = copy.deepcopy(old)

        if state.temperatureUnit == 'Celsius':
            tmp = Steam_temp_C[0] - 1
        elif state.temperatureUnit == 'Fahrenheit':
            tmp = Steam_temp_F[0] - 1

        state.steamTemperature = tmp
        new = state.steamTemperature
        self.assertEqual(old, new)

    def test_steamTemperature_max(self):
        state = machine_state()
        old = state.steamTemperature
        tmp = copy.deepcopy(old)

        if state.temperatureUnit == 'Celsius':
            tmp = Steam_temp_C[1] + 1
        elif state.temperatureUnit == 'Fahrenheit':
            tmp = Steam_temp_F[1] + 1

        state.steamTemperature = tmp
        new = state.steamTemperature
        self.assertEqual(old, new)

    # def test_steamCleanTime(self):
    # def test_coffeePID(self):
    # def test_groupPID(self):
    # def test_mysteryPID(self):

    # def test_autoOnTime(self):
    #     old =
    #     new =
    #     self.assertEqual(old, new)

    # def test_autoStandbyTime(self):
    #     old =
    #     new =
    #     self.assertEqual(old, new)

    # def test_autoSkipDay(self):
    #     old =
    #     new =
    #     self.assertEqual(old, new)
