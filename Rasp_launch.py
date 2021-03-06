from threading import Thread, RLock
from sonars import sonar_thread
from motors import pwmLed as mot_thread
import rasp_playing

'''Main file that launches all programs'''
def main():
	#Init threads
	shared.init()
	saved_model = 'saved-models/BLE/BLE8164-150-100-50000-325000.h5'
    model = neural_net(NUM_SENSORS, [164, 150], saved_model)
	#Threads handling sonar readings
	sonarclass = sonar_thread.Afficheur()
	mot_thread.setup()

	motclass0 = mot_thread.motor_class(0)

    p = rasp_playing.player(model)
    p.play()


if __name__ == '__main__':
	main()