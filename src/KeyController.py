from keyHardwareInput import *
from time import *
from enderecos import *
from threading import *
import time
class keyController(object):
    pressed= []

    def __init__(self):
        sleep(5)
        for i in range(0,10):
            self.pressed.append(False)

    def pressionar(self,teclas):
        threads = []
        if teclas[0]==True:
            threads.append(Thread(target=self.pressionaeSolta,args=[UP]))

        if teclas[1]==True:
            threads.append(Thread(target=self.pressionaeSolta,args=[DOWN]))

        if teclas[2]==True:
            threads.append(Thread(target=self.pressionaeSolta,args=[LEFT]))

        if teclas[3]==True:
            threads.append(Thread(target=self.pressionaeSolta,args=[RIGHT]))

        if teclas[4]==True:
            threads.append(Thread(target=self.pressionaeSolta,args=[A]))

        if teclas[5]==True:
            threads.append(Thread(target=self.pressionaeSolta,args=[B]))

        if teclas[6]==True:
            threads.append(Thread(target=self.pressionaeSolta,args=[C]))

        if teclas[7]==True:
            threads.append(Thread(target=self.pressionaeSolta,args=[X]))

        if teclas[8]==True:
            threads.append(Thread(target=self.pressionaeSolta,args=[Y]))

        if teclas[9]==True:
            threads.append(Thread(target=self.pressionaeSolta,args=[Z]))

        for thread in threads:
            try:
                if (active_count()<=4):
                    thread.start()
            except Exception as e:
                print(e)

    def pressionaeSolta(self,key):
        self.pressKey(key)
        time.sleep(0.2)
        self.releaseKey(key)

    def pressKey(self,hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def releaseKey(self,hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0,
                            ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))