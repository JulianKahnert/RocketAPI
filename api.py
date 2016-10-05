#!/usr/bin/env python3

import logging
import socket
import time


class api:
    def read(self, idx, run_num=0):
        """
        Read data
        """
        # generate message
        request = cs_attach('r' + format(idx, '04X') + format(1, '04X'))
        request = bytes(request, 'utf-8')

        self.log.info('read byte #{} (run {})'.format(idx, run_num + 1))
        if run_num != 0:
            # not very nice, but more reliable:
            time.sleep(0.1)

        # send request
        self.log.debug('-> {}'.format(request))
        self.s.send(request)

        try:
            # recieve data
            raw = self.s.recv(self.buffer_size)

        except socket.timeout:
            # try to read data 3 times, if valid break
            if run_num < 3:
                self.log.warning('socket timed out - retry to read ...')
                self.read(idx, run_num + 1)
            else:
                critical(self.log, 'socket timed out')

        except (ConnectionResetError, BrokenPipeError):
            critical(self.log,
                     'connection broken: unable to continue, please create a new state object')

        self.log.debug('<- {}'.format(raw))

        # verify message and checksum
        bLen = len(raw) == 13
        bSame = request[:9] == raw[:9]
        bChecksum = cs_verify(raw)
        if not (bLen and bSame and bChecksum) and run_num == 2:
            critical(self.log,
                     'invalid message from machine - len: {}, same: {}, checksum: {}'.format(bLen, bSame, bChecksum))

        # cut request and checksum
        data = raw.split(request[:-2])[1][:-2]
        value = int(data, 16)
        self.log.debug('recieved value: "{}"'.format(value))
        return value

    def write(self, idx, value):
        """
        write data on machine...
        """
        # no floats allowed
        value = int(value)

        # create request
        self.log.info('write byte #{} with value "{}"'.format(idx, value))
        request = cs_attach('w' + format(idx, '04X') + format(1, '04X') + format(value, '02X'))
        request = bytes(request, 'utf-8')

        # send request
        self.log.debug('-> {}'.format(request))
        self.s.send(request)

        # validation of write request
        time.sleep(0.8)
        machine_val = self.read(idx)
        if machine_val != value:
            self.log.warning('write validation failed! machine: {} - wanted: {}'.format(machine_val, value))

    def close(self):
        """
        Destructor
        """
        self.log.info('close connection to machine')
        self.s.close()

    def __init__(self, machine_ip='192.168.1.1', machine_port=1774):
        """
        Contructor
        """
        # create logger
        self.log = logging.getLogger('rocket.api')

        # connection to Rocket
        self.machine_ip = machine_ip
        self.machine_port = machine_port
        self.buffer_size = 128

        # establishing the connection
        self.s = socket.create_connection(
            (self.machine_ip, self.machine_port), timeout=3)

        # get first "hello" from machine
        if self.s.recv(self.buffer_size) == b'*HELLO*':
            self.log.info('connection established')
        else:
            critical(self.log, 'machine not reachable')


def critical(log_obj, msg):
    """
    CHECKSUM
    """
    log_obj.critical(msg)
    raise RuntimeError(msg)


def checksum(raw):
    """
    CHECKSUM
    """
    if isinstance(raw, bytes):
        raw = raw.decode('utf-8')

    value = 0
    for sz in raw:
        value += ord(sz)
    value_hex = hex(value & 255)[2:].upper()
    if len(value_hex) < 2:
        value_hex = '0' + value_hex
    return value_hex


def cs_attach(message_tmp):
    message_tmp += checksum(message_tmp)
    return message_tmp


def cs_verify(raw):
    if isinstance(raw, bytes):
        raw = raw.decode('utf-8')

    # checksum max length 2 digits
    message_actual = raw[:-2]
    cs_actual = raw[-2:]
    cs_expected = checksum(message_actual)
    return cs_actual == cs_expected
