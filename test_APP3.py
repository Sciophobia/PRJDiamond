# Project: Project Diamond, Application Three Unit Test
# Purpose Details: Tests functionality of Application Three's methods.
# Course: IST 411
# Author: Sciophobia (Timothy)
# Date Developed: 10/31/2021
# Last Date Changed: 10/31/2021
# Rev: 1
import gzip
import hashlib
import hmac
import smtplib
import threading
import time
import unittest
import Pyro4
from unittest.mock import patch

from APP3 import App3


class MyTestCase(unittest.TestCase):
    """Avoids conflict with actual log database with a blank method."""

    def createEmptyLogger(self, blank, blank2):
        pass

    """ Tests the validateDigest function with a test message as its payload. If the in-method digest matches the
    App3 version then the test passes."""

    @patch("APP5.App5.log", createEmptyLogger)
    def test_validateDigest_equal(self):
        print("*** App3 test_validateDigest_equal***")
        msg = "Test Message"
        A3 = App3()
        key = bytes("Test Key", 'utf-8')
        A3.key = "Test Key"
        digesterSHA256 = hmac.new(key, msg.encode('utf-8'), hashlib.sha256)
        digestSHA256 = digesterSHA256.hexdigest()
        self.assertEqual(A3.validateDigest(msg, digestSHA256), True)

    """ Tests whether the validateDigest function returns false when two different digests are compared."""

    @patch("APP5.App5.log", createEmptyLogger)
    def test_validateDigest_mismatch(self):
        print("***App3 test_validateDigest_mismatch***")
        msg = "Test Message"
        A3 = App3
        key = bytes("Test Key", 'utf-8')
        A3.key = "Test Key"
        digesterSHA256 = hmac.new(key, msg.encode('utf-8'), hashlib.sha256)
        digestSHA256 = digesterSHA256.hexdigest()
        invalidMsg = "InvalidMsg"
        self.assertEqual(A3.validateDigest(A3, invalidMsg, digestSHA256), False)

    """ Tests the connection to the secure SMTP server that the application will be using to e-mail the payload."""

    def test_sendEmail(self):
        print("***App3 test_sendEmail***")
        # Connect to penn state secure SMTP server
        host = 'authsmtp.psu.edu'
        port = 465
        smtp = smtplib.SMTP_SSL('authsmtp.psu.edu', 465)

        print("Host: ", host, " Port: ", port)
        # check we have an open socket
        self.assertIsNotNone(smtp.sock)

        # run a no-operation, which is basically a server-side pass-through
        self.assertEqual((smtp.noop()), (250, b'2.0.0 OK'))

        # assert disconnected
        smtp.quit()
        self.assertIsNone(smtp.sock)

    """Compresses a string using the GZIP library into a bytes format.
    Credit: https://gist.github.com/Garrett-R/dc6f08fc1eab63f94d2cbb89cb61c33d"""

    def gzip_str(self, string_: str) -> bytes:
        return gzip.compress(string_.encode())

    """Validates whether a compressed payload is sent successfully using the sendPayload method. 
       The mock pyro server then receives the payload and the method should return the payload that was sent
       (compressed original)."""

    @patch("APP5.App5.log", createEmptyLogger)
    def test_sendPayload(self):
        print("***App3 test_sendPayload***")
        MServer = MockServer()
        uri = MServer.getURI()
        A3test = App3()
        compressedPayload = self.gzip_str("Test")
        self.assertEqual(A3test.sendPayload("Test", uri), compressedPayload)


class MockServer(object):

    def __init__(self, interval=1):
        """ Constructor

        :type interval: int
        :param interval: Check interval, in seconds.
        """
        self.interval = interval
        self.daemon = Pyro4.Daemon()
        self.uri = self.daemon.register(BlankDaemon)
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    """ Method that mimics a listener node for Pyro4. """

    def run(self):
        time.sleep(10)
        try:
            self.daemon.requestLoop()
            return self.daemon
        except Exception as exc:
            print('\nError (Mock Server): ', exc, '\n')

    if __name__ == '__main__':
        unittest.main()

    def getURI(self):
        return self.uri


class BlankDaemon:
    """Receives compressed payload from App3 using the Pyro4 proxy library.
     Then the data is converted to bytes using serpent and decompressed using
     the GZIP library."""

    @Pyro4.expose
    def receivePayload(self, payload):
        print("Fake pyro received.")



