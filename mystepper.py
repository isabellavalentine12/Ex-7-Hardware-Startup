import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from pidev.MixPanel import MixPanel
from pidev.kivy import DPEAButton
spi = spidev.SpiDev()

# Init a 200 steps per revolution stepper on Port 0
s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=3)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'mystepper'

class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White

class MainScreen(Screen):
    press_number = 0
    direction_value = 0
    direction_number = 0

    def turn_on_off(self):
        if s0.is_busy() == True:
            s0.go_until_press(self.direction_value, int(100 + (round(self.slideeer.value, 0) / 30 * 6400)))
        if self.press_number%2 == 0:
            print('Speed in steps per second:' , int(100+(round(self.slideeer.value, 0)/30*6400)))
            s0.go_until_press(self.direction_value, int(100+(round(self.slideeer.value, 0)/30*6400))) #second argument is in steps per second
            #s0.go_until_press(self.direction_value, 3*6400)
            self.turn_on_off_button.text = "Off"
        else:
            s0.softStop()
            self.turn_on_off_button.text = "On"
        self.press_number += 1

    def direction_changer(self):
        if s0.is_busy() == True:
            #s0.go_until_press(self.direction_value, 3 * 6400)
            s0.go_until_press(self.direction_value, int(100 + (round(self.slideeer.value, 0) / 30 * 6400)))
        else:
            print("s0 is not running")

        if self.direction_number%2 == 0:
            self.direction_value = 1
        else:
           self.direction_value = 0
        self.direction_number += 1

    def slideeer_action(self):
        print("slider value = " , self.slideeer.value)
        if self.turn_on_off_button.text == 'Off':
            s0.go_until_press(self.direction_value, int(100 + (round(self.slideeer.value, 0) / 30 * 6400)))
        else:
            print('stepper motor is off')

    #def fun(self):


Builder.load_file('mystepper.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))

def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
