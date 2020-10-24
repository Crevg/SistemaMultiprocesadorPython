#Controlador de cache utilizado para mantener coherencia 
class Control:
    #Recibe la referencia a la cache y la referencia al bus, inicializa los 4 tags como vacios
    def __init__(self, cache, bus): 
        self.cache = cache
        self.bloques = [None,None,None,None]
        self.bus = bus

    #Recibe la direccion y retornar el bloque de cache de esa direccion, si no lo encuentra retorna None
    def leerBloque(self, dir):
        encontrado = False
        for i in range (0, len(self.bloques)):
            if self.bloques[i] == dir:
                encontrado = True
                break
        if  encontrado:
            return self.cache.leerBloque(dir)
        return None

    #Tras un read miss recibe el numero de procesador, direccion y boolean si el estado es invalido o no
    #Envia el read miss al bus y actualiza el cache con el dato correspondiente
    def readMiss(self, num, dir, I):
        bloque =  self.bus.readMiss(num, dir)
        if (I):
            nuevoBloque = self.cache.leerBloque(dir)
            nuevoBloque.setDato(bloque[0])            
            nuevoBloque.setEstado(bloque[1])
        else:
            self.reemplazoCache(dir, bloque[0], bloque[1])

    #Recibe el num de procesador y la direccion y envia la busqueda de un O al bus si el dato fue S 
    def readHit(self, num, dir):
        bloque = self.bus.readHit(num, dir)
        if bloque[0]:
            return bloque[1]
    #Recibe el num de proce, la direccion y el dato, envia el write miss al bus y escribe en cache el dato.
    def writeMiss(self, num, dir, data):
        self.bus.writeMiss(num, dir)
        self.reemplazoCache(dir, data, "M")

    #Recibe el num de proce, el bloque y el dato, escribe el dato y envia la invalidacion al cache.
    def writeHit(self, num, bloque, data):
        estado = bloque.getEstado()
        if estado == "E":                       #E -> M P
            bloque.setEstado("M")
            bloque.setDato(data)
        elif estado == "O":                     # O -> O P
            bloque.setDato(data)
        else: #M,S,I
            bloque.setDato(data)            # M -> M , S -> M, I -> M P
            bloque.setEstado("M")    
            self.bus.writeHit(num, bloque.getDir())
           
    #Recibe la direccion el dato y el estado y escribe el bloque en cache reemplazando a otro.
    def reemplazoCache(self, dir, dato, estado):
        numero = 0
        reemplazo = self.cache.reemplazarBloque(dir, dato, estado)
        self.bloques[reemplazo[0]] = dir
        if reemplazo[1]:
            self.bus.writeBack(reemplazo[2])