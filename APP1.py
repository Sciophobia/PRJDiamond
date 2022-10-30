# Project: Project Diamond, Application One
# Purpose Details: To CURL a JSON payload and send it securely to APP2 using SSL.
# Course: IST 411
# Author: Sciophobia (Timothy)
# Date Developed: 10/9/2021
# Last Date Changed: 12/11/2021
# Rev: 3

import json
import socket
import ssl
import urllib.request
import timeit
import warnings

import pika

from APP5 import App5
from pymongo import ASCENDING
from pymongo import MongoClient
from Crypto.Cipher import AES

client = MongoClient()
db = client.team6DB
logCollection = db.Log
logCollection.ensure_index([("timestamp", ASCENDING)])
myName = 'App1'


class App1(App5):
    url = 'https://jsonplaceholder.typicode.com/posts/1/comments'

    def __init__(self):
        pass



    def sendPayload(self, payload, port):
        """Sends the payload to APP2 using TLS with network sockets. The port is specified as a variable.
        Wraps socket with certificate "server.crt" and key file "server.key". All workflow actions are logged
        into the MongoClient."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Sending payload to server...\n')
            self.log('App1', 'Using Certificate file server.crt with key file server.key.')
            socketWrapped = ssl.wrap_socket(s,
                                            server_side=False,
                                            certfile="server.crt",
                                            keyfile="server.key")
            socketWrapped.connect((socket.gethostname(), port))
            print("\nPayload type: ", payload, "\n")
            self.log('App1', ('Sending payload to APP2. With socket host ', socket.gethostname(), ' on port ', port))
            socketWrapped.sendall(payload)
            print('Payload Sent. \n')
            self.log('App1', ('SSL Payload sent. Port ', port, ', With host ', socket.gethostname()))
            return socketWrapped

        except Exception as exc:
            print('Error sending payload. ', getattr(exc, 'message', repr(exc)), '\n')
            self.log('App1', ('Error sending payload. Error thrown: ', str(exc), ' Terminating.'))
            return exc



    def writeOut(self, jsonPayload):
        """Writes the given payload out to a text file. All exceptions are caught and actions logged into the
        MongoClient."""
        try:
            file = open('outFile.txt', 'w')
            jsonPayloadDec = json.loads(jsonPayload)
            self.log('App1', "Writing payload to text file outFile.txt.")
            file.write((json.dumps(jsonPayloadDec)))
            file.close()
            self.log('App1', "Wrote payload to text file outFile.txt.")
            return True
        except Exception as exc:
            print('\nError writing payload to file.', exc, '\n')
            self.log('App1', ('Error writing payload to file. Error thrown: ', str(exc), ' Terminating.'))
            return exc



    def retrievePayload(self, port):
        """Retrieves the JSON payload using CURL from the internet."""
        try:
            print(ssl.OPENSSL_VERSION)
            print('Fetching Payload...\n')
            self.log('App1', ('Fetching payload from ', self.url))
            self.response = urllib.request.urlopen(self.url)
            jsonPayload = self.response.read()
            self.log('App1', ('Payload received from ', self.url))
            print('Here is my payload:\n', jsonPayload.decode("ascii"), '\n')
            self.writeOut(jsonPayload)
            self.log('App1', 'Saved payload to outFile.txt')
            # Now we must send the payload over to App2
            self.sendPayload(jsonPayload, port)
            return True
        except Exception as exc:
            print(('Error retrieving payload. ', getattr(exc, 'message', repr(exc)), '\n'))
            self.log('App1', ('Error retrieving payload. Error thrown: ', str(exc), ' Terminating.'))
            return exc



    def receiveMessage(self):
        """Receives the encrypted message from App4 using RabbitMQ."""
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
            print("Connection established.")
            channel = connection.channel()
            self.log('App1', 'Declaring message queue ist411Team6.')
            channel.queue_declare(queue='ist411Team6')
            self.log('App1', 'Queue ist411Team6 declared.')
            print("Queue ist411Team6 declared...")
            warnings.warn("Starting channel callback...")

            def callback(ch, method, properties, body):
                print("Received: %r" % body)
                self.log('App1', 'Message received in channel ist411Team6.')
                self.processMessage(body)


            channel.basic_consume('ist411Team6', callback, auto_ack=True)
            channel.start_consuming()


        except Exception as exc:
            print("Error receiving message: \n", exc, "\n")
            self.log('App1', ('Error regarding the message queue. ', getattr(exc, 'message', repr(exc)), '\n'))



    def processMessage(self, cipherPayload):
        """Decrypts the AES-encrypted message and processes the decrypted data. Calculators total roundtrip time and logs
        the time in MongoDB. """
        try:
            dObj = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
            dText = dObj.decrypt(cipherPayload)
            print("Decrypted: \n", dText.decode("utf8"))
            self.stop = timeit.default_timer()
            roundtrip = self.stop - self.start
            print('Total app run time: ', roundtrip)
            self.log('App1', ('Total roundtrip time calculator as ', roundtrip, ' seconds. '))
            return dText
        except Exception as exc:
            print('\nError performing decryption.', exc, '\n')
            return exc

    def __enter__(self):
        self.connection = MongoClient(self.hostname, self.port)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close()

    def runApp1(self):
        """Executes App1's method and initiates roundtrip timer. """
        self.start = timeit.default_timer()
        portNum = 8080
        a = App1()
        a.retrievePayload(portNum)
        print("Listening to message queue...")
        a.receiveMessage()


if __name__ == "__main__":
    A1 = App1
    A1.runApp1(A1)
