import os
import gnupg
from pprint import pprint

class encript(object):
    def __init__(self,home):
        self.gpg = gnupg.GPG(gnupghome=home)


    def creatinKEY(self,mail,pasS):
        input_data = self.gpg.gen_key_input(
            name_email='garrantsitsua@gmail.com',
            passphrase='5dIf"ri?siaVrU#0jC')
        key = self.gpg.gen_key(input_data)
        print(key)

    def listkeys(self):
        arrPri = []
        arrPubl = []   
        public_keys = self.gpg.list_keys()
        private_keys = self.gpg.list_keys(True)
        for x in public_keys:
            arrPubl.append(x['keyid'])
        for x in private_keys:
            arrPri.append(x['keyid'])
        print("pribate key:")
        pprint(arrPri)
        print("public key:")
        pprint(arrPubl)
#gakoa sortu 
"""gpg = gnupg.GPG(gnupghome='keys')
input_data = gpg.gen_key_input(
    name_email='garrantsitsua@gmail.com',
    passphrase='5dIf"ri?siaVrU#0jC')
key = gpg.gen_key(input_data)
print(key)
#gakoak zerrendatu
gpg = gnupg.GPG(gnupghome='keys')
public_keys = gpg.list_keys()
private_keys = gpg.list_keys(True)
print('public keys:')
pprint(public_keys)
print('private keys:')
pprint(private_keys)
#gakoa exportattu
#ascii_armored_public_keys = gpg.export_keys("2B8CC6F15BFDE7C2")
#ascii_armored_private_keys = gpg.export_keys("2B8CC6F15BFDE7C2", True,expect_passphrase=False)
#with open('mykeyfile.asc', 'w') as f:
#    f.write(ascii_armored_public_keys)
#    f.write(ascii_armored_private_keys)

#gakoa inportatu
key_data = open('mykeyfile.asc').read()
import_result = gpg.import_keys(key_data)
pprint(import_result.results)"""

try:
    os.mkdir("key")
    cript = encript("key")
    cript.creatinKEY(None,None)
except FileExistsError:
    cript = encript("key")
    cript.listkeys()
    print("existit")


