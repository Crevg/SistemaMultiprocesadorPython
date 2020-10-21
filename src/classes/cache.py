from .bloque import Bloque
#Memoria Cache L1
class Cache:
    #Inicializa los bloques en 2 pares de 2 bloques por la asociatividad e inicializa los punteros de reemplazo
    def __init__(self):
        self.siguienteImpar = 0
        self.siguientePar = 0
        self.way0 = [Bloque(None, None, 0, "I"), Bloque(None, None, 1, "I")] #PARES
        self.way1 = [Bloque(None, None, 2, "I"), Bloque(None, None, 3, "I")] #IMPARES

    #Recibe la direccion, el dato y el estado y busca un bloque para reemplazar de acuerdo a su asociatividad
    #Retorna el dato anterior y una bandera que indica si se debe hacer Write Back del mismo.
    def reemplazarBloque(self, dir, dato, estado):
        par = dir[-1] == '0'
        Writeback = False
        WBData = (None, None)
        if par:
            if self.way0[self.siguientePar].estado == 'O' or self.way0[self.siguientePar].estado == 'M':
                Writeback = True
                WBData = (self.way0[self.siguientePar].dir, self.way0[self.siguientePar].dato)
            self.way0[self.siguientePar].dir = dir
            self.way0[self.siguientePar].dato = dato
            self.way0[self.siguientePar].estado = estado

            if self.siguientePar == 0:
                self.siguientePar = 1
                return (0, Writeback, WBData)
            else:
                self.siguientePar = 0
                return (1, Writeback, WBData)
        else:
            if self.way1[self.siguienteImpar].estado == 'O' or self.way1[self.siguienteImpar].estado == 'M':
                Writeback = True
                WBData = (self.way1[self.siguienteImpar].dir, self.way1[self.siguienteImpar].dato)
            self.way1[self.siguienteImpar].dir = dir
            self.way1[self.siguienteImpar].dato = dato
            self.way1[self.siguienteImpar].estado = estado
            if self.siguienteImpar == 0:
                self.siguienteImpar = 1
                return (2, Writeback, WBData)
            else:
                self.siguienteImpar = 0
                return (3, Writeback, WBData)
       
    #Retorna el bloque indicado en forma de string
    def visualizacionBloque(self, bloque):
        return str(bloque.getNumero()) + ": " + str(bloque.getDir()) + "\t" + str(bloque.getDato()) + "\t" + bloque.getEstado()

    #Retorna la lista de bloques en forma de string
    def visualizacionBloques(self):
        datos = []
        datos.append(self.visualizacionBloque(self.way0[0]))
        datos.append(self.visualizacionBloque(self.way0[1]))
        datos.append(self.visualizacionBloque(self.way1[0]))
        datos.append(self.visualizacionBloque(self.way1[1]))
        return datos

    #Recibe la direccion y busca el bloque
    #Retorna None si no lo encuentra
    def leerBloque(self, dir):
        if (int(dir,2)%2 == 0):
            for i in range (0,2):
                if (self.way0[i].getDir() == dir):
                    return self.way0[i]
        else:
            for i in range (0,2):
                if (self.way1[i].getDir() == dir):
                    return self.way1[i]
        return None