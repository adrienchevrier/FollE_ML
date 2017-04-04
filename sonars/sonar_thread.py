import random
import sys
from threading import Thread, RLock
import time
import RPi.GPIO as GPIO
import shared

GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24
TRIG_2 = 27 
ECHO_2 = 22
TRIG_2 = 16
TRIG_3 = 17
TRIG_4 = 18
ECHO_2 = 19
ECHO_3 = 20
ECHO_4 = 21


class Afficheur(Thread):
    #Thread permettant de recuperer distance via les sonars
    def __init__(self, Trig, Echo, snum):
       Thread.__init__(self)
       self.Trig = Trig
       self.Echo = Echo
       self.num = snum

    #code a executer pendant le thread
    def run(self):
        with verrou:
            print ("Distance Measurement In Progress")
            GPIO.setup(self.Trig,GPIO.OUT)
            GPIO.setup(self.Echo,GPIO.IN)

            GPIO.output(self.Trig, False)
            print ("Waiting For Sensor To Settle")
            time.sleep(2)

            GPIO.output(self.Trig, True)
            time.sleep(0.00001)
            GPIO.output(self.Trig, False)

            while GPIO.input(self.Echo)==0:
              pulse_start = time.time()

            while GPIO.input(self.Echo)==1:
              pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start

            distance = pulse_duration * 17150

            distance = round(distance, 2)
            shared.s_readings[self.num] = distance

            print ("Distance:",distance,"cm")

def setup():
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.setup(TRIG_2,GPIO.OUT)
    GPIO.setup(ECHO_2,GPIO.IN)
    create()

# Creation des threads
def create():
    global thread_0
    global thread_1
    global thread_2
    global thread_3
    global thread_4
    #Last number is sonar number (0 left maximum right)
    thread_0 = Afficheur(TRIG,ECHO,0)
    thread_1 = Afficheur(TRIG_1,ECHO_1, 1)
    thread_2 = Afficheur(TRIG_2,ECHO_2, 2)
    thread_3 = Afficheur(TRIG_3,ECHO_3, 3)
    thread_4 = Afficheur(TRIG_4,ECHO_4, 4)

# Lancement des threads
def Launch():
    thread_1.start()
    thread_2.start()

# Attend que les threads se terminent
def wait():
    thread_1.join()
    thread_2.join()

def loop():
    while True:
        Launch()
        wait()


def destroy():
    GPIO.cleanup()             # Release resource


if __name__ == '__main__':     # Program start from here
    
    try:
        setup()
        #create()
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()    