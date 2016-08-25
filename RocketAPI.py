#!/usr/bin/env python3

import socket
import argparse
from rocket_state import machine_state


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
        # from: https://wiki.python.org/moin/TcpCommunication
        BUFFER_SIZE = 1024
        # might be added (!?): BUFFER_WAIT = 200; //ms
        MESSAGE = b'Hello, World!'
        #MESSAGE = self._cs_attach('r00000001')

        # <https://github.com/jffry/rocket-r60v/blob/a9c657b7697bc92c3cdc9511f0aaf8b55b148e0d/src/protocol/messages/MachineState.ts#L260>
        #MESSAGE = self._cs_attach('r00000073')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.machine_ip, self.machine_port))
        s.send(MESSAGE)
        data = s.recv(BUFFER_SIZE)
        s.close()
        self.state = self._parse_state(data)
        return self.state

    def write(self, state):
        """
        write data on machine...
        """
        print('write data on machine')

    # ### HELPER FUNCTIONS ###

    def _parse_state(self, data):
        """
        CURRENTLY NOT WORKING!!!
        Fix methods (from src/protocol/MemorySlice.ts):
        * getByte
        * getBoolean
        * getShort
        * getInt
        """
        state = machine_state()
        state.temperatureUnit = data.getByte(0)
        state.language = data.getByte(1)
        state.coffeeTemperature = data.getByte(2)
        state.steamTemperature = data.getByte(3)
        state.coffeePID = self._parse_PID(data, 4)          # 4-5, 10-11, 16-17
        state.coffeePID = self._parse_PID(data, 6)          # 6-7, 12-13, 18-19
        state.coffeePID = self._parse_PID(data, 8)          # 8-9, 14-15, 20-21
        state.pressureA = self._parse_profile(data, 22)     # 22-36
        state.pressureB = self._parse_profile(data, 38)     # 38-52
        state.pressureC = self._parse_profile(data, 54)     # 54-68
        state.waterSource = data.getByte(70)
        state.activeProfile = data.getByte(71)
        state.steamCleanTime = data.getByte(72)
        state.isServiceBoilerOn = data.getBoolean(73)
        state.isMachineInStandby = data.getBoolean(74)
        state.coffeeCyclesSubtotal = data.getShort(75)      # 75-76
        state.coffeeCyclesTotal = data.getInt(77)           # 77-80
        state.autoOnTime = [data.getByte(81), data.getByte(82)]
        state.autoStandbyTime = [data.getByte(83), data.getByte(84)]
        state.autoSkipDay = data.getByte(85)
        return state

    def _parse_PID(self, data, offset):
        PID = []
        PID.append(data.getByte(offset + 0))
        PID.append(data.getByte(offset + 6))
        PID.append(data.getByte(offset + 12))
        return PID

    def _parse_profile(self, data, offset):
        profile = []
        profile.append([data.getShort(offset + 0), data.getByte(offset + 10)])
        profile.append([data.getShort(offset + 2), data.getByte(offset + 11)])
        profile.append([data.getShort(offset + 4), data.getByte(offset + 12)])
        profile.append([data.getShort(offset + 6), data.getByte(offset + 13)])
        profile.append([data.getShort(offset + 8), data.getByte(offset + 14)])
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

    def _cs_attach(self, message):
        message += self._checksum(message)

    def _cs_verify(self, raw):
        # checksum max length 2 digits!?
        message_actual = raw[:-2]
        cs_actual = raw[-2:]
        cs_expected = self._checksum(message_actual)

        return cs_actual == cs_expected


# external helper functions

def f2c(self, f):
    c = (f - 32) * 5 / 9
    return round(c)


def c2f(self, c):
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