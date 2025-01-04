import os
import tempfile
from shutil import rmtree
from pprint import pprint
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from threading import Timer







class asime(object):
    def __init__(self,home):
        self.home = home
        self.public_key = None
        self.private_key = None
        self.fitxategia =  tempfile.mkdtemp(suffix=None, prefix=None, dir=home)
         
    def Generastekey(self,name): 
       os.chdir(self.fitxategia)  
       #pribate key 
       os.mkdir("prybate", mode=0o777, dir_fd=None)
       os.chdir('prybate')
       private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
       )
       pemPri = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
       )
       filePri = open('prybate.pem','w')
       for x in pemPri.splitlines():
           filePri.write(f'{str(x,"utf-8")}\n')
       #publik key
       os.chdir('../')
       os.mkdir("public", mode=0o777, dir_fd=None)
       os.chdir("public")
       public_key = private_key.public_key()
       pemPu = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
       )
       filePubli = open(f'pU{name}.pem','w')
       for x in pemPu.splitlines():
           filePubli.write(f'{str(x,"utf-8")}\n')
    
    def loadPublic(self,nameFile):
        with open(nameFile, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
            self.public_key = public_key

    def loadPrymari(self,nameFile):
        with open(nameFile, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=b'mypassword',
                backend=default_backend()
            )
            self.private_key = private_key    

    def encrypted(self,data):
        ciphertext = self.public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    def decrypt(self,data):
        plaintext = self.private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext

    def signe(self,message):
         signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
         ) 
         return signature

    def signeverific(self,signature,message):
        print(self.public_key)
        verify = self.public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return verify  
        
    def delete(self):
        rmtree(self.fitxategia)



#asi = asime(".") 
#asi.Generastekey()
#asi.loadPrymari()
#asi.loadPublic()
#en = asi.encrypted(b'apa')
#sing = asi.signe(b'apa')
#verifi = asi.signeverific(sing,b'apa')
#print(verifi)






