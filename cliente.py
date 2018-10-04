import socket 
import time

s = socket.socket()
s.connect(("192.168.0.40",9999))


while True:
    recibido = s.recv(4096)
    url = str(recibido,encoding='utf-8')
    mensaje = input(url + ">")
    print(mensaje)
    mensaje_b = bytes(mensaje,encoding = "utf-8")
    s.send(mensaje_b)
    recibido = s.recv(4096)
    print(str(recibido,encoding='utf-8'))
    #recibido = s.recv(1111096)
    #print(recibido)
    if mensaje == "itxi":
        break
print ("agur")

s.close()