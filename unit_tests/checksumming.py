#!/usr/bin/python

import unittest
import random
from rocket import R60V


# known messages and their checksum (from Checksum.unit.ts)
checksum_data = {
    # empty message
    '': '00',
    # known checksums 1
    'r00000073': 'FC',
    'rB0000050': '09',
    'w00000064OK': '9B',
    # known checksums 2
    'Checksum calculation 1': '33',
    'Checksum calculation 2': '34',
    'Checksum calculation 3': '35',
    'Checksum calculation 4': '36',
    'Checksum calculation 5': '37',
    'Checksum calculation 6': '38',
    'Checksum calculation 7': '39',
    'Checksum calculation 8': '3A',
    'Checksum calculation 9': '3B',
    # Checksum: overflow
    'checksums overflow gracefully 1': 'F9',
    'checksums overflow gracefully 2': 'FA',
    'checksums overflow gracefully 3': 'FB',
    'checksums overflow gracefully 4': 'FC',
    'checksums overflow gracefully 5': 'FD',
    'checksums overflow gracefully 6': 'FE',
    'checksums overflow gracefully 7': 'FF',
    'checksums overflow gracefully 8': '00',
    'checksums overflow gracefully 9': '01'}

# known wrong messages (from Checksum.unit.ts) - verification should be:
# False
wrong_message_checksums = [
    # invalid message
    'F00DS0DA33',
    # tweaked checksums to be wrong
    'r00000073FF',
    'rB0000050FF',
    'w00000064OKFF']


class test_R60V(unittest.TestCase):
    def setUp(self):
        self.obj = R60V()

    # unit test functions
    def test_known_checksums(self):
        for msg in checksum_data.keys():
            # expected checksum
            expected = checksum_data[msg]
            # calculated checksum
            calc = self.obj._checksum(msg)

            self.assertEqual(calc, expected)

    def test_long_strings(self):
        # generate long string
        long_str = 'some-thing' * 1000
        # calculate checksum
        calc = self.obj._checksum(long_str)
        # (saved) expected checksum
        expected = '78'

        self.assertEqual(calc, expected)

    def test_insensitivity_of_byte_order(self):
        # Checksum should be insensitive to byte order
        # pick components
        comps = 'abcdefghijklmnopqrstuvwxyz0123456789'
        # shuffle components
        comps_shuffled = ''.join(random.sample(comps, len(comps)))
        # calculate checksums
        cs = self.obj._checksum(comps)
        cs_shuffled = self.obj._checksum(comps_shuffled)

        self.assertEqual(cs, cs_shuffled)

    def test_wrong_messages(self):
        for wrg_msg in wrong_message_checksums:
            self.assertFalse(self.obj._cs_verify(wrg_msg))
