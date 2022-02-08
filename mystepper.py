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
from threading import Thread

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
    turn_number = 0

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
        if self.direction_number%2 == 0:
            self.direction_value = 1
            print('direction_val = 1')
        else:
           self.direction_value = 0
           print('direction_val = 0')
        self.direction_number += 1

        if s0.is_busy() == True:
            #s0.go_until_press(self.direction_value, 3 * 6400)
            s0.go_until_press(self.direction_value, int(100 + (round(self.slideeer.value, 0) / 30 * 6400)))
        else:
            print("s0 is not running")

    def slideeer_action(self):
        print("slideeer value = " , self.slideeer.value)
        if self.turn_on_off_button.text == 'Off':
            s0.go_until_press(self.direction_value, int(100 + (round(self.slideeer.value, 0) / 30 * 6400)))
        else:
            print('stepper motor is off')

    def fun_time(self):
        self.fun_label.text = str(s0.get_position_in_units())
        print('PRINT 0')
        s0.set_speed(1)
        s0.start_relative_move(-15)
        print('15 REVOLUTIONS')
        sleep(15)
        sleep(0.1)
        self.fun_label.text = str(s0.get_position_in_units())
        print('PRINT 15')
        s0.softStop()
        sleep(.1)
        print('SLEEP 10 SECS')
        sleep(10)

        s0.set_speed(5)
        s0.start_relative_move(-10)
        print('10 REVOLUTIONS')
        sleep(2)
        self.fun_label.text = str(s0.get_position_in_units())
        print('SLEEP 8 SECS')
        sleep(8)
        s0.softStop()
        sleep(.1)
        print('GOING HOME')
        s0.goHome()
        sleep(0.1) #ISSUES HERE??
        self.fun_label.text = str(s0.get_position_in_units())

        sleep(30)
        self.fun_label.text = str(s0.get_position_in_units())
        sleep(2)
        s0.set_speed(6)
        s0.start_relative_move(-75)
        sleep(12.5)
        sleep(2)
        self.fun_label.text = str(s0.get_position_in_units())
        sleep(10)
        s0.goHome()
        sleep(13)
        self.fun_label.text = str(s0.get_position_in_units())
        sleep(1)

    def start_fun_thread(self):  # This should be inside the MainScreen
        Thread(target=self.fun_time, daemon=True).start()


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
