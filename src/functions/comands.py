import subprocess as sub
from time import sleep
import pyautogui as auto
import pyttsx3 as voz
from comtypes.safearray import numpy as np

import src as _
from os import path
import src.functions.asistente as asis
import speech_recognition as re
from random import randint, uniform,random

from src.functions.NeuronalNetwork import NeuralNetwork


def notas():

    hablar('Estoy lista para escribir tu texto ')
    asis.sonido()
    listenRead()




def youtube():
    exe = path.join(_.DIRNAME,'comands/video.bat')
    exef = exe.replace('\\','/')
    sub.call(exef)
    hablar('abriendo youtube')
    return None



def hablar(texto):
    lupita = voz.init()
    velocidad = lupita.getProperty('rate')
    lupita.setProperty('rate', velocidad-20)
    lupita.setProperty('voice', 'TTS_MS_ES-MX_SABINA_11.0') # voz con acento mexicano
    lupita.say(texto)
    lupita.runAndWait()

def listenRead():

    r = re.Recognizer()
    with re.Microphone() as source:

        r.adjust_for_ambient_noise(source)
        print("¡Ordena!")
        hablar("puedes hablar lo que quieres que escriba")
        audio = r.listen(source)

    try:
        comando = r.recognize_google(audio,language='es-EC')
        hablar(comando)
        escribir(comando) # lo que se debe hacer con el comando de audio

    except re.UnknownValueError:
    #si no se entendió
      print("No te pude entender")
      hablar('No te pude entender')
      listenRead()

    except LookupError as e:
        print('no entendí repite de nuevo')
        hablar('no entendí repite de nuevo')
        listenRead()



def escribir(text):
    sub.call('start notepad.exe', shell=True)
    print(text)
    hablar(text)
    hablar('listo')
    auto.write(text)
    







def tablas_comand():
    var='7'
    hablar('esta es la tabla del {0}'.format(var))
    a = int(var)
    for i in range(0,11):
        resultado = i* a
        hablar("{0} por {1}  {2}".format(str(var),str(i),str(resultado)))




def learning():
    nn = NeuralNetwork([2, 3, 2], activation='tanh')
    X = np.array([[0, 0],  # sin obstaculos
                  [0, 1],  # sin obstaculos
                  [0, -1],  # sin obstaculos
                  [0.5, 1],  # obstaculo detectado a derecha
                  [0.5, -1],  # obstaculo a izq
                  [1, 1],  # demasiado cerca a derecha
                  [1, -1]])  # demasiado cerca a izq

    y = np.array([[0, 1],  # avanzar
                  [0, 1],  # avanzar
                  [0, 1],  # avanzar
                  [-1, 1],  # giro izquierda
                  [1, 1],  # giro derecha
                  [0, -1],  # retroceder
                  [0, -1]])  # retroceder
    nn.fit(X, y, learning_rate=0.03, epochs=15001)

    index = 0
    for e in X:
        print("X:", e, "y:", y[index], "Network:", nn.predict(e))
        index = index + 1





