import time
import os
import sys
import statistics

#For get the pip packeges in project directory.
sys.path.append(os.path.join(os.path.dirname(__file__), 'site-packages'))

#Import For Multi Thread
import concurrent.futures

#Import for Raspberry Pi
import RPi.GPIO as GPIO

#Import for HX711
from hx711 import hx711

#Setup for full screen
#Important set the small window size then full full screen.
from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '900')
from kivy.core.window import Window
#Window.fullscreen = True

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.clock import Clock

#Import for Japanese Font
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'noto-cjk/NotoSansJP-Regular.otf')

#Preference for HX711
hx = hx711.HX711(23, 24)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(111.5)
hx.reset()
hx.tare(79)

print("Tare done! Add weight now...")

#Like the common value
class CV():
    loopflag = True
    tareflag = False
    stableflag = False

    dispweight = 0
    currweight = 0
    prevweight = 0
    diffweight = 0
    sum1weight = 0
    sum2weight = 0
    saveweight = [0]

def SoundTare():
    os.system("aplay --quiet './sounds/Hard_Tech_Bass_A4.wav'")

def SoundSize6S():
    os.system("mpg321 --quiet './sounds/SoundSize6S.mp3'")

def SoundSize5S():
    os.system("mpg321 --quiet './sounds/SoundSize5S.mp3'")

def SoundSize4S():
    os.system("mpg321 --quiet './sounds/SoundSize4S.mp3'")

def SoundSize3S():
    os.system("mpg321 --quiet './sounds/SoundSize3S.mp3'")

def SoundSize2S():
    os.system("mpg321 --quiet './sounds/SoundSize2S.mp3'")

def SoundSizeS():
    os.system("mpg321 --quiet './sounds/SoundSizeS.mp3'")

def SoundSizeM():
    os.system("mpg321 --quiet './sounds/SoundSizeM.mp3'")

def SoundSizeL():
    os.system("mpg321 --quiet './sounds/SoundSizeL.mp3'")

def SoundSize2L():
    os.system("mpg321 --quiet './sounds/SoundSize2L.mp3'")

def SoundSize3L():
    os.system("mpg321 --quiet './sounds/SoundSize3L.mp3'")

def SoundSize4L():
    os.system("mpg321 --quiet './sounds/SoundSize4L.mp3'")

def SoundSize5L():
    os.system("mpg321 --quiet './sounds/SoundSize5L.mp3'")

def SoundSize6L():
    os.system("mpg321 --quiet './sounds/SoundSize6L.mp3'")

def SoundStable():
     os.system("aplay --quiet './sounds/Hard_Tech_Bass_A4.wav'")
     print("sound play")


def GetWeight():
    CV.saveweight.append(hx.get_weight(5))
    hx.reset()
    time.sleep(0.001)
    if len(CV.saveweight) > 9:
        del CV.saveweight[0]
    print(CV.saveweight)

#Get the weight from HX711
def CalcWeight():
    CV.loopflag = True

    while CV.loopflag:

        if CV.tareflag == True:
            hx.reset()
            hx.tare(39)
            del CV.saveweight[0:]
            CV.dispweight = 0
            CV.tareflag = False
            print("tared")

        else:
            GetWeight()
            midweight = statistics.median(CV.saveweight)
            goodweight = [e for e in CV.saveweight if -2 < midweight - e < 2 ]
            CV.currweight = statistics.mean(goodweight)
            print("Mid")
            print(midweight)
            print("+-2")
            print(goodweight)
            print("Weight")
            print(CV.currweight)

            if -2 < CV.currweight < 2:
#                executor.submit(SoundStable)
                CV.dispweight = 0
                print("around 0")

            elif CV.currweight < CV.prevweight + 1 and CV.currweight > CV.prevweight - 1:
                CV.dispweight = CV.prevweight
                CV.sum2weight = CV.prevweight
                CV.diffweight = CV.sum1weight - CV.sum2weight
                if CV.diffweight > 150:
                    CV.stableflag = False
                    executor.submit(SoundSize3L)
                elif CV.diffweight >= 111 and CV.diffweight < 150:
                    CV.stableflag = False
                    executor.submit(SoundSize2L)
                elif CV.diffweight >= 95 and CV.diffweight < 111:
                    CV.stableflag = False
                    executor.submit(SoundSizeL)
                elif CV.diffweight >= 80 and CV.diffweight < 95:
                    CV.stableflag = False
                    executor.submit(SoundSizeM)
                elif CV.diffweight >= 65 and CV.diffweight < 80:
                    CV.stableflag = False
                    executor.submit(SoundSizeS)
                elif CV.diffweight >= 55 and CV.diffweight < 65:
                    CV.stableflag = False
                    executor.submit(SoundSize2S)
                elif CV.diffweight > 10 and CV.diffweight < 55:
                    CV.stableflag = False
                    executor.submit(SoundSize3S)
                elif CV.diffweight >= -10 and CV.diffweight < 10:
                    CV.stableflag = False
                    print("same weight")
                elif CV.diffweight < -10:
                    CV.stableflag = False
                    executor.submit(SoundStable)
                #elif CV.diffweight <= 0:
                    #print("zero")

                else:
                    print("other")
                CV.sum1weight = CV.sum2weight

            else:
                CV.dispweight = CV.currweight
                CV.prevweight = CV.currweight
                print("movable")
                CV.stableflag = True

    print("Cleaning and Exit")
    GPIO.cleanup()
    sys.exit()

class LayoutAdd(BoxLayout):
    dispweight = NumericProperty(0)

    def __init__(self, **kwargs):
        super(LayoutAdd, self).__init__(**kwargs)
        Clock.schedule_interval(self.LabelWeight, 0.1)

    def LabelWeight(self, dt):
        self.dispweight = CV.dispweight

    def TareButton(self):
        CV.tareflag = True
        executor.submit(SoundTare)

    def ExitButton(self):
        CV.loopflag = False
        App.get_running_app().stop()

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title = 'Scaling!'

    def build(self):
        return LayoutAdd()

if __name__ == '__main__':
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    executor.submit(CalcWeight)
    MainApp().run()
