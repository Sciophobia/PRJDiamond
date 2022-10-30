# Project: Project Diamond, Application Three
# Purpose Details: Receive SFTP payload and verify hash. Then send and e-mail the payload.
# Course: IST 411
# Author: Sciophobia (Timothy)
# Date Developed: 10/15/2021
# Last Date Changed: 11/28/2021
# Rev: 1
import getpass
import gzip
import hashlib
import hmac
import json
import smtplib
from email.mime.text import MIMEText

import Pyro4
import pysftp

from APP5 import App5


class App3(App5):

    def __init__(self):
        # Will change to true once hash is validated.
        self.key = "t6key"
        self.hashValidation = False
        pass



    def listenForPayload(self):
        """ Listens for a SFTP payload containing both the JSON data and appended digest. """
        password = getpass.getpass()
        username = 'tvg5197'
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        cinfo = {'cnopts': cnopts, 'host': 'oz-ist-lvmjxo.oz.psu.edu', 'username': username, 'password': password,
                 'port': 1855}
        try:
            with pysftp.Connection(**cinfo) as sftp:
                # Fetch payload from FTP server
                localDisk = '/home/tvg5197/'
                payload = (sftp.open(localDisk + 'abist411fa21Team6/App3/ftpreceive/JSONPayloadD.JSON', 'r', -1))

                # Separate JSON & digest

                split = payload.readlines()
                payloadStripped = split[0].rstrip('\n')
                print(payloadStripped)
                # payloadDec = payloadStripped.decode('ascii')
                payloadJSON = json.loads(payloadStripped)
                payloadJSONstr = json.dumps(payloadJSON)

                '''split[1].rstrip('\n') is the digest sent over with payload.
                payloadJSON is the original payload.'''
                # Validate SHA-256 digest
                print("Digest validation\n")
                self.hashValidation = self.validateDigest(payloadJSON, split[1].rstrip('\n'))
                # Email the payload.
                if self.hashValidation:
                    self.sendEmail(payloadJSONstr)
                    self.sendPayload(payloadJSONstr, self.uri)
                return payloadJSONstr

        except Exception as exc:
            print('Error listening for payload. ', getattr(exc, 'message', repr(exc)), '\n')
            self.log('App3', ('Error receiving payload. Error thrown: ', str(exc), ' Terminating.'))
            return exc



    def validateDigest(self, payload, digest):
        """ Validates the digest with a self-hashed version of the same payload."""
        key = bytes(self.key, 'utf-8')
        digesterSHA256 = hmac.new(key, payload.encode('utf-8'), hashlib.sha256)
        digestSHA256 = digesterSHA256.hexdigest()
        if hmac.compare_digest(digest, digestSHA256):
            print('Digests match.\n')
            self.log('App3', 'Digests verified and match.')
            return True
        else:
            return False



    def sendEmail(self, payload):
        """ Sends the JSON payload e-mail through a secure SMTP server,
            catch any exceptions, & then quit SMTP thread. """
        fromAddress = 'tvg5197@psu.edu'
        toAddress = 'tvg5197@psu.edu'
        subject = 'JSON Payload'
        msg = MIMEText(payload)
        msg['Subject'] = subject
        msg['From'] = fromAddress
        msg['To'] = toAddress
        try:
            mailMan = smtplib.SMTP_SSL('authsmtp.psu.edu', 465)
            mailMan.sendmail(fromAddress, [toAddress], msg.as_string())
            self.log('App3', 'Sent payload to email.')
        except Exception as exc:
            print('Error emailing payload. ', getattr(exc, 'message', repr(exc)), '\n')
            self.log('App3', ('Error emailing payload. Error thrown: ', str(exc), ' Terminating.'))
        finally:
            mailMan.quit()
            return msg



    def gzip_str(self, string_: str) -> bytes:
        """Compresses a string using the GZIP library into a bytes format."""
        return gzip.compress(string_.encode())


    def sendPayload(self, payload, uri):
        """ Compresses the payload using the GZIP library.
        Then using Pyro4 sends the compressed payload to App 4's request loop."""
        try:
            # We have to connect to the listening node.
            serverApp = Pyro4.Proxy(uri)

            # Print out object type for troubleshooting if needed. Compress with GZIP.
            print('Compressing... Current Object type: ', type(payload), "\n")
            self.log('App3', 'Compressing the payload.')
            compressedPayload = self.gzip_str(payload)
            print('Object type: ', type(compressedPayload), "\n")

            # Call remote method and print out whatever it returns.
            print(serverApp.receivePayload(compressedPayload))


            print('\nCompleted\n')
            self.log('App3', 'Payload compressed and sent successfully.')
            return compressedPayload
        except Exception as exc:
            print('Error occurred sending the payload. ', getattr(exc, 'message', repr(exc)), '\n')
            self.log('App3', ('Error occurred sending the payload. Error thrown: ', str(exc), ' Terminating.'))
            return False


# Run App 3
if __name__ == "__main__":
    A3 = App3()
    A3.uri = input("What is the Pyro URI of the greeting object? ").strip()
    A3.listenForPayload()
