'''
class that manages actions according to state
State contains the 5 sonars and 3 BLE sensors information 

Adrien CHEVRIER
'''



import shared
import sys
#sys.path.append('/usr/local/lib/python3.5/dist-packages')
import os

import random
import math
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

import threading


# PyGame init
width = 1400
height = 1000
init_x = 200
init_y = 500

# Showing sensors and redrawing slows things down.
show_sensors = True
draw_screen = True

auto = True #cat moves automatically or not

rc = 10 #coefficient to calculate reward

#Init rewards
rtab_sonar = [-1,-1,-1,-1,-1,-1]

global keyboard_in
keyboard_in = ''


class GameState:
    def __init__(self):

        global keyboard_in 
        global auto




        # Global-ish.
        self.crashed = False

        # Record steps.
        self.num_steps = 0

    def frame_step(self, action):


        print_stuff = ''

        if action == 0:  # Turn left.
            shared.motors[0] = 0.1
            shared.motors[1] = 0.4
        elif action == 1:  # Turn right.
            shared.motors[0] = 0.4
            shared.motors[1] = 0.1
        elif action == 2:
            shared.motors[0] = 0.5
            shared.motors[1] = 0.5
        elif action == 3:
            shared.motors[0] = 0
            shared.motors[1] = 0


        clock.tick()

        # Get the current location and the readings there.

        readings = shared.s_readings
        BLE_readings = shared.b_readings
        BLE_detect = self.detect_with_ble(BLE_readings)
        state = np.array([readings+BLE_readings])

        # Set the reward.
        # Car crashed when any reading == 1
        if self.car_is_crashed(readings):
            self.crashed = True
            reward = -500
        else:
            #Calculate reward
            rtab_sonar[0]=(1700*mlab.normpdf(readings[0], 20, 2))*BLE_detect[0]
            rtab_sonar[1]=(3000*mlab.normpdf(readings[1], 15, 2))*BLE_detect[1]
            rtab_sonar[2]=(6000*mlab.normpdf(readings[2], 15, 2))*BLE_detect[2]
            rtab_sonar[3]=(3000*mlab.normpdf(readings[3], 15, 2))*BLE_detect[3]
            rtab_sonar[4]=(1700*mlab.normpdf(readings[4], 20, 2))*BLE_detect[4]
            rtab_sonar[5]=( (int(self.sum_readings(readings))-5) / 10)
            reward = sum(rtab_sonar)

            print_stuff = "\n\n detect BLE :"+str(BLE_detect)+"\n\n reward : "+str(reward)+"\n\n RSONARS details :"+str(rtab_sonar)+"\n\n state:"+str(state)


        self.num_steps += 1

        return reward, state,print_stuff

    def detect_with_ble(self,breadings):
        detected = [-1,-1,-1,-1,-1]

        if (breadings[0]>220) & (breadings[0]<260):
            if (breadings[1]>205) & (breadings[1]<245):
                if (breadings[2]>240) & (breadings[2]<280):
                    detected[0] = 1
                else:
                   detected[0] = 0
            else:
                   detected[0] = 0
        else:
                   detected[0] = 0

        if (breadings[0]>180) & (breadings[0]<220):
            if (breadings[1]>145) & (breadings[1]<185):
                if (breadings[2]>190) & (breadings[2]<230):
                    detected[1] = 1
                else:
                   detected[1] = 0
            else:
                   detected[1] = 0
        else:
                   detected[1] = 0




        if (breadings[0]>195) & (breadings[0]<235):
            if breadings[1]>155 & (breadings[1]<195):
                if( breadings[2]>195) & (breadings[2]<235):
                    detected[2] = 1
                else:
                   detected[2] = 0
            else:
                   detected[2] = 0
        else:
                   detected[2] = 0


        if (breadings[0]>190) & (breadings[0]<230):
            if (breadings[1]>145) & (breadings[1]<185):
                if (breadings[2]>180) & (breadings[2]<220):
                    detected[3] = 1
                else:
                   detected[3] = 0
            else:
                   detected[3] = 0
        else:
                   detected[3] = 0

        if (breadings[0]>240) & (breadings[0]<280):
            if (breadings[1]>205) & (breadings[1]<245):
                if (breadings[2]>220) & (breadings[2]<260):
                    detected[4] = 1
                else:
                   detected[4] = 0
            else:
                   detected[4] = 0
        else:
                   detected[4] = 0

        return detected



    def car_is_crashed(self, readings):
        if readings[0] == 4 or readings[1] == 4 or readings[2] == 4 or readings[3] == 4 or readings[4] == 4:
            return True
        else:
            return False


    def sum_readings(self, readings):
        """Sum the number of non-zero readings."""
        tot = 0
        for i in readings:
            tot += i
        return tot






if __name__ == "__main__":
    game_state = GameState()
    while True:
        game_state.frame_step((random.randint(0, 2)))
