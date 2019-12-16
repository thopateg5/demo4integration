from rest_framework import generics
from .serializers import BucketlistSerializer
from .models import Bucketlist

import base64
import hmac
import hashlib
import time
import urllib
import urllib.parse
import requests
import re

from django.http import HttpResponse


class DeviceManager():    

    API_VERSION = '2018-06-30'
    TOKEN_VALID_SECS = 60 * 60   #365 * 24 * 60 * 60
    TOKEN_FORMAT = 'SharedAccessSignature sr=%s&sig=%s&se=%s&skn=%s'
    
    
    def __init__(self, connectionString=None):
        if connectionString != None:
            iotHost, keyName, keyValue = [sub[sub.index('=') + 1:] for sub in connectionString.split(";")]
            self.iotHost = iotHost
            self.keyName = keyName
            self.keyValue = keyValue
    
    def _buildExpiryOn(self):
        return '%d' % (time.time() + self.TOKEN_VALID_SECS)
    
    def _buildSasToken(self):
        targetUri = self.iotHost.lower()
        expiryTime = self._buildExpiryOn()
        toSign = '%s\n%s' % (targetUri, expiryTime)
        key = base64.b64decode(self.keyValue.encode('utf-8'))
        signature = urllib.parse.quote(
            base64.b64encode(
                hmac.HMAC(key, toSign.encode('utf-8'), hashlib.sha256).digest()
                )
        ).replace('/', '%2F')
        return self.TOKEN_FORMAT % (targetUri, signature, expiryTime, self.keyName)
    
    def createDeviceId(self, deviceId):
        sasToken = self._buildSasToken()
        url = 'https://%s/devices/%s?api-version=%s' % (self.iotHost, deviceId, self.API_VERSION)
        body = '{deviceId: "%s"}' % deviceId
        r = requests.put(url, headers={'Content-Type': 'application/json', 'Authorization': sasToken}, data=body)
        return r.text, r.status_code

    
    def retrieveDeviceId(self, deviceId):
        sasToken = self._buildSasToken()
        url = 'https://%s/devices/%s?api-version=%s' % (self.iotHost, deviceId, self.API_VERSION)
        r = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': sasToken})
        return r.text, r.status_code
    
    def listDeviceIds(self, top=None):
        if top == None:
            top = 1000
        sasToken = self._buildSasToken()
        url = 'https://%s/devices?top=%d&api-version=%s' % (self.iotHost, top, self.API_VERSION)
        r = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': sasToken})
        
        return r.text, r.status_code

    def createSasToken(self):
        sasToken1 = self._buildSasToken()
        return sasToken1

    def deleteDeviceId(self, deviceId):
        sasToken = self._buildSasToken()
        url = 'https://%s/devices/%s?api-version=%s' % (self.iotHost, deviceId, self.API_VERSION)
        r = requests.delete(url, headers={'Content-Type': 'application/json', 'Authorization': sasToken, 'If-Match': '*' }) 
        # If-Match Etag, but if * is used, no need to precise the Etag of the device. The Etag of the device can be seen in the header requests.text response 
        print(r.text)
        return r.text, r.status_code

    def deleteAllDevice(self, top=None):
        if top == None:
            top = 1000
        sasToken = self._buildSasToken()
        url = 'https://%s/devices?top=%d&api-version=%s' % (self.iotHost, top, self.API_VERSION)
        r = requests.delete(url, headers={'Content-Type': 'application/json', 'Authorization': sasToken,'If-Match': '*'})
        
        return r.text, r.status_code

    def DeletelistDevice(self, top=None):
        data = self.listDeviceIds()
        l1 =[]
        a = '{"deviceId":"(\\w+)"'
        t = re.compile(a)
        dev_name = t.findall(data[0])
        for a in dev_name:       
            g = self.deleteDeviceId(a)		
            l1.append(g)
        return l1
    
# if __name__ == '__main__':
# 	connectionString = 'HostName=newmyiothub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=7m1wTjgz4bgjPtTpRoV/fLhH3m73o9j9J0qtaJ9DJSU='
# 	dm = DeviceManager(connectionString)
# 	#print("\n\n")
# 	#print(dm.createSasToken())          #SAS Tocken 
	
# 	deviceId = 'iotdevice010'
#     print("\n\n")       
# 	print(dm.createDeviceId(deviceId)) 
# #	print("\n\n")
# #	print(dm.retrieveDeviceId(deviceId))
# #	print("\n\n")
# #	print(dm.listDeviceIds())
	