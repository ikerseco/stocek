import os
import tempfile
from pprint import pprint
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from threading import Timer
#gakoa sortu
private_key = rsa.generate_private_key(
     public_exponent=65537,
     key_size=2048,
     backend=default_backend()
 )
#gako pribatua
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
 )
#print(f'pribatua\n:{pem}')
#gako publikoa
public_key = private_key.public_key()
pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
 )
#print(f'publikoa\n:{pem}')
#firmatu
message = b"A message I want to sign"
signature = private_key.sign(
     message,
     padding.PSS(
         mgf=padding.MGF1(hashes.SHA256()),
         salt_length=padding.PSS.MAX_LENGTH
     ),
     hashes.SHA256()
 )
#firma egiaztatu 
verify = public_key.verify(
     signature,
     message,
     padding.PSS(
         mgf=padding.MGF1(hashes.SHA256()),
         salt_length=padding.PSS.MAX_LENGTH
     ),
     hashes.SHA256()
)
#zifratu
message = b"encrypted data"
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        )
    )
#print(f'zifratua:\n{ciphertext}')
#deszifratu
plaintext = private_key.decrypt(
     ciphertext,
     padding.OAEP(
         mgf=padding.MGF1(algorithm=hashes.SHA256()),
         algorithm=hashes.SHA256(),
         label=None
     )
)
#print(f'zifratua kenduta:\n{plaintext.decode("utf-8")}') 








class asime(object):
    def __init__(self,home):
        self.fitxategia = tempfile.mkdtemp(suffix=None, prefix=None, dir=home)
         
    def Generastekey(self): 
       os.chdir(self.fitxategia)  
       #pribate key 
       os.mkdir("prybate", mode=0o777, dir_fd=None)
       os.chdir('prybate')
       private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
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
       os.mkdir("PCpublic", mode=0o777, dir_fd=None)
       os.chdir("PCpublic")
       public_key = private_key.public_key()
       pemPu = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
       )
       filePubli = open('pcPublic.pem','w')
       for x in pemPu.splitlines():
           filePubli.write(f'{str(x,"utf-8")}\n')
    
    def encrypted(self,data):
        with open(f'..\\PCpublic\\pcPublic.pem', "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
            ciphertext = public_key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return ciphertext
    
    def decrypt(self,data):
        with open(f'..\\prybate\\prybate.pem', "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=b'mypassword',
                backend=default_backend()
            )
            plaintext = private_key.decrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            print(plaintext)

    



asi = asime(".") 
asi.Generastekey()
xe = asi.encrypted(b"apa")
xd = asi.decrypt(xe)
print(xe)
