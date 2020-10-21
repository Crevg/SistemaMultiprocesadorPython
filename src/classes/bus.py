from threading import Lock
from time import sleep

#Bus único de acceso a memoria y que se utiliza para hacer snooping de los tags de los bloques de caché
#Utiliza Mutex para asegurar acceso único

class Bus:
    #Recibe referencia a la lista de procesadores y a la memoria, inicializa el mutex
    def __init__(self, cpuList, mem):
        self.cpuList = cpuList
        self.mem = mem
        self.mutex = Lock()

    #Broadcast de read miss a los demás controladores
    def readMiss(self, cpuN, dir):
        self.mutex.acquire()
        sleep(1)
        dato = None
        try:
            dato = None
            encontrado = False
            print(cpuN)
            for i in range (0, len(self.cpuList)):
                if i == (cpuN-1):
                    continue
                bloque = self.cpuList[i].control.leerBloque(dir)
                if (bloque == None):
                    continue
                estadoBloque = bloque.getEstado()
                if (estadoBloque == "O"):  # O -> O B
                    encontrado = True 
                    dato = (bloque.getDato(), "S")
                elif (estadoBloque == "S"):
                    dato = (bloque.getDato(), "S") # S -> S B 
                elif (estadoBloque == "E"):
                    dato = (bloque.getDato(), "S") 
                    bloque.setEstado("S")     #E -> S B
                    encontrado = True
                elif(estadoBloque == "M"):
                    dato = (bloque.getDato(), "S")
                    bloque.setEstado("O")     #M -> S B
                    encontrado = True
                
                if (encontrado):
                    break

            return dato                               # I -> S P
        except:
            print("Read Miss Error")
        finally:
            if (dato == None):
                dato = self.mem.leerBloque(dir)
                self.mutex.release()                     
                return (dato, "E") 
            self.mutex.release()                        # I -> E
            return dato                          # I -> E P

    #Broadcast de Write Miss a los demás controladores
    def writeMiss(self,cpuN, dir):
        self.mutex.acquire()
        sleep(1)
        try:
            for i in range (0, len(self.cpuList)):
                if i == (cpuN-1):
                    continue
                bloque = self.cpuList[i].control.leerBloque(dir)
                if (bloque == None):
                    continue
                estadoBloque = bloque.getEstado()
                if estadoBloque == "M" or estadoBloque == "O":
                    self.writeBack((dir, bloque.getDato()))
                bloque.setEstado("I")  # E,M,S,I,O -> I B
        except:
            print ("Write miss error")
        finally:
            self.mutex.release()   

    #Broadcast de invalidación a los demás procesadores
    def writeHit(self, cpuN, dir):
        self.mutex.acquire()
        sleep(1)
        try:
            for i in range (0, len(self.cpuList)):
                if i == (cpuN-1):
                    continue
                bloque = self.cpuList[i].control.leerBloque(dir)
                if (bloque == None):
                    continue
                estadoBloque = bloque.getEstado()
                if estadoBloque == "S" or estadoBloque == "E":
                    bloque.setEstado("I")  # S - > I B
                elif estadoBloque == "M" or estadoBloque == "O":
                    bloque.setEstado("I")  # M -> I, O -> I  B
                    self.writeBack((dir, bloque.getDato()))
        except:
            print("Write Hit error")
        finally:
            self.mutex.release()   

    #Se llama cuando hay un read hit pero el dato esta en S para buscar si otro tiene copia en O
    def readHit(self, cpuN, dir):
        self.mutex.acquire()
        sleep(1)
        try:
            dato = None
            encontrado = False
            for i in range (0, len(self.cpuList)):
                if i == (cpuN-1):
                    continue
                bloque = self.cpuList[i].control.leerBloque(dir)
                if (bloque == None):
                    continue
                estadoBloque = bloque.getEstado()
                if (estadoBloque == "O"):  # O -> O B
                    encontrado = True 
                    dato = bloque.getDato()       
                    break
      
        except:
            print("Read hit error")
        if not encontrado:
            self.mutex.release()
            return (False, None)
        self.mutex.release()
        return (True, dato)

    #Hace Writeback del bloque a memoria
    def writeBack(self, bloque):
        print("WB", bloque)
        self.mem.escribirBloque(bloque[0], bloque[1])