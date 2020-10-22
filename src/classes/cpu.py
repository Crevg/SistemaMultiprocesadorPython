from .control import Control
import threading
from time import sleep
import random
import numpy as np

hexVar = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'] #Variable con los valores hex posibles a utilizar

#Clase del CPU que es ejecutada por 1 hilo por instancia
class Processor(threading.Thread):
    #Recibe
    ##refresh: Callback para refrescar GUI
    ##number: El numero de CPU a asignar
    ##runType: El tipo de ejecucion (False 1 ciclo, True más)
    ##enable: Callback para habilitar o deshabilitar input de la GUI
    ##cache: Referencia al cache
    ##control: Referencia al control
    ##ciclos: Cantidad de ciclos: 1 por defecto
    #No recibe pero incializa:
    ##instruccion actual, siguiente y anterior, bandera de pausa y bandera de corriendo
    def __init__(self, refresh, number, runType, enable, cache, control, cycles=1):
        threading.Thread.__init__(self)
        self.number = number
        self.running = False
        self.instruccionActual = ""
        self.siguienteInstruccion = ""   
        self.anteriorInstruccion = ""     
        self.cache = cache
        self.control =  control
        self.runType = runType
        self.cycles = cycles
        self.pausa = False
        self.refresh = refresh
        self.enable = enable

    #Funcion que se ejecuta cuando se inicia el hilo, tiene el ciclo de ejecucion de acuerdo
    #al tipo de corrida
    def run(self):
        self.enable("disabled")
        self.running = True
        shouldContinue = bool(self.runType)
        i = 0
        if (self.siguienteInstruccion == ""):
            self.ejecutarInstruccion()
        while(self.running and (shouldContinue or (i < self.cycles))):
            print(self.anteriorInstruccion)
            if self.runType == 1 and i >= self.cycles:
                shouldContinue = False
                break
            self.ejecutarInstruccion()
            i += 1
            if (self.pausa):
                break
        self.anteriorInstruccion = self.instruccionActual
        self.instruccionActual = ""
        self.refresh()
        self.running = False
        self.enable("normal")

    #Detiene la ejecuión
    def stop(self):
        self.pausa = True
    #Setters y getters
    def getCache(self):
        return self.cache

    def getInstruccionActual(self):
        return self.instruccionActual

    def getSiguienteInstruccion(self):
        return self.siguienteInstruccion

    def setSiguienteInstruccion(self, instr):
        self.siguienteInstruccion = instr

    def getAnteriorInstruccion(self):
        return self.anteriorInstruccion

    #Genera la siguiente instruccion de acuerdo a distribucion normal
    #Si es necesario genera direccion y valor para sus instrucciones
    def generarInstruccion(self):
        op = np.random.normal(1,1,1)
        if op > 2:
            op = "WRITE"
        elif op < 0:
            op = "READ"
        else:
            op = "CALC"

        if op == "CALC":
            return op
        else:
            dirDeBloque = np.random.poisson(2,1)
            if dirDeBloque <= 3:
                pass
                #direccion = USE CACHE[dirDeBloque]
            else:
                pass
                #Direccion = DO NOT USE CACHE (map 4 cache address out of the dist)
            direccion = random.randrange(0, 15)
            op = op + " " + bin(direccion)[2:].zfill(4)
            if (op[:5] == "WRITE"):
                op = op + ";"
                for i in range (0,4):
                    op = op + random.choice(hexVar)                
            return op

    #Ejecuta la instruccion siguiente
    def ejecutarInstruccion(self):
        self.anteriorInstruccion = self.instruccionActual
        self.instruccionActual = self.siguienteInstruccion
        self.siguienteInstruccion = self.generarInstruccion()
        self.refresh()
        sleep(0.5)
        if self.instruccionActual != "":
            if self.instruccionActual[0] == "R":
                self.ejecutarRead()
            elif self.instruccionActual[0] == "C":
                self.ejecutarCalc()
            else:
                self.ejecutarWrite()

    #Ejecuta la instruccion read
    def ejecutarRead(self):
        sleep(1)
        dir = self.instruccionActual.split()[1]
        bloqueCache = self.cache.leerBloque(dir)
        if bloqueCache == None:
            self.control.readMiss(self.number, dir, False)
        elif bloqueCache.getEstado() == "I":
            self.control.readMiss(self.number, dir, True)
        else: 
            if bloqueCache.getEstado() == 'S':
                self.control.readHit(self.number, dir)

    #Ejecuta la instruccion write
    def ejecutarWrite(self):
        sleep(1)
        inst = self.instruccionActual.split()[1].split(";")
        dir = inst[0]
        data = inst[1]               
        bloqueCache = self.cache.leerBloque(dir)
        if (bloqueCache == None):
            self.control.writeMiss(self.number, dir, data)
        else: 
            self.control.writeHit(self.number, bloqueCache, data)
    #Ejecuta la instruccion calc
    def ejecutarCalc(self):
        sleep(2)