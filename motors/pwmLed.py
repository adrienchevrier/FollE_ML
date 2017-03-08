#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from threading import Thread, RLock

LedPin = 15

class motor_class(Thread):
	"""docstring for motor_class"""
	def __init__(self):
		super(motor_class, self).__init__()
		


	def setup(self):
		global p
		GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
		GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
		GPIO.output(LedPin, GPIO.LOW)  # Set LedPin to low(0V)
	
		p = GPIO.PWM(LedPin, 1000)     # set Frequece to 1KHz
		p.start(0)                     # Duty Cycle = 0
	
	def run(self):
		while True:
			for dc in range(0, 101, 4):   # Increase duty cycle: 0~100
				print ("%4d" % dc)
				p.ChangeDutyCycle(dc)     # Change duty cycle
				time.sleep(0.05)
			time.sleep(1)
			for dc in range(100, -1, -4): # Decrease duty cycle: 100~0
				print ("%4d" % dc)
				p.ChangeDutyCycle(dc)
				time.sleep(0.05)
			time.sleep(1)
	
	def destroy(self):
		p.stop()
		GPIO.output(LedPin, GPIO.HIGH)    # turn off all leds
		GPIO.cleanup()

if __name__ == '__main__':     # Program start from here
mot = motor_class()
	mot.setup()
	try:
		mot.run()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		mot.destroy()
