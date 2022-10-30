# Project: Project Diamond, Application Two
# Purpose Details: To receive the secure payload from App1 using TLS.
# Course: IST 411
# Author: Sciophobia (Timothy)
# Date Developed: 10/9/2021
# Last Date Changed: 10/31/2021
# Rev: 2
import getpass
import hashlib
import hmac
import json
import socket
import ssl

import pysftp as pysftp

from APP5 import App5


class App2(App5):
    myName = 'App2'
    test = False

    def __init__(self):
        self.key = "t6key"
        pass

    def startServer(self, port):
        """The server starts on the specified port. The socket is then created and wrapped with the
        certificate file "server.crt" and the keyfile "server.key". """

        try:
            print(ssl.OPENSSL_VERSION)
            print('\nCreate an INET, STREAMing socket using SSL \n')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_sock = ssl.wrap_socket(s,
                                       server_side=True,
                                       certfile="server.crt",
                                       keyfile="server.key")
            print('Binding the socket to a public host (localhost) and port,', port, ', ...\n')
            self.log('App2 ', 'Server socket using Cert File server.crt and Key File server.key')
            ssl_sock.bind((socket.gethostname(), port))
            self.log('App2 ', ('Bind socket to localhost and port ', port))
            ssl_sock.listen(5)
            self.log('App2 ', 'Now listening for outside connections.')
            print("\nCiphers: " + str(ssl_sock.cipher()), '\n')
            if not self.test:
                print("Executing listenForPayload...\n")
                self.listenForPayload(ssl_sock, port)
            return True
        except Exception as exc:
            print('Error starting server. ', getattr(exc, 'message', repr(exc)), '\n')
            self.log('App2 ', ('Error starting server. Error thrown: ', str(exc), ' Terminating.'))
            return False

    def listenForPayload(self, ssl_sock, port):
        """The payload is accepted after the SSL handshake is completed. The method then decodes the data and closes
        the connection with the client node."""
        try:
            while True:
                print("Accepting connections from outside...", '\n')
                (clientsocket, address) = ssl_sock.accept()
                data = clientsocket.recv(1024).decode("ascii")
                self.log('App 2 ', ('Connection accepted on port ', port))
                try:
                    print('Payload received')
                    print(data, '\n')
                    print(type(data), '\n')
                    self.log('App 2 ', 'Payload received and decoded.')
                finally:
                    print("Closing connection with client.", '\n')
                    self.log('App 2 ', 'Closing connection with client.')
                    return self.sendPayload(data, self.hashDataSHA256(data, self.key))
        except Exception as exc:
            print('\nError retrieving payload.', exc, '\n')
            self.log('App 2 ', ('Error retrieving payload. Error thrown: ', str(exc), ' Terminating.'))
            return exc

    def hashDataSHA256(self, msg, key):
        """
        Hashes the message using SHA-256. The payload is hashed with SHA-256 in order to maintain data integrity.
        :param msg: Payload to be hashed.
        :param key: Key to be hashed.
        :return: JSON Payload with SHA-256 Checksum
        """
        # print("***Processing SHA-256: ", whoami, "***\n")
        print("Key: ", self.key, "\n")
        print("Digest...")

        try:
            self.log('App2', "Hashing payload.")
            print("\nMessage Type: ", type(msg), "Key type: ", type(key), "\n")
            key = bytes(self.key, 'utf-8')
            digesterSHA256 = hmac.new(key, msg.encode('utf-8'), hashlib.sha256)
            digestSHA256 = digesterSHA256.hexdigest()
        except Exception as exc:
            print('Error hashing payload. ', getattr(exc, 'message', repr(exc)), '\n')
            self.log('App2', ("Error hashing payload. Error thrown: ", (str(exc), "Terminating.")))
            return exc
        finally:
            print("Hashing complete.\n")
            self.log('App2 ', "Successfully hashed JSON payload using SHA-256.")
            # Append checksum to message
            self.log('App2', "Appending checksum to message.")
            return digestSHA256

    def sendPayload(self, payload, digest):
        """Appends the payload's digest to the payload message and uses SFTP to transfer the JSON to App 3 via SFTP"""
        password = getpass.getpass()
        username = 'tvg5197'
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        cinfo = {'cnopts': cnopts, 'host': 'oz-ist-lvmjxo.oz.psu.edu', 'username': username, 'password': password,
                 'port': 1855}
        try:
            with pysftp.Connection(**cinfo) as sftp:
                localDisk = '/home/tvg5197/'
                print("Connection established.\n")
                self.log('App2', "Connection established via SFTP.")
                # Preparing appended payload for transfer.
                print("Preparing write out...\n")
                self.writeOut(payload, digest)
                # Upload the payload to an SFTP server
                self.log('App 2 ', "Putting payload in App3 FTP receive directory.")

                # sftp.put('App3/ftpsend/jsonPayloadD.JSON', 'App3/ftpreceive/jsonPayloadD.JSON')
                print('\n!Now transferring payload to SFTP folder!\n')
                self.log('App2', "Now transferring payload to SFTP folder.")
                sftp.put((localDisk + "abist411fa21Team6/App2/ftpsend/jsonPayloadD.JSON"),
                         'abist411fa21Team6/App3/ftpreceive/JSONPayloadD.JSON')

        except Exception as e:
            print('Error sending payload. ', getattr(e, 'message', repr(e)), '\n')
            self.log('App 2 ', ('Error sending payload. ', getattr(e, 'message', repr(e)), '\n'))
            return e
        finally:
            print("\nTask End.\n")
            sftp.close()
            self.log('App 2 ', "Payload sent to App3  using SFTP.")
            return payload

    def writeOut(self, jsonPayload, digest):
        """Writes the given JSON to the local disk for SFTP processing. All exceptions are caught and actions logged into the
        MongoClient."""
        try:

            print("Writing file...")
            self.log('App2', "Writing payload to JSON file jsonPayloadD.JSON.")
            with open('App2/ftpsend/jsonPayloadD.JSON', 'w') as outFile:
                outFile.write(json.dumps(jsonPayload))
                print("Digest: ", digest)
                outFile.writelines('\n' + digest)
            print("Wrote payload to text file jsonPayloadD.JSON")

            self.log('App2', "Wrote payload to text file jsonPayloadD.JSON.")
            return True
        except Exception as exc:
            print('\nError writing payload to file.', exc, '\n')
            self.log('App2', ('Error writing payload to file. Error thrown: ', str(exc), ' Terminating.'))
            return exc

    def runApp2(self):
        myPort = 8080
        a = App2()
        a.startServer(myPort)


if __name__ == "__main__":
    A2 = App2
    A2.runApp2(A2)
