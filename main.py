import time
import os
import sys

#For get the pip packeges in project directory.
sys.path.append(os.path.join(os.path.dirname(__file__), 'site-packages'))

#Import For Multi Thread
import concurrent.futures

#Import for Raspberry Pi
import RPi.GPIO as GPIO

#Import for HX711
from hx711 import hx711

#Configuration for window size
from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')

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
hx = hx711.HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(81)
hx.reset()
hx.tare(79)

print("Tare done! Add weight now...")

#Like the global value
class CommonValue():
    flugloop = True
    weight = 0

#Get the weight from HX711
def WeightGet():
    CommonValue.flugloop = True
    while CommonValue.flugloop:
        CommonValue.weight = hx.get_weight(79)
        hx.power_down()
        hx.power_up()
        time.sleep(0.01)
        print(CommonValue.weight)
    print("Cleaning and Exit")
    GPIO.cleanup()
    sys.exit()


class LayoutAdd(BoxLayout):
    weight = NumericProperty(0)

    def __init__(self, **kwargs):
        super(LayoutAdd, self).__init__(**kwargs)
        Clock.schedule_interval(self.LabelWeight, 0.1)

    def LabelWeight(self, dt):
        self.weight = CommonValue.weight

    def ButtonTare(self):
        hx.reset()
        hx.tare(19)

    def ButtonExit(self):
        CommonValue.flugloop = False
        App.get_running_app().stop()

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title = 'Scaling!'

    def build(self):
        return LayoutAdd()

if __name__ == '__main__':
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    executor.submit(WeightGet)
    MainApp().run()
