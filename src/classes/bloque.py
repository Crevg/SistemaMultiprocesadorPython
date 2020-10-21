#Bloque de cache
class Bloque:
    #Inicializa el dato, la direccion, el numero y estado
    def __init__(self, dato, dir, numero, estado):
        self.dato = dato
        self.dir = dir
        self.numero = numero
        self.estado = estado

    #Setters y Getters
    def setEstado(self, estado):
        self.estado = estado

    def getEstado(self):
        return self.estado

    def getNumero (self):
        return self.numero

    def getDato(self):
        return self.dato

    def setDato(self, dato):
        self.dato = dato

    def getDir(self):
        return self.dir
