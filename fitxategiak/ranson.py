import os
from aesencrypt import aesenc
import binascii
import json


class ransow(object):
    def __init__(self):
        self.aes = None

    def oneGenerateKey(self,ruta):
        r = ruta.split("/")
        nameAr = r[len(r)-1]
        name = nameAr.split(".") 
        key = binascii.hexlify(os.urandom(32))
        iv = binascii.hexlify(os.urandom(16)) 
        Aes = {}
        Aes["key"] = str(key,encoding='utf-8')
        Aes["iv"] = str(iv,encoding='utf-8')
        strDecriAes = json.dumps(Aes)
        print(name)  
   

ran = ransow()
ran.oneGenerateKey("/sdksdk/kskd.py")