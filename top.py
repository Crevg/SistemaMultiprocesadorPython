from src.classes.bloque import Bloque
from src.classes.cache import Cache
from src.classes.cpu import Processor
from src.classes.control import Control
from src.classes.memory import Memory
from src.classes.bus import Bus
from time import sleep
from window import App
from tkinter import *




#####################################################################################
####################################################################################
#    Este script se encarga de crear, inicializar, mantener y conectar las
#    distintas clases entre si y ejecutar y detener el sistema cuando
#    sea necesario 
#####################################################################################



########################Inicializacion de variables

base_cpu_labels = ["CPU# ", "Instrucción actual: ", "Instrucción siguiente: " , "Bloque ", "Bloque ", "Bloque ", "Bloque "] #Lista de los labels a actualizar de CPU
nextInstruction = ["","","",""] #Lista de instrucciones siguientes
cpu_list = []  #Lista de CPUs
cache_list = [] #Lista de caches
control_list = [] #Lista de controladores
memoria = Memory() #Referencia a memoria
bus = Bus(cpu_list, memoria ) #Referencia al bus

#Le asigna los caches a los controladores
for i in range (0,4):
    cache_list.append(Cache())
    control_list.append(Control(cache_list[i], bus))

#Inicializa la ventana
root = Tk()
app = App(root)


########################Creación y detención de CPU

#Crear los threads
def crear_cpu(number, runType, cycles=1):
    return Processor(setVars, number, runType, habilitarBotones, cache_list[number-1], control_list[number-1], cycles)

#Inicia la ejecución de los CPUs
def iniciar_cpu(cpu):
    cpu.start()

#Detiene explicitamente la ejecucion de los CPUs 
def detener_cpu(cpu):
    cpu.stop()
    cpu.join()



#Refrescar los labels y botones de la GUI cuando ocurre alguna acción que lo requiera

#Valor inicial de los labels
def setVarsDefault():
    app.buttonPausaOpc_2["state"]="disabled"
    app.buttonPausaOpc_2["text"]= "Pausar"
    for i in range(1, len(base_cpu_labels)):
        setVarsAux(1, i, "")
        setVarsAux(2, i, "")
        setVarsAux(3, i, "")
        setVarsAux(4, i, "")

#Valos de los labels en cada ciclo
def setVars():
    for i in range (0,4):
        bloques = cache_list[i].visualizacionBloques()
        setVarsAux(i+1, 1, cpu_list[i].getInstruccionActual())
        setVarsAux(i+1, 2, cpu_list[i].getSiguienteInstruccion())
        setVarsAux(i+1, 3, bloques[0])
        setVarsAux(i+1, 4, bloques[1])
        setVarsAux(i+1, 5, bloques[2])
        setVarsAux(i+1, 6, bloques[3])
        nextInstruction[i] = cpu_list[i].getSiguienteInstruccion()
    setLabelsMemoria()

#Actualiza el label indicado
def setVarsAux(cpuN, index, CPUinfo):
    updated = base_cpu_labels[index] + CPUinfo
    if app.getCPULabels(cpuN)[index]["text"] != updated:
        app.getCPULabels(cpuN)[index]["text"] = base_cpu_labels[index] + CPUinfo

#Set labels de memoria
def setLabelsMemoria():
    bloquesIniciales = memoria.obtenerDatos()
    for i in range (1, 17):
        app.MEMLabels[i]["text"] = "Bloque " + bloquesIniciales[i-1][0] + ": \t" + bloquesIniciales[i-1][1]


#Deshabilita los botones de GUI dependiendo del estado de la aplicación
def habilitarBotones(estado):
    isRunning = False
    for i in range(0, len(cpu_list)):
        isRunning = isRunning or cpu_list[i].running
    if isRunning and estado == "normal":
        pass
    else:
        app.buttonOpc_1["state"] = estado
        app.buttonOpc_2["state"] = estado
        app.buttonOpc_3["state"] = estado
        app.entryOpc_2["state"] = estado
        for i in range (0,4):
            app.getCPULabels(i+1)[8]["state"] = estado
            app.getCPULabels(i+1)[9]["state"] = estado
        if (estado == "normal"):
            app.buttonPausaOpc_2["state"]="disabled"
        else:
            app.buttonPausaOpc_2["state"]="normal"

