import os
import subprocess
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class aesenc(object):
    def __init__(self,key,iv):
        self.ciper = Cipher(algorithms.AES(key), modes.CFB(iv))
    
    def encript(self,data):
        encryptor = self.ciper.encryptor() 
        ct = encryptor.update(data) 
        return ct

    def decript(self,data):
        decryptor = self.ciper.decryptor()
        cd = decryptor.update(data)
        return cd



""""

key1 = os.urandom(32)
iv1 = os.urandom(16)

print(key1)

cliente1 = aesenc(key1,iv1)

m1 = bytes('a',encoding='utf-8')
result = subprocess.run(["powershell", "-Command", "ls C:\\Users\\garra\\Documents\\git\\soket\\stocek\\tmp01ltsdc5"], capture_output=True, text=True)
print(len(m1))
print(len("a"))
m2 = b'C:\\Users\\garra\\Documents\\git\\soket\\stocek\\tmp01ltsdc5'
print(len(m2))
r = bytes(result.stdout,encoding='utf8')
print(len(r))
m1enc = cliente1.encript(m2)
print(m1enc)
print(len(m1enc))
m1dec= cliente1.decript(m1enc)
print(str(m1dec,encoding='utf-8'))




key1 = os.urandom(32)
iv1 = os.urandom(16)
result = subprocess.run(["powershell", "-Command", "ls"], capture_output=True, text=True)

cipher = Cipher(algorithms.AES(key1), modes.CBC(iv1))
encryptor = cipher.encryptor()
ct = encryptor.update(b'bai') 
print(ct)
decryptor = cipher.decryptor()
cd = decryptor.update(ct) 
print(cd)
"""
