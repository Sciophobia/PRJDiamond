# Project: Project Diamond, Application Two Unit Test
# Purpose Details: Tests functionality of Application Two's methods.
# Course: IST 411
# Author: Sciophobia (Timothy)
# Date Developed: 10/9/2021
# Last Date Changed: 10/31/2021
# Rev: 2
import socket
import unittest
from time import sleep
from unittest.mock import patch
from APP2 import App2


class TestApp2(unittest.TestCase):


    def setUp(self):
        """Sets up the unit test variables for TestApp2.
         :type port: The port number that shall be used for all tests.
         :type payload: A simple bytearray to use as a test payload."""
        self.port = 8080
        self.payload = bytearray()
        self.A2 = App2

    '''Avoids conflict with actual log database with a blank method.'''

    def createEmptyLogger(self, blank, blank2):
        pass

    def createEmptyLogger(self, blank):
        pass

    def trueFunc(self, null):
        pass



    @patch("APP2.App2.log", createEmptyLogger)
    # @patch("APP2.App2.listenForPayload", trueFunc)
    def test_start_server(self):
        '''This test checks whether the server can start successfully on a predetermined test port. If this is the case
        the function returns true.'''
        print("***App2 test_start_server***")
        try:
            port = self.port
            A2 = App2
            A2.test = True
            print('Sleeping for 5 seconds...')
            sleep(5)
            print("Testing start server...")
            self.assertTrue(A2.startServer(A2, port))
            print("Complete.")
        except Exception as exc:
            print(str(exc))



    @patch("APP2.App2.log", createEmptyLogger)
    def test_listen_for_payload_unsecure_socket(self):
        '''This test checks whether the server accepts an unsecure socket or whether it throws an exception.
        If this is the case it returns false.'''
        try:
            print('\n ****App2 test_listen_for_payload_unsecure_socket**** \n')
            print("Sleeping for 5 seconds...")
            sleep(5)
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.bind((socket.gethostname(), self.port))
            self.A2 = App2
            with self.assertRaises(BrokenPipeError):
                serverSocket.sendall(self.payload)
            serverSocket.close()
        except Exception as exc:
            print(str(exc))


    # def tearDown(self):
    @patch("APP2.App2.log", createEmptyLogger)
    def test_sendPayload(self):
        ''' Tests the method sendPayload whether it successfully puts a test payload in the SFTP directory'''
        A2 = App2

        self.assertEqual(A2.sendPayload(A2, "Test Payload", "Digest"), "Test Payload")


if __name__ == '__main__':
    unittest.main()

    '''
     def listenForPayload(self, ssl_sock, port):
            try:
                while True:
                    print("Accepting connections from outside...", '\n')
                    (clientsocket, address) = ssl_sock.accept()
                    data = clientsocket.recv(1024).decode("ascii")
                    self.log('Connection accepted on port ', port)
                    try:
                        print('Payload received')
                        print(data, '\n')
                        print(type(data), '\n')
                        self.log('Payload received and decoded.')
                    finally:
                        clientsocket.shutdown(socket.SHUT_RDWR)
                        clientsocket.close()
                        print("Closing connection with client.", '\n')
                        self.log('Closing connection with client.')
                        return True
            except Exception as exc:
                print('\nError retrieving payload.', exc, '\n')
                error = ('Error retrieving payload. Error thrown: ', str(exc), ' Terminating.')
                self.log(error)
                return False
                
    '''
