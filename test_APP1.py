# Project: Project Diamond, Application One Unit Test
# Purpose Details: Tests functionality of Application One's methods.
# Course: IST 411
# Author: Sciophobia (Timothy)
# Date Developed: 10/9/2021
# Last Date Changed: 12/12/2021
# Rev: 1
import json
import socket
import ssl
import threading
import time
import unittest
from unittest.mock import patch

from APP1 import App1
from APP4 import App4
from Crypto.Cipher import AES


class TestAPP1(unittest.TestCase):

    # This is called immediately before calling the test methods.
    def setUp(self):
        self.port = 8080
        x = '{ "name":"John", "age":30, "city":"New York"}'
        self.testPayload = json.dumps(json.loads(x))


    def createEmptyLogger(self, blank, blank2):
        pass

    def createEmptyLogger(self, blank):
        pass





    @patch("APP1.App1.log", createEmptyLogger)
    def test_writeOut_testPayload(self):
        """This tests the function that writes out App1's pulled JSON payload to a text file. In this case
        a test JSON object is used."""
        print('***App1 test_writeOut_testPayload***')
        A1 = App1
        self.assertTrue(App1.writeOut(A1, self.testPayload))



    @patch("APP1.App1.log", createEmptyLogger)
    def test_sendPayload(self):
        """ This test sends a bytearray payload via the sendPayload function to a mocked server running
         in the background with threading. Sleep functions are used to prevent conflict with other tests
         using the same port number."""
        print('***App1 test_sendPayload***')
        A1 = App1
        MServer = MockServer(self.port)
        print("Sending payload to mock server...")
        time.sleep(15)
        print("Sleeping stopped.")
        self.assertTrue(App1.sendPayload(A1, bytearray(), self.port))

    @patch("APP1.App1.log", createEmptyLogger)

    def test_receiveMessage(self):
        """ This tests the Rabbit Messaging Queue method receiveMessage's ability to receive a message successfully."""
        print("***test_receiveMessage***")

        A1 = App1

        with self.assertWarns(Warning):
            A1.receiveMessage(A1)

    @patch("APP1.App1.log", createEmptyLogger)
    def test_processMessage(self):
        """ This tests the decryption method used to decrypt incoming messages."""
        print("***test_processMessage***")
        A1 = App1
        testPayload = b"Test"
        pad = b' '
        obj = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
        plaintext = testPayload
        print("Payload:\n", plaintext)
        length = 16 - (len(plaintext) % 16)
        plaintext += length * pad
        print("Length: ", length)
        encryptedPayload = obj.encrypt(plaintext)
        A1.start = 1
        A1.stop = 1
        decrypt = A1.processMessage(A1, encryptedPayload)
        decrypt = decrypt.strip()
        self.assertEqual(decrypt, testPayload)




class MockServer(object):
    """ SSL Socket Listener Mock Class

    The run() method will be started and it will run in the background
    until the test exits.
    """

    def __init__(self, port, interval=1):
        """ Constructor

        :type interval: int
        :param interval: Check interval, in seconds.
        :param port: Test listener's port number
        """
        self.interval = interval
        self.port = port
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        print("Starting thread...")
        thread.start()  # Start the execution


    def run(self):
        """The method that provides core functionality for threaded (background) listener."""
        time.sleep(10)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_sock = ssl.wrap_socket(s,
                                       server_side=True,
                                       certfile="server.crt",
                                       keyfile="server.key")
            ssl_sock.bind((socket.gethostname(), self.port))
            ssl_sock.listen(5)
            (clientsocket, address) = ssl_sock.accept()
            try:
                print('Payload received')
            finally:
                clientsocket.shutdown(socket.SHUT_RDWR)
                ssl_sock.close()
                clientsocket.close()
        except Exception as exc:
            print('\nError (Mock Server): ', exc, '\n')
            ssl_sock.close()
            clientsocket.close()


