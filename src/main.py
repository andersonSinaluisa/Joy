import time
from threading import Thread
from tkinter import *
from tkinter import ttk
import subprocess as sub
import importlib.machinery



import src.functions.asistente as asistente
import src.database.local as local



import src as _
from os import path,stat


from subprocess import Popen
def main():

    tim = BgCLI()
    tim.start()
    timer = BackgroundTimer()
    timer.start()

    asistente.hablar('Bienvenido')

    asistente.joyinit()








class BackgroundTimer(Thread):
   def run(self):
        time.sleep(2)

        exeServer = path.join(_.DIRNAME, 'comands/server.bat')
        exe_ = exeServer.replace('\\', '/')
        sub.call(exe_)

class BgCLI(Thread):
    def run(self):
        time.sleep(5)

        exeClient = path.join(_.DIRNAME, 'comands/entrada.bat')
        exef = exeClient.replace('\\', '/')
        sub.call(exef)


if __name__ == '__main__':
    main()
