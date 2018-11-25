import os
class bialketa(object):
    def __init__(self,izena,datuak,ruta,modua):
        self.izena = izena
        self.datuak = datuak
        self.ruta = ruta
        self.modua = modua
    
    def exekutatu(self):
        os.chdir(self.ruta)
        bytenone = bytes("none",encoding = 'utf-8')
        if self.modua == "all":
            con = 0
            for x in self.izena:
              try:
                if self.datuak[con] != bytenone:
                    f =  open(x,'wb')
                    f.write(self.datuak[con])
                    #print(self.datuak[con])
              except (IndexError,PermissionError):
                  None
              con += 1 
                

#bialketa = bialketa(izena_a,datu_a,ruta,modua)
#bialketa.exekutatu()
