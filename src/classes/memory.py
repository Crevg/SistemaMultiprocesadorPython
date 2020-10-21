import random as r
from time import sleep

hexVar = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

#Clase que implementa la Memoria del sistema
class Memory:
    #Crea la lista de bloques de memoria y los inicializa
    def __init__(self):
        self.bloques = []
        self.initBloques()

    #Inicializa los bloques de memoria con 0s
    def initBloques(self):
        for i in range(0, 16):
            dato = ""
            for j in range(0, 4):
                dato= dato + '0' #r.choice(hexVar) # 
            self.bloques.append(dato)

    #Obtiene todos los bloques de memoria de manera inmediata para visualizacion
    def obtenerDatos(self):
        datos = []
        for i in range (0,16):
            datos.append( (bin(i)[2:].zfill(4), self.bloques[i]))
        return datos
    #Recibe la direccion y lee el bloque de memoria con delay de Mem Wall
    def leerBloque (self, num):
        index = int(num, 2)
        sleep(5)
        return self.bloques[index]

    #Recibe la direccion y el dato y escribe un bloque de memoria con delay de Mem Wall
    def escribirBloque (self, num, nuevoDato):
        index = int(num, 2)
        sleep(5)
        self.bloques[index] = nuevoDato
