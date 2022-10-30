# Project: Project Diamond, Application Four Unit Test
# Purpose Details: Tests functionality of Application Four's methods.
# Course: IST 411
# Author: Sciophobia (Timothy)
# Date Developed: 11/24/2021
# Last Date Changed: 12/12/2021
# Rev: 1
import gzip
import unittest
from unittest.mock import patch

from Crypto.Cipher import AES

from APP4 import App4


def gzip_str(string_: str) -> bytes:
    """Compresses a string using the GZIP library into a bytes format."""
    return gzip.compress(string_.encode())


class MyTestCase(unittest.TestCase):

    def createEmptyLogger(self, blank, blank2):
        """Avoids conflict with actual log database with a blank method."""
        pass

    @patch("APP5.App5.log", createEmptyLogger)
    def test_processPayload_dataDecompression(self):
        """Tests the payload decompression method within Application four using a string 'Test'."""
        print("***App3 test_processPayload_dataDecompression***")
        A4d = App4()
        testGZIP = gzip_str("Test")
        # unzips as an byte object.
        self.assertEqual(A4d.processPayload(testGZIP), b"Test")

    @patch("APP5.App5.log", createEmptyLogger)
    def test_run_pyroDaemon(self):
        """Tests whether we can launch a Pyro4 proxy listener successfully on the localhost."""
        print("***App3 test_run_pyroDaemon***")
        A4d = App4()
        self.assertTrue(A4d.run(True))

    @patch("APP5.App5.log", createEmptyLogger)
    def test_encryptPayload(self):
        """Tests the AES encryption of the payload with a test payload."""
        A4e = App4()
        testPayload = b"Test"
        pad = b' '
        obj = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
        plaintext = testPayload
        print("Payload:\n", plaintext)
        length = 16 - (len(plaintext) % 16)
        plaintext += length * pad
        print("Length: ", length)
        encryptedPayload = obj.encrypt(plaintext)
        self.assertEqual(A4e.encryptPayload(testPayload), encryptedPayload)

    @patch("APP5.App5.log", createEmptyLogger)
    def test_sendPayload(self):
        """Tests the messaging Rabbit Message Queue function that is used to send the encrypted payload to App1."""
        print("***App3 test_run_pyroDaemon***")
        A4d = App4()
        payload = b"Test"
        self.assertEqual(A4d.sendPayload(payload), payload)


if __name__ == '__main__':
    unittest.main()
