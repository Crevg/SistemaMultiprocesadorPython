from tkinter import *
from tkinter import messagebox
from tkinter import ttk
fontOpc =("Helvetica", 20)
fontCPU = ("Helvetica", 14)

#Clase que define la GUI
class App:

    def __init__(self, root):
        self.bgColor = "#b6d9f2"
        root.title = "Multiprocessing system"
        self.buttonColor = "#3a4991"
        self.blueC = "#4d55e3"
        self.yellowC = "#dcf56e"
        #frame inicial
        frame = Frame(root, bg=self.bgColor, width=1200, height=720)
        frame.pack_propagate(0)
        frame.pack()

        #frame cpus
        frameCPUs = Frame(frame, width=1200, height=270,  bg=self.bgColor, borderwidth = 1, relief=RAISED)
        frameCPUs.pack_propagate(0)
        frameCPUs.pack(side = TOP)

        #frame ind CPU
        frameCPU_1 = Frame(frameCPUs,  bg=self.bgColor,width=280, height=300)
        frameCPU_1.pack_propagate(0)
        frameCPU_1.pack(side = LEFT, padx=10)
        frameCPU_2 = Frame(frameCPUs,  bg=self.bgColor,width=280, height=300)
        frameCPU_2.pack_propagate(0)
        frameCPU_2.pack(side = LEFT, padx=10)
        frameCPU_3 = Frame(frameCPUs,  bg=self.bgColor,width=280, height=300)
        frameCPU_3.pack_propagate(0)
        frameCPU_3.pack(side = LEFT, padx=10)
        frameCPU_4 = Frame(frameCPUs,  bg=self.bgColor,width=280, height=300)
        frameCPU_4.pack_propagate(0)
        frameCPU_4.pack(side = LEFT, padx=10)

        self.CPULabels = [] #2 dimensiones. Listas de CPU#, Curr instr, next Instru
        self.setCPULabels(frameCPU_1, frameCPU_2, frameCPU_3, frameCPU_4)

        
        #frame memoria
        frameMem = Frame(frame, bg=self.bgColor, width=400)
        frameMem.pack_propagate(0)
        frameMem.pack(side = LEFT, pady=(10,0), padx= (50,0), fill= Y)

        self.MEMLabels = []
        self.setBloquesDeMemoria(frameMem)

        #frame opciones
        frameOpc = Frame(frame, bg=self.bgColor, width=800)
        frameOpc.pack_propagate(0)
        frameOpc.pack(side = RIGHT, fill= Y)

        #frame opcion individual

        frameOpc_1 = Frame(frameOpc, bg=self.bgColor, )
        frameOpc_1.pack(side = TOP, fill=X, pady=30)
        labelOpc_1 = Label(frameOpc_1, bg=self.bgColor, text="Ejecutar siguiente ciclo",font=fontOpc)
        labelOpc_1.pack( side = LEFT, padx=(150,0))
        self.buttonOpc_1 = Button(frameOpc_1, bg=self.buttonColor, relief=FLAT, fg = "white", highlightbackground="black", text="Ejecutar", command=None)
        self.buttonOpc_1.pack(side = RIGHT, padx=(0,100))


        frameOpc_2 = Frame(frameOpc,  bg=self.bgColor, height=140)
        frameOpc_2.pack(side = TOP, fill=X, pady=30)
        labelOpc_2 = Label(frameOpc_2,bg=self.bgColor,  text="Ejecutar varios ciclos",font=fontOpc)
        labelOpc_2.pack( side = LEFT, padx=(150,0))
        self.buttonOpc_2 = Button(frameOpc_2, bg=self.buttonColor,  relief=FLAT, fg = "white", highlightbackground="black", text="Ejecutar", command=None)
        self.buttonOpc_2.pack(side = RIGHT, padx=(0,100))
        self.entryOpc_2 = Entry(frameOpc_2, width=3, font=fontOpc)
        self.entryOpc_2.pack(side = RIGHT, padx= (0,20))
 


        frameOpc_3 = Frame(frameOpc, bg=self.bgColor, )
        frameOpc_3.pack(side = TOP, fill=X, pady=30)
        labelOpc_3 = Label(frameOpc_3, bg=self.bgColor, text="Ejecutar indefinidamente", font=fontOpc)
        labelOpc_3.pack( side = LEFT, padx=(150,0))
        self.buttonOpc_3 = Button(frameOpc_3,bg=self.buttonColor, relief=FLAT, fg = "white", highlightbackground="black", text="Ejecutar", command=None)
        self.buttonOpc_3.pack(side = RIGHT, padx=(0,100))
        self.buttonPausaOpc_2 = Button(frameOpc_3,bg=self.buttonColor, relief=FLAT,fg = "white", highlightbackground="black",     text="Pausar", command=None)
        self.buttonPausaOpc_2.pack(side = RIGHT, padx= (0,20))

    #Funcion utilizada para inicializar la lista de labels con la informacion del CPU y sus instrucciones
    def setCPULabels(self, frame1, frame2, frame3, frame4):
        c = 0
        self.CPULabels.append(self.setCPULabelsAux(frame1, 1))
        self.CPULabels.append(self.setCPULabelsAux(frame2, 2))
        self.CPULabels.append(self.setCPULabelsAux(frame3, 3))
        self.CPULabels.append(self.setCPULabelsAux(frame4, 4))
        return        

    #Funcion auxiliar de CPU labels para 1 unico cuadro de CPU
    def setCPULabelsAux(self, frame, number):
        listaLabels = [] 
        listaLabels.append(Label(frame, bg=self.bgColor, anchor='w', text= "CPU# " + str(number)))  #0
        listaLabels[-1].pack(side=TOP, fill=X)
        prevInstruc = Label(frame, bg=self.bgColor, anchor='w') #10
        prevInstruc.pack(side=TOP, fill=X)
        listaLabels.append(Label(frame, bg=self.bgColor, anchor='w')) #1
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame, bg=self.bgColor,  anchor='w')) #2
        listaLabels[-1].pack(side=TOP, fill=X, pady= (0,10))
        cacheHeader = Label(frame,  anchor='w', text="Bloque #   Dir\tDato\tEstado", borderwidth=2, relief="raised", bg=self.bgColor,) #NaN
        cacheHeader.pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='w', bg=self.yellowC, borderwidth=2, relief="sunken", )) #3
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='w' ,bg=self.yellowC, borderwidth=2, relief="sunken", ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='w',bg = self.blueC ,   fg ="white", borderwidth=2, relief="sunken"  )) #5
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='w' ,bg = self.blueC ,   fg ="white", borderwidth=2, relief="sunken" )) #6
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame, bg=self.bgColor,  anchor='w', text="Agregar la siguiente instrucción" )) #7
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Entry(frame, width=16)) #8
        listaLabels[-1].pack(side=LEFT, anchor="nw", padx=5, ipady=3)
        listaLabels.append(Button(frame,bg=self.buttonColor, relief=FLAT,  fg = "white", highlightbackground="black", text="Agregar")) #9
        listaLabels[-1].pack(side=LEFT, anchor="n", padx=5)       
        listaLabels.append(prevInstruc) # adding 10

        return listaLabels


    #Agrega los labels de los bloques de memoria 
    def setBloquesDeMemoria(self, frame):

        listaLabels = []
        listaLabels.append(Label(frame,  anchor='center',bg=self.bgColor, relief="raised", borderwidth=2, text="Bloques de memoria", font=fontCPU))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center',  bg=self.yellowC,borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center', bg = self.blueC ,   fg ="white", borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center',  bg=self.yellowC, borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center', bg = self.blueC ,   fg ="white", borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center',  bg=self.yellowC,borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center',  bg = self.blueC ,   fg ="white", borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center',  bg=self.yellowC,borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center',  bg = self.blueC ,   fg ="white", borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center',  bg=self.yellowC,borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center',  bg = self.blueC ,   fg ="white", borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center',  bg=self.yellowC,borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center',  bg = self.blueC ,   fg ="white", borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center', bg=self.yellowC, borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center',  bg = self.blueC ,   fg ="white", borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center',  bg=self.yellowC,borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        listaLabels.append(Label(frame,  anchor='center', bg = self.blueC ,   fg ="white",  borderwidth=3, relief="sunken" ))
        listaLabels[-1].pack(side=TOP, fill=X)
        for i in range (0, len(listaLabels)):
            listaLabels[i].configure(borderwidth=2)
        self.MEMLabels = listaLabels

    #Retorna la lista de labels de todos los CPUs
    def getCPULabels(self, CPUNumber):
        return self.CPULabels[CPUNumber-1]

    #Muestra un msj de error
    def showError(self, err):
        messagebox.showerror("Error", err)

