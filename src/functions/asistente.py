import os

import speech_recognition as re
import pyttsx3 as voz
from nltk import TabTokenizer


import src.database.local as local
import pygame
import src as _
from os import path

from textblob import TextBlob
import string
import simpleaudio as sa
from textblob import Word
from textblob.wordnet import VERB
from os import path,stat
from src.functions.chat import conversation

vocales="aeiou"
spluarl ='asesos'
lverbo = 'arerir'
lvpasado= 'adoido'
lvfuturo = 'rárérás'

def sonido():
    ruta = path.join(_.DIRNAME, 'files/sound.wav')
    rutaf = ruta.replace('\\', '/')

    print("el directorio es {0}".format(rutaf))
    wave_obj = sa.WaveObject.from_wave_file(rutaf)
    play_obj = wave_obj.play()
    play_obj.wait_done()




def hablar(texto):
    lupita = voz.init()
    velocidad = lupita.getProperty('rate')
    lupita.setProperty('rate', velocidad-45)
    lupita.setProperty('voice', 'TTS_MS_ES-MX_SABINA_11.0') # voz con acento mexicano
    lupita.say(texto)
    lupita.runAndWait()



def interpretar(comando_de_audio):
    tokenizer = TabTokenizer()
    txt = TextBlob(comando_de_audio)

    print("el texto es {0}".format(str(txt)))
    a= txt.translate()
    result = a.sentiment
    print("sentimientos {0}".format(str(result)))

    b = TextBlob(comando_de_audio)
    b.words

    if result.polarity < -0.25 :
        hablar("no me gusta lo que dices")
    elif result.polarity < -0.50 :
        hablar("no me gusta lo que dices")
    elif result.polarity > -0.51 and result.polarity < -0.99:
        hablar("no estoy de acuerdo, eres muy negativo")
    elif result.polarity < 0.25:

        conversation(comando_de_audio)

    elif result.polarity > 0.50:
        hablar("tienes razón")
        conversation(comando_de_audio)

    #polaridad positivo o negativo
    #subjetividad
    # print(type(vd))

    joyinit()




def joyinit():

    r = re.Recognizer()
    with re.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:

        sonido()
        comando = r.recognize_google(audio, language='es-EC')

        print("Creo que dijiste: " + comando)


        interpretar(comando)  # lo que se debe hacer con el comando de audio

    except re.UnknownValueError:
        # si no se entendió
        #hablar('no has dicho nada')
        print("No te pude entender")
        joyinit()



    except LookupError as e:
        print('el error es {0}'.format(e))
        #hablar('error temporal')
        joyinit()