#############################################Funciones de ejecucion

#Ejecuta únicamente el siguiente ciclo de los procesadores
def siguiente_ciclo(nextInstruction=nextInstruction):
    for i in range(0,len(cpu_list)):
        cpu_list[i].join()
    cpu_list.clear()
    for i in range(0,4):
        cpu_list.append(crear_cpu(i+1, 0))
        cpu_list[i].setSiguienteInstruccion(nextInstruction[i])
        cpu_list[i].start()
    nextInstruction = ["","","",""]
    setVars()

#Ejecuta la cantidad de ciclos indicados 
def varios_ciclos(nextInstruction=nextInstruction):
    for i in range(0,len(cpu_list)):
        cpu_list[i].join()
    cycles = 0
    try:
        cycles = int(app.entryOpc_2.get())
    except:
        app.showError("Inserte un número válido de ciclos.")
        return
    cpu_list.clear()
    for i in range(0,4):
        cpu_list.append(crear_cpu(i+1, 1, cycles))
        cpu_list[i].setSiguienteInstruccion(nextInstruction[i])
        cpu_list[i].start()
    nextInstruction = ["","","",""]
    setVars()

#Ejecuta el sistema hasta que se pause
def indefinido(nextInstruction=nextInstruction):
    for i in range(0,len(cpu_list)):
        cpu_list[i].join()
    cpu_list.clear()
    for i in range(0,4):
        cpu_list.append(crear_cpu(i+1, 2))
        cpu_list[i].setSiguienteInstruccion(nextInstruction[i])
        cpu_list[i].start()
        nextInstruction[i]
    setVars()

#Pausa el sistema al finalizar este ciclo
def pausar_reanudar():
    app.buttonPausaOpc_2["state"]="disabled"
    for i in range (0,4):
        cpu_list[i].stop()       

#Asigna la siguiente instruccion a ejecutar a un procesador
def asignarInst(cpuN):
    instru = app.getCPULabels(cpuN)[8].get().split()
    if len(instru) == 1 and instru[0] == "CALC":
        try:
            nextInstruction[cpuN-1] = instru[0]
        except:
            return
    elif len(instru) == 2 and instru[0] == "READ" and len(instru[1]) == 4:
        
        try:
            dire = int(instru[1], 2)
            nextInstruction[cpuN-1] = " ".join(instru)
        except:
            return
        
    elif len(instru) == 2 and instru[0] == "WRITE" :
        predicado = instru[1].split(";")
        if len(predicado) == 2 and len(predicado[0]) == 4 and len(predicado[1]) == 4:
            try:
                dire = int(predicado[0],2)
                hexN = int(predicado[1], 16)
                nextInstruction[cpuN-1] = " ".join(instru)
            except:
                return   
        else:
            return
    else:
        return
    app.getCPULabels(cpuN)[8].delete(0, END)


##########################################Asignar las funciones de ejecución a los botones de la GUI

app.buttonOpc_1["command"]=siguiente_ciclo
app.buttonOpc_2["command"]=varios_ciclos
app.buttonOpc_3["command"]=indefinido
app.buttonPausaOpc_2["command"]=pausar_reanudar
app.getCPULabels(1)[9]["command"]= lambda: asignarInst(1)
app.getCPULabels(2)[9]["command"]= lambda: asignarInst(2)
app.getCPULabels(3)[9]["command"]= lambda: asignarInst(3)
app.getCPULabels(4)[9]["command"]= lambda: asignarInst(4)

#########################################Llamadas a funciones iniciales y mainloop
setLabelsMemoria()
setVarsDefault()
root.mainloop()