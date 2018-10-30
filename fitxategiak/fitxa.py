import os
class bialketa(object):
    def __init__(self,izena,datuak,ruta,modua):
        self.izena = izena
        self.datuak = datuak
        self.ruta = ruta
        self.modua = modua
    
    def exekutatu(self):
        print(self.izena)
        #print(self.datuak)
        print(self.ruta)
        print(self.modua)
        os.chdir(self.ruta)
        if self.modua == "all":
            con = 0
            for x in self.izena:
              f =  open(x,'wb')
              f.write(self.datuak[con])
              con += 1 

#bialketa = bialketa(izena_a,datu_a,ruta,modua)
#bialketa.exekutatu()
