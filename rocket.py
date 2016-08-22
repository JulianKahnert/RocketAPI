#!/usr/bin/python

import numpy as np
import copy
import socket


class R60V:
    def __init__(self, machine_ip='192.168.1.1', machine_port=1774):
        """
        Documentation would be nice...
        """
        # connection to Rocket
        self.machine_ip = machine_ip
        self.machine_port = machine_port

    def send(self):
        """
        Documentation would be nice...
        """
        print('send data')

    def recieve(self):
        """
        Documentation would be nice...
        """
        print('get data')

    def parse(self):
        """
        Documentation would be nice...
        """
        print('python => bytes')

    def open(self):
        """
        Documentation would be nice...
        """
        message = self.cs_attach('r00000001')

        # from first connection attempt
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.machine_ip, self.machine_port))

        # DOUBLE CHECK THE REST:
        sock.write(message)

        conn, addr = sock.accept()
        print('Connection address:', addr)
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            print("received data:", data)
            conn.send(data)  # echo
        conn.close()

    def close(self):
        """
        Documentation would be nice...
        """
        print('close tcp connection')

    def update(self):
        """
        Documentation would be nice...
        """
        print('update properties')

    def checksum(self, raw):
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

    def cs_attach(self, message):
        message += self.checksum(message)

    def cs_verify(self, raw):
        # checksum max length 2 digits!?
        message_actual = raw[:-2]
        cs_actual = raw[-2:]
        cs_expected = self.checksum(message_actual)

        return cs_actual == cs_expected
