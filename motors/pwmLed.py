#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from threading import Thread, RLock

LedPin = 15

class motor_class(Thread):
	"""docstring for motor_class"""
	def __init__(self, num):
		super(motor_class, self).__init__()
		self.num = num

	
	def run(self):
		while True:
			with shared.verrou:
				print ("%4d" % dc)
				p.ChangeDutyCycle(shared.motors[self.num])     # Change duty cycle
				print ("%4d" % shared.motors[self.num])
				time.sleep(0.05)
	
	def destroy(self):
		p.stop()
		GPIO.output(LedPin, GPIO.HIGH)    # turn off all leds
		GPIO.cleanup()

def setup(self):
	global p
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.output(LedPin, GPIO.LOW)  # Set LedPin to low(0V)

	p = GPIO.PWM(LedPin, 1000)     # set Frequece to 1KHz
	p.start(0)                     # Duty Cycle = 0

if __name__ == '__main__':     # Program start from here
mot = motor_class()
	mot.setup()
	try:
		mot.run()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		mot.destroy()
