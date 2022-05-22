'''
Melissa Arreola Pasos         00000216552
Itzel Haydeé Garza González   00000216628
'''

#Librería utilizada para el puerto serial
import serial
#Librería utilizada para la creación del hilo
import threading
#Librería para dar un tiempo de espera
import time
#Libreria para las estadisticas
import statistics as estadisticas
#Librería para crear elementos gráficos
from tkinter import *
#Libreria para las estadisticas
from matplotlib import pyplot as plt
#Libreria que nos ayudará con algunos cálculos
import numpy as np
#Librería que se usará para la conexión a la BD
import mysql.connector as pysql



class Main_Frame(Frame):

    def __init__(self, master=None):
        super().__init__(master,width=950, height=550)
        self.master = master
        self.pack()

        #Creación de un hilo para leer los datos del arduino constantemente
        self.hiloA = threading.Thread(target=self.leeArduino,daemon=True)

        #Se declara el arduino mediante el modulo "serial" y lo vinculamos al COM5
        self.arduino = serial.Serial('COM5',9600,timeout=5)
        time.sleep(1)

        '''
        Se establece la conexión a la BD
        '''
        self.pydb = pysql.connect(host='localhost', user='root', password='sesamo', database='sistema_incendios')

        #Se establece el objeto cursor
        self.mycursor = self.pydb.cursor()

        #Variable para contabilizar personas
        self.personas = int()
        self.personas = 0
        self.cantPersonas = StringVar()
        self.cantPersonas.set("0")
        #Variable para contabilizar incendios
        self.incendiosRegistrados = int()

        #variables para detectar si un tipo de incendio se activó
        self.incendioMayor = TRUE
        self.incendioMenor = FALSE

        #Variable para configurar temperatura
        self.temperatura = int()

        self.servoMotor = FALSE
        self.sensorLlama = FALSE

        self.modoIncendio = StringVar()

        self.statusIncendio = StringVar()
        self.color = StringVar()
        self.color.set("green3")

        #Método para cargar widgets de la interfaz
        self.createWidgets()
        #Se inicializa el hilo
        self.hiloA.start()

    def createWidgets(self):
        '''
        Función encargada de establecer los valores de los widgets en el frame principal
        :return: ningún valor
        '''
        #Se inserta la imagen
        #imagenPersona = ImageTk.PhotoImagen()

        #Se crean etiquetas para el contador de personas
        Label(self, text="Personas: ",bg="green3", font=("Arial", "11", "bold")).place(x=150, y=380)
        Label(self, text="                                                                  ", font=("Arial", "11", "bold")).place(x=250, y=380)
        Label(self, textvariable= self.cantPersonas, font=("Arial","11","bold")).place(x=300, y=380)
        Label(self, textvariable=self.modoIncendio, bg="green3",font=("Arial","11","bold")).place(x=400, y=10)
        self.modoIncendio.set("MODO: Incendio mayor")
        Label(self, textvariable= self.statusIncendio, bg=self.color.get(), font=("Arial", "11", "bold")).place(x=400, y=30)
        #Boton que despliega las estadisticas
        Button(self, text="Estadísticas", command=self.despliegaEstadisticas, font=("Arial", "11", "bold")).place(x=400, y=450)



    def despliegaEstadisticas(self):
        '''
        Funcion encargada de desplegar la grafica de barras para las estadisticas
        :return:
        '''
        # Se realiza una consulta a la bd de las personas afectadas por un incendio
        self.mycursor.execute('SELECT SUM(personas_afectadas) FROM incendios_registrados')
        # Se guardan los valores obtenidos
        personas_afectadas = self.mycursor.fetchall()

        # Se realiza una consulta a la bd de la cantidad de incendios registrados
        self.mycursor.execute('SELECT COUNT(*) FROM incendios_registrados')
        incendios_registrados = self.mycursor.fetchall()

        #Se crea un instancia del módulo matplotpy
        self.plt = plt

        plt.title('Incendios registrados y personas afectadas')
        datosPA = []
        datosIR = []
        datos = []
        contador = 0
        for x in personas_afectadas:
            datosPA.append(x[0])
        for x in incendios_registrados:
            datosIR.append(x[0])
        y = np.zeros(len(datos))
        for i in range(0):
            y[contador] = i
        self.plt.ion()

        #Se asignan etiquetas a las barras del eje x y valores para el eje y
        self.plt.bar('Personas afectadas',datosPA)
        self.plt.bar('Incendios registrados',datosIR)

        #Se muestra la gráfica
        plt.show()

    def insert(self, personas):
        pers = str(personas)
        sql = "INSERT INTO incendios_registrados (personas_afectadas) VALUES ("+pers+")"
        self.mycursor.execute(sql)
        self.pydb.commit()

    def leeArduino(self):
        '''
        Función encargada de leer el puerto serial de Arduino
        :return: ningún valor
        '''
        while True:

           dato = self.arduino.readline()[:-2]
           datoStr = str(dato)
           datoStr = datoStr.replace("b'", '').replace("'", '')
           print(datoStr)

           if datoStr != "":
               if (datoStr == '1'  or datoStr == '3' or datoStr == '4' or datoStr == '5' or datoStr == '6' or datoStr == '7'):
                   self.accion(datoStr)

    def accion(self, datoStr):
        if datoStr == '1': #Incendio
            self.incendiosRegistrados = self.incendiosRegistrados + 1
            self.sensorLlama = TRUE
            self.servoMotor = TRUE
            self.color.set("red3")
            self.statusIncendio.set("INCENDIO ACTIVO")
        if datoStr == '3' and self.sensorLlama == TRUE and self.servoMotor == TRUE: #Se apagó el incendio
            self.sensorLlama = FALSE
            self.servoMotor = FALSE
            self.insert(self.personas)
            self.personas = 0
            self.cantPersonas.set(self.personas)
            self.statusIncendio.set("")
            self.color.set("green3")
            time.sleep(2)
        if datoStr == '4':#Entró una persona
            self.personas = self.personas + 1
            self.cantPersonas.set(self.personas)
        if datoStr == '5':#Salió una persona
            if(self.personas > 0):
                self.personas = self.personas - 1
                self.cantPersonas.set(self.personas)
        if datoStr == '6': #Modo incendio menor
            self.modoIncendio.set("MODO: Incendio menor")
        if datoStr == '7': #Modo incendio mayor
            self.modoIncendio.set("MODO: Incendio mayor")


