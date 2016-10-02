#!/usr/bin/env python3

import logging
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
        if self.s.recv(self.buffer_size) == b'*HELLO*':
            logging.info('Connection established!')
        else:
            logging.critical('ERROR: machine not reachable')
            return

        # waiting time seems to be important here
        time.sleep(0.5)

    def __del__(self):
        """
        Destructor
        """
        self.s.close()
        logging.info('Connection closed!')

    def read(self, idx):
        """
        Read data
        """
        # generate message
        request = self._cs_attach('r' + format(idx, '04X') + format(1, '04X'))
        request = bytes(request, 'utf-8')
        
        # send request
        logging.info('-> {}'.format(request))
        self.s.send(request)

        # recieve data
        try:
            raw = self.s.recv(self.buffer_size)
        except timeout:
            logging.error('connection timed out')
        logging.info('<- {}'.format(raw))

        # get date from message
        if self._cs_verify(raw):
            # cut request and checksum
            data = raw.split(request[:-2])[1][:-2]
            value = int(data, 16)
        else:
            logging.error('ERROR IN CHECKSUM!')
            value = []

        # not very nice, but more reliable:
        time.sleep(0.1)

        return value

    def write(self, idx, value):
        """
        write data on machine...
        """
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
