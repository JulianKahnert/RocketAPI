#!/usr/bin/env python3

import unittest
import random
import api


# known messages and their checksum (from Checksum.unit.ts)
checksum_data = {
    # empty message
    b'': '00',
    # known checksums 1
    b'r00000073': 'FC',
    b'rB0000050': '09',
    b'w00000064OK': '9B',
    # known checksums 2
    b'Checksum calculation 1': '33',
    b'Checksum calculation 2': '34',
    b'Checksum calculation 3': '35',
    b'Checksum calculation 4': '36',
    b'Checksum calculation 5': '37',
    b'Checksum calculation 6': '38',
    b'Checksum calculation 7': '39',
    b'Checksum calculation 8': '3A',
    b'Checksum calculation 9': '3B',
    # Checksum: overflow
    b'checksums overflow gracefully 1': 'F9',
    b'checksums overflow gracefully 2': 'FA',
    b'checksums overflow gracefully 3': 'FB',
    b'checksums overflow gracefully 4': 'FC',
    b'checksums overflow gracefully 5': 'FD',
    b'checksums overflow gracefully 6': 'FE',
    b'checksums overflow gracefully 7': 'FF',
    b'checksums overflow gracefully 8': '00',
    b'checksums overflow gracefully 9': '01'}

# known wrong messages (from Checksum.unit.ts) - verification should be:
# False
wrong_message_checksums = [
    # invalid message
    b'F00DS0DA33',
    # tweaked checksums to be wrong
    b'r00000073FF',
    b'rB0000050FF',
    b'w00000064OKFF']


class test_R60V(unittest.TestCase):
    # def setUp(self):
    #     self.obj = R60V()

    # unit test functions
    def test_known_checksums(self):
        for msg in checksum_data.keys():
            # expected checksum
            expected = checksum_data[msg]
            # calculated checksum
            calc = api.checksum(msg)

            self.assertEqual(calc, expected)

    def test_long_strings(self):
        # generate long string
        long_str = 'some-thing' * 1000
        # calculate checksum
        calc = api.checksum(long_str)
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
        cs = api.checksum(comps)
        cs_shuffled = api.checksum(comps_shuffled)

        self.assertEqual(cs, cs_shuffled)

    def test_wrong_messages(self):
        for wrg_msg in wrong_message_checksums:
            self.assertFalse(api.cs_verify(wrg_msg))
