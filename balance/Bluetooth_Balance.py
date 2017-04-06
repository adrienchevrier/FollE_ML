
import bluetooth
import RPi.GPIO as GPIO
import time
import sys

CLK = 18
MISO = 23
MOSI = 24
CS = 25
LedPin = 22 

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
port = 0

def setupSpiPins(clkPin, misoPin, mosiPin, csPin):

	''' Set all pins as an output except MISO (Master Input, Slave Output)'''
	GPIO.setup(clkPin, GPIO.OUT)
	GPIO.setup(misoPin, GPIO.IN)
	GPIO.setup(mosiPin, GPIO.OUT)
	GPIO.setup(csPin, GPIO.OUT)

def setup():
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led

	server_sock.bind(("",port))
	server_sock.listen(1)
	print "listening on port %d" % port
	try:
		bluetooth.advertise_service( server_sock, "FooBar Service", uuid )
		#client_sock,address = server_sock.accept()
		print "Accepted connection from ",address
	except Exception as e:
		raise e
	finally:
		client_sock,address = server_sock.accept()
		print "Accepted connection from ",address
		return client_sock

def sendBits(data, numBits, clkPin, mosiPin):
	''' Sends 1 Byte or less of data'''
	
	data <<= (8 - numBits)
	
	for bit in range(numBits):
		# Set RPi's output bit high or low depending on highest bit of data field
		if data & 0x80:
			GPIO.output(mosiPin, GPIO.HIGH)
		else:
			GPIO.output(mosiPin, GPIO.LOW)
		
		# Advance data to the next bit
		data <<= 1
		
		# Pulse the clock pin HIGH then immediately low
		GPIO.output(clkPin, GPIO.HIGH)
		GPIO.output(clkPin, GPIO.LOW)

def recvBits(numBits, clkPin, misoPin):
	'''Receives arbitrary number of bits'''
	retVal = 0
	
	for bit in range(numBits):
		# Pulse clock pin 
		GPIO.output(clkPin, GPIO.HIGH)
		GPIO.output(clkPin, GPIO.LOW)
		
		# Read 1 data bit in
		if GPIO.input(misoPin):
			retVal |= 0x1
		
		# Advance input to next bit
		retVal <<= 1
	
	# Divide by two to drop the NULL bit
	return (retVal/2)

def readAdc(channel, clkPin, misoPin, mosiPin, csPin):
	if (channel < 0) or (channel > 7):
		print "Invalid ADC Channel number, must be between [0,7]"
		return -1
		
	# Datasheet says chip select must be pulled high between conversions
	GPIO.output(csPin, GPIO.HIGH)
	
	# Start the read with both clock and chip select low
	GPIO.output(csPin, GPIO.LOW)
	GPIO.output(clkPin, GPIO.HIGH)
	
	# read command is:
	# start bit = 1
	# single-ended comparison = 1 (vs. pseudo-differential)
	# channel num bit 2
	# channel num bit 1
	# channel num bit 0 (LSB)
	read_command = 0x18
	read_command |= channel
	
	sendBits(read_command, 5, clkPin, mosiPin)
	
	adcValue = recvBits(12, clkPin, misoPin)
	
	# Set chip select high to end the read
	GPIO.output(csPin, GPIO.HIGH)
  
	return adcValue

def COM(client_sock):
	quit ='quit'
	led = 'led'
	test=100
	Prec=readAdc(0, CLK, MISO, MOSI, CS)
	Prec=(Prec+40)*(-41)+165772

	while True:
		try:
			print 'first'
			data = client_sock.recv(1024)
			print "received [%s]" % data
			#client_sock.send("Bien recu \n")

			# calcul poids
			time.sleep(10)
			test=readAdc(0, CLK, MISO, MOSI, CS)
			test=test*(-41)+165772
			print "ADC Result: ", str(test-Prec-2300)
			string = str(test-Prec-2300)
			#string=str(test)
			string = '%s\n' %(string)
			print "ADC Result2: %s" % string
			#client_sock.send("1100 \n")
			#client_sock.send(string)

			if data == quit:
				print 'quit'
				break
			if data == led:
				print 'led'
				sec=readAdc(0, CLK, MISO, MOSI, CS)
				tot=sec
				while sec>(tot-50):
					print str(tot-50)
					print '...led on'
					GPIO.output(LedPin, GPIO.LOW)  # led on
					time.sleep(0.5)
					print 'led off...'
					GPIO.output(LedPin, GPIO.HIGH) # led off
					time.sleep(0.5)
					sec=readAdc(0, CLK, MISO, MOSI, CS)
					print "ADC Result: ", str(sec)

				break
				print '...led on'
				GPIO.output(LedPin, GPIO.LOW)  # led on
				time.sleep(20)
			print 'toto'
			client_sock.send(string)
			

				#time.sleep(20)
		except:
			server_sock.close()
	#GPIO.output(LedPin, GPIO.LOW)  # led on

def loop(client_sock):
	global server_sock	
	COM(client_sock)
	server_sock.close()
		

if __name__ == '__main__':
	
	try:
		GPIO.setmode(GPIO.BCM)
		setupSpiPins(CLK, MISO, MOSI, CS)
		loop(setup())
	except KeyboardInterrupt:
		#client_sock.close()
		GPIO.output(LedPin, GPIO.HIGH)     # led off
		GPIO.cleanup() 
		server_sock.close()
		sys.exit(0)
