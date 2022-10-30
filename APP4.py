# Project: Project Diamond, Application Four
# Purpose Details: receive the Pyro python object and convert it back to JSON. Then
# encrypts the payload and sends the payload to App1 using RabbitMQ.
# Course: IST 411
# Author: Sciophobia (Timothy)
# Date Developed: 11/18/2021
# Last Date Changed: 12/11/2021
# Rev: 2

import gzip

import Pyro4
import pika
import serpent
from Crypto.Cipher import AES

from APP5 import App5


class App4Daemon(App5):
    """Receives compressed payload from App3 using the Pyro4 proxy library.
    """

    @Pyro4.expose
    def receivePayload(self, payload):
        A4 = App4()
        A4.processPayload(payload)


class App4(App5):


    def run(self, testMode):
        """ Registers the Pyro4 Daemon and starts the request loop to fetch payload from App 3."""
        try:
            daemon = Pyro4.Daemon()
            uri = daemon.register(App4Daemon)
            self.log('App4', 'Pyro Daemon registered and ready.')
            print('\nReady. Object URI: ', str(uri), ' \n')
            if not testMode:
                daemon.requestLoop()
            return True
        except Exception as e:
            print('\nAn error occurred. \n')
            print(getattr(e, 'message', repr(e)))
            return e



    def processPayload(self, payload):
        """Converts compressed payload to bytes using serpent and
        decompresses the same payload using the GZIP library."""
        try:
            print(type(payload))
            print("Converting received message to bytes using serpent...")
            self.log('App4', 'Message received.')
            payloadSerp = serpent.tobytes(payload)
            print(type(payloadSerp))
            print("Decompressing the data using GZIP library...")
            self.log('App4', 'Decompressing the Pyro4 message using GZIP.')
            decompressedData = gzip.decompress(payloadSerp)
            print("Decompressed data: ", decompressedData)
            self.log('App4', 'Data successfully decompressed..')
            self.encryptPayload(decompressedData)
            return decompressedData
        except Exception as e:
            print('\nAn error occurred running receivePayload in App4 Daemon. \n')
            self.log("App4", "There was an issue receiving the payload from App3.")
            print(getattr(e, 'message', repr(e)))
            return e



    def sendPayload(self, payload):
        """Sends the AES encrypted payload to App1s ist411Team6 queue using RabbitMQ."""
        try:
            # self.log('App4', '')

            msgBytes = payload
            self.log('App4', 'Connecting to the Message Channel')

            print("Connecting to Localhost Queue...")
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()
            print("Channel Connected.")
            self.log('App4', 'Connected to the Message Channel.')
            channel.queue_declare(queue="ist411Team6")
            self.log('App4', 'Message queue ist411Team6 declared.')
            channel.basic_publish(exchange='', routing_key='ist411Team6', body=msgBytes)
            # print("Sent: \n" + msgBytes)
            self.log('App4', 'Message sent to queue ist411Team6.')
            connection.close()
            self.log('App4', 'Message channel connection closed.')
            return payload
        except Exception as e:
            print('\nAn error occurred sending message to App1 using message queueing...\n')
            self.log("App4", "An error occurred sending message to App1 using message queueing.")
            print(getattr(e, 'message', repr(e)))
            self.log("App4", (getattr(e, 'message', repr(e))))



    def encryptPayload(self, payload):
        """Encrypts the given payload using AES encryption then passes that encrypted payload to the sendPayload
        function. """
        try:
            pad = b' '
            self.log('App4', 'Starting AES encryption of payload.')
            obj = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
            # .encode('utf-8')
            plaintext = payload
            print("Payload:\n", plaintext)
            length = 16 - (len(plaintext) % 16)
            self.log('App4', 'Padding payload for encryption.')
            plaintext += length * pad
            print("Length: ", length)
            self.log('App4', 'Encrypting payload with AES encryption.')
            encryptedPayload = obj.encrypt(plaintext)
            self.log('App4', 'Sending encrypted payload to App1.')
            self.sendPayload(encryptedPayload)
            return encryptedPayload
        except Exception as e:
            print('\nAn error occurred encrypting message\n')
            self.log("App4", "An error occurred encrypting message.")
            print(getattr(e, 'message', repr(e)))
            self.log("App4", (getattr(e, 'message', repr(e))))
            return e

if __name__ == "__main__":
    A4 = App4()
    A4.run(False)
