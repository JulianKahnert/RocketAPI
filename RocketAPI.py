#!/usr/bin/env python3

import socket
import time
import argparse
from rocket_state import machine_state
from rocket_state import Language
from rocket_state import DayOfWeek
from rocket_state import TemperatureUnit
from rocket_state import WaterSource
from rocket_state import ActiveProfile


class R60V:
    def __init__(self, machine_ip='192.168.1.1', machine_port=1774):
        """
        Documentation would be nice...
        """
        # connection to Rocket
        self.machine_ip = machine_ip
        self.machine_port = machine_port

        self.state = []

    def read(self):
        """
        read data from machine...

        """
        # might be added (!?): BUFFER_WAIT = 200; //ms

        BUFFER_SIZE = 128
        self.s = socket.create_connection((self.machine_ip, self.machine_port), 10)
        # get first "hello" from machine
        print(self.s.recv(BUFFER_SIZE))

        # waiting time seems to be important here
        time.sleep(1)

        self._parse_state()
        #print(self._read_byte(2))
       
        #for idx in range(0, 6):
        #    print('INDEX: {}'.format(idx))
        #    print(self._read_byte(idx))

        self.s.close()
        return self.state

    def write(self, state):
        """
        write data on machine...
        """
        print('write data on machine')

    # ### HELPER FUNCTIONS ###

    def _read_byte(self, idx):
        # from: https://wiki.python.org/moin/TcpCommunication
        BUFFER_SIZE = 128
        # generate message
        request = self._cs_attach('r' + format(idx, '04X') + format(1, '04X'))
        request = bytes(request, 'utf-8')
        #print('-> {}'.format(request))
        self.s.send(request)
        raw = self.s.recv(BUFFER_SIZE)
        #print('<- {}'.format(raw))
        if self._cs_verify(raw):
            # cut request and checksum
            data = raw.split(request[:-2])[1][:-2]
            value = int(data, 16)

        else:
            print('ERROR IN CHECKSUM!')
            value = []
        print('Index {} => {}'.format(idx, value))

        # not very nice, but more reliable:
        time.sleep(0.1)
        return value


    def _parse_state(self):
        """
        CURRENTLY NOT WORKING!!!
        Fix methods (from src/protocol/MemorySlice.ts):
        * getByte
        * getBoolean
        * getShort
        * getInt
        """
        state = machine_state()
        state.temperatureUnit = TemperatureUnit[self._read_byte(0)]
        state.language = Language[self._read_byte(1)]
        state.coffeeTemperature = self._read_byte(2)
        state.steamTemperature = self._read_byte(3)
        #state.coffeePID = self._parse_PID(4)          # 4-5, 10-11, 16-17
        #state.coffeePID = self._parse_PID(6)          # 6-7, 12-13, 18-19
        #state.coffeePID = self._parse_PID(8)          # 8-9, 14-15, 20-21
        state.pressureA = self._parse_profile(22)     # 22-36
        state.pressureB = self._parse_profile(38)     # 38-52
        state.pressureC = self._parse_profile(54)     # 54-68
        state.waterSource = WaterSource[self._read_byte(70)]
        state.activeProfile = ActiveProfile[self._read_byte(71)]
        #state.steamCleanTime = self._read_byte(72)
        state.isServiceBoilerOn = self._read_byte(73) == 1
        state.isMachineInStandby = self._read_byte(74) == 1
        #state.coffeeCyclesSubtotal = self._read_byte(75)      # 75-76
        #state.coffeeCyclesTotal = self._read_byte(77)           # 77-80
        #state.autoOnTime = [self._read_byte(81), self._read_byte(82)]
        #state.autoStandbyTime = [self._read_byte(83), self._read_byte(84)]
        #state.autoSkipDay = self._read_byte(85)
        self.state = state

    def _parse_PID(self, offset):
        PID = []
        PID.append(self._read_byte(offset + 0))
        PID.append(self._read_byte(offset + 6))
        PID.append(self._read_byte(offset + 12))
        return PID

    def _parse_profile(self, offset):
        profile = []
        profile.append([self._read_byte(offset + 0) / 10,
                        self._read_byte(offset + 10) / 10])
        profile.append([self._read_byte(offset + 2) / 10,
                        self._read_byte(offset + 11) / 10])
        profile.append([self._read_byte(offset + 4) / 10,
                        self._read_byte(offset + 12) / 10])
        profile.append([self._read_byte(offset + 6) / 10,
                        self._read_byte(offset + 13) / 10])
        profile.append([self._read_byte(offset + 8) / 10,
                        self._read_byte(offset + 14) / 10])
        return profile

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
        # checksum max length 2 digits!?
        message_actual = raw[:-2]
        cs_actual = raw[-2:]
        cs_expected = self._checksum(message_actual)

        return cs_actual == cs_expected


# external helper functions

def num2hex(idx):
    return format(idx, '04X')

def hex2num(sz):
    return int(sz, 16)

def f2c(f):
    c = (f - 32) * 5 / 9
    return round(c)


def c2f(c):
    f = (c * 9 / 5) + 32
    return round(f)


# COMMAND LINE INTERFACE

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Commandline tool to read and write data from R60V.')
    parser.add_argument('-r', '--read',
                        dest='read',
                        action='store_true',
                        help='read machine state')
    
    parser.add_argument('-on', '--on',
                        dest='on',
                        action='store_true',
                        help='start the machine')

    parser.add_argument('-off', '--off',
                        dest='off',
                        action='store_true',
                        help='shut down the machine')

    parser.add_argument('-s', '--set',
                        dest='setting',
                        nargs=2,
                        action='store',
                        help='change settings with a key-value pair')
    args = parser.parse_args()

    obj = R60V()
    
    if args.on:
        print('Start the machine ...')

    if args.off:
        print('Shutting down the machine ...')

    if args.read:
        print('Read machine state!')

    if args.setting:
        print('Write these settings on the machine:')
        print(args.setting)
