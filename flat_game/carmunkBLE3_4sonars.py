'''
Simulation of car following user with 4 sensors used for the reward
3 sensors used to detect the user and determine whether or not he is
in front of the car.
State contains the 4 sonars and 3 BLE sensors information 

Adrien CHEVRIER
'''




import sys
#sys.path.append('/usr/local/lib/python3.5/dist-packages')
import os

import random
import math
import numpy as np

import pygame as pygame
from pygame.color import THECOLORS

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

import threading
import readchar


# PyGame init
width = 1400
height = 1000
init_x = 200
init_y = 500
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Turn off alpha since we don't use it.
screen.set_alpha(None)

# Showing sensors and redrawing slows things down.
show_sensors = True
draw_screen = True

auto = True #cat moves automatically or not

rc = 10 #coefficient to calculate reward

#Init rewards
rtab_sonar = [-1,-1,-1,-1,-1]

global keyboard_in
keyboard_in = ''


class GameState:
    def __init__(self):

        global keyboard_in 
        global auto


        if auto== False:
        # Create new threads
            thread1 = InputThread(1, "InputThread", 1)

        # Start new Threads
            thread1.start()





        # Global-ish.
        self.crashed = False

        # Physics stuff.
        self.space = pymunk.Space()
        self.space.gravity = pymunk.Vec2d(0., 0.)

        # Create the car.
        self.create_car(init_x, init_y, 0)

        # Record steps.
        self.num_steps = 0

        # Create walls.
        static = [
            pymunk.Segment(
                self.space.static_body,
                (0, 1), (0, height), 1),
            pymunk.Segment(
                self.space.static_body,
                (1, height), (width, height), 1),
            pymunk.Segment(
                self.space.static_body,
                (width-1, height), (width-1, 1), 1),
            pymunk.Segment(
                self.space.static_body,
                (1, 1), (width, 1), 1)
        ]
        for s in static:
            s.friction = 1.
            s.group = 1
            s.collision_type = 1
            s.color = THECOLORS['red']
        self.space.add(static)

        # Create some obstacles, semi-randomly.
        # We'll create three and they'll move around to prevent over-fitting.
        self.obstacles = []
        self.obstacles.append(self.create_obstacle(200, 350, 100))
        self.obstacles.append(self.create_obstacle(700, 200, 125))
        self.obstacles.append(self.create_obstacle(600, 800, 35))
        self.obstacles.append(self.create_obstacle(1000, 350, 100))


        # Create a cat.
        self.create_cat()

    def create_obstacle(self, x, y, r):
        c_body = pymunk.Body(pymunk.inf, pymunk.inf)
        c_shape = pymunk.Circle(c_body, r)
        c_shape.elasticity = 1.0
        c_body.position = x, y
        c_shape.color = THECOLORS["blue"]
        self.space.add(c_body, c_shape)
        return c_body

    def create_cat(self):
        inertia = pymunk.moment_for_circle(1, 0, 14, (0, 0))
        self.cat_body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.cat_body.position = init_x+150, init_y
        self.cat_shape = pymunk.Circle(self.cat_body, 30)
        self.cat_shape.color = THECOLORS["orange"]
        self.cat_shape.elasticity = 1.0
        self.cat_shape.angle = 0.5
        direction = Vec2d(1, 0).rotated(self.cat_body.angle)
        self.space.add(self.cat_body, self.cat_shape)

    def create_human(self,x,y):
        inertia = pymunk.moment_for_circle(1, 0, 14, (0, 0))
        self.human_body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.human_body.position = init_x+50, init_y
        self.human_shape = pymunk.Circle(self.human_body, 30)
        self.human_shape.color = THECOLORS["pink"]
        self.human_shape.elasticity = 1.0
        self.human_shape.angle = 0.5
        direction = Vec2d(1, 0).rotated(self.human_body.angle)
        self.space.add(self.human_body, self.human_shape)

    def create_car(self, x, y, r):
        inertia = pymunk.moment_for_circle(1, 0, 14, (0, 0))
        self.car_body = pymunk.Body(1, inertia)
        self.car_body.position = x, y
        self.car_shape = pymunk.Circle(self.car_body, 25)
        self.car_shape.color = THECOLORS["green"]
        self.car_shape.elasticity = 1.0
        self.car_body.angle = r
        driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.apply_impulse(driving_direction)
        self.space.add(self.car_body, self.car_shape)

    def frame_step(self, action):

        global keyboard_in

        print_stuff = ''

        if action == 0:  # Turn left.
            self.car_body.angle -= .2
        elif action == 1:  # Turn right.
            self.car_body.angle += .2

        # Move obstacles.
        if self.num_steps % 100 == 0:
            self.move_obstacles()

        # Move cat.
        if self.num_steps % 5 == 0:
            self.move_cat()


        driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.velocity = 100 * driving_direction


        if action == 3:
            self.car_body.velocity = 0*Vec2d(1, 0).rotated(self.car_body.angle)

        # Update the screen and stuff.
        screen.fill(THECOLORS["black"])
        draw(screen, self.space)
        self.space.step(1./10)
        if draw_screen:
            pygame.display.flip()
        clock.tick()

        # Get the current location and the readings there.
        x, y = self.car_body.position
        xC, yC = self.cat_body.position
        readings = self.get_sonar_readings(x, y, self.car_body.angle)
        BLE_readings = self.get_BLE_readings(x,y,xC,yC,self.car_body.angle)
        color = self.detect_with_ble(BLE_readings)
        state = np.array([readings+BLE_readings])

        if keyboard_in=='t':
            #os.system("kill -9 %d"%(os.getppid()))
            exit()
        elif keyboard_in=='r':
            print("you killed yourself")
            readings = [1,1,1,1,1]
            keyboard_in = ''

        else:
            pass
        # Set the reward.
        # Car crashed when any reading == 1
        if self.car_is_crashed(readings):
            self.crashed = True
            reward = -500
            self.recover_from_crash(driving_direction)
        else:
            #Calculate reward
            rtab_sonar[0]=(2000*mlab.normpdf(readings[0], 16, 2))*color[0]
            rtab_sonar[1]=(6000*mlab.normpdf(readings[1], 15, 2))*color[1]
            rtab_sonar[2]=(6000*mlab.normpdf(readings[2], 15, 2))*color[2]
            rtab_sonar[3]=(2000*mlab.normpdf(readings[3], 16, 2))*color[3]
            rtab_sonar[4]=( (int(self.sum_readings(readings))-5) / 10)
            reward = sum(rtab_sonar)

            print_stuff = "\n\n detect BLE :"+str(color)+"\n\n reward : "+str(reward)+"\n\n RSONARS details :"+str(rtab_sonar)+"\n\n state:"+str(state)


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



    def move_obstacles(self):
        # Randomly move obstacles around.
        for obstacle in self.obstacles:
            speed = random.randint(1, 5)
            direction = Vec2d(1, 0).rotated(self.car_body.angle + random.randint(-2, 2))
            obstacle.velocity = speed * direction
            direction = Vec2d(1, 0).rotated(self.cat_body.angle)
            self.cat_body.velocity = speed * direction

    def move_cat(self):
        global keyboard_in
        #check if cat in auto move mode or not
        if auto== True:
            speed = random.randint(20, 200)
            self.cat_body.angle -= random.randint(-1, 1)
            direction = Vec2d(1, 0).rotated(self.cat_body.angle)
            self.cat_body.velocity = speed * direction
        else :
        #if not move according to keys 'zqsd'
            Vec2d(1, 0).rotated(self.cat_body.angle)
            self.cat_body.velocity = 0*Vec2d(1, 0).rotated(self.cat_body.angle)
            if keyboard_in == 'z':
                self.cat_body.position = self.cat_body.position.x, self.cat_body.position.y+6
                self.cat_shape.angle = 0
            elif keyboard_in == 'd':
                self.cat_body.position = self.cat_body.position.x+6, self.cat_body.position.y
                self.cat_shape.angle = 0.5
            elif keyboard_in == 's':
                self.cat_body.position = self.cat_body.position.x, self.cat_body.position.y-6
                self.cat_shape.angle = 1
            elif keyboard_in == 'q':
                self.cat_body.position = self.cat_body.position.x-6, self.cat_body.position.y
                self.cat_shape.angle = -0.5    
            elif keyboard_in == ' ':
                self.cat_body.velocity = 0*Vec2d(1, 0).rotated(self.cat_body.angle)
            else:
                self.cat_body.velocity = 0*Vec2d(1, 0).rotated(self.cat_body.angle)
            #keyboard_in = ''

    def move_humans(self):
        for human in self.humans:
            speed = random.randint(20, 200)
            human.human_shape.angle -= random.randint(-1, 1)
            direction = Vec2d(1, 0).rotated(human.human_shape.angle)
            human.velocity = speed * direction

    def car_is_crashed(self, readings):
        if readings[0] == 1 or readings[1] == 1 or readings[2] == 1 or readings[3] == 1:
            return True
        else:
            return False

    def recover_from_crash(self, driving_direction):
        """
        We hit something, so recover.
        """
        while self.crashed:
            # Go backwards.

            randX = (random.randint(0, 500))*0
            randY = (random.randint(0, 200))*0
            self.car_body.velocity = -100 * driving_direction
            self.cat_body.position = init_x+150+randX, init_y+ randY
            self.cat_body.angle = 0

            self.car_body.position = init_x+ randX, init_y+ randY
            self.car_body.angle = 0
            self.crashed = False

            #self.car_body.velocity = -100 * driving_direction
            
            for i in range(10):
                screen.fill(THECOLORS["red"])  # Red is scary!
                draw(screen, self.space)
                self.space.step(1./10)
                if draw_screen:
                    pygame.display.flip()
                clock.tick()

    def sum_readings(self, readings):
        """Sum the number of non-zero readings."""
        tot = 0
        for i in readings:
            tot += i
        return tot

            #return 1 if cat detected and 0 otherwise
    def get_check(self,arm,x,y,angle,offset):
        # Used to count the distance.
        i = 0

        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1

            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], angle+ offset
            )

            # Check if we've hit the cat. Return 1
            # if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= width or rotated_p[1] >= height:
                return   0
            else:
                obs = screen.get_at(rotated_p)
                if self.get_cat_or_not(obs) == 0:
                    return 1

        # Return 0 for nothing detected
        return 0

        #returns array with cat checked values
    def verify_detected(self, x, y, angle):
        #table contain if cat is detected
        readings = []

        arm_left = self.make_sonar_arm(x, y)
        arm_middle = arm_left
        arm_right = arm_left
        arm_left2 = arm_left
        arm_right2 = arm_left

        # Rotate them and get readings.
        readings.append(self.get_check(arm_left2, x, y, angle, 0.75))
        readings.append(self.get_check(arm_left, x, y, angle, 0.30))
        readings.append(self.get_check(arm_middle, x, y, angle, 0))
        readings.append(self.get_check(arm_right, x, y, angle, -0.30))
        readings.append(self.get_check(arm_right2, x, y, angle, -0.75))

        return readings

    def get_sonar_readings(self, x, y, angle):
        readings = []
        """
        Instead of using a grid of boolean(ish) sensors, sonar readings
        simply return N "distance" readings, one for each sonar
        we're simulating. The distance is a count of the first non-zero
        reading starting at the object. For instance, if the fifth sensor
        in a sonar "arm" is non-zero, then that arm returns a distance of 5.
        """
        # Make our arms.
        arm_left = self.make_sonar_arm(x, y)
        arm_middle = self.make_sonar_arm(x+5, y-15)
        arm_middle2 = self.make_sonar_arm(x+5, y+15)
        arm_right = arm_left

        # Rotate them and get readings.
        readings.append(self.get_arm_distance(arm_left, x, y, angle, 0.5))
        readings.append(self.get_arm_distance(arm_middle, x, y, angle, 0))
        readings.append(self.get_arm_distance(arm_middle2, x, y, angle, 0))
        readings.append(self.get_arm_distance(arm_right, x, y, angle, -0.5))

        if show_sensors:
            pygame.display.update()

        return readings





    def get_arm_distance(self, arm, x, y, angle, offset):
        # Used to count the distance.
        i = 0

        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1

            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], angle + offset
            )

            # Check if we've hit something. Return the current i (distance)
            # if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= width or rotated_p[1] >= height:
                return i  # Sensor is off the screen.
            else:
                obs = screen.get_at(rotated_p)
                if self.get_track_or_not(obs) != 0:
                    return i

            if show_sensors:
                pygame.draw.circle(screen, (255, 255, 255), (rotated_p), 3)

        # Return the distance for the arm.
        return i


    def get_color(self,arm,x,y,angle):
        # Used to count the distance.
        i = 0

        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1

            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], angle
            )

            # Check if we've hit something. Return the current i (distance)
            # if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= width or rotated_p[1] >= height:
                return "out"  # Sensor is off the screen.
            else:
                obs = screen.get_at(rotated_p)
                if self.get_cat_or_not(obs) == 0:
                    return "orange"
                if self.get_track_or_not(obs)==0:
                    return "black"

        # Return the distance for the arm.
        return i

    def make_sonar_arm(self, x, y):
        spread = 10  # Default spread.
        distance = 20  # Gap before first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for i in range(1, 40):
            arm_points.append((distance + x + (spread * i), y))

        return arm_points


    def get_BLE_readings(self, xR,yR,xC,yC, angle):
        d = []
        sensors = self.make_BLE_sensors(xR,yR)
        for point in sensors:
                rotated_p = self.get_rotated_BLE(
                    xR, yR, point[0], point[1], angle
                )
                d.append(self.get_BLE_distance(rotated_p[0],rotated_p[1],xC,yC))

        if show_sensors:
            pygame.display.update()
        return d

    def get_BLE_distance(self, xR, yR,xC, yC):
        # Used to count the distance.
        i = 0

        # calculate distance between 2 points
        i = math.sqrt((xR-xC)*(xR-xC)+(yR-yC)*(yR-yC))

        if show_sensors:
                pygame.draw.circle(screen, (255, 255, 255), (xR,height-yR), 2)

        # Return the distance for the arm.
        return i


    def make_BLE_sensors(self,x,y):
        distance = 15   #sensors dis
        BLE_points = []
        BLE_points.append((x-15,y+15))
        BLE_points.append((x+25,y))
        BLE_points.append((x-15,y-15))
        
        return BLE_points

    def get_rotated_point(self, x_1, y_1, x_2, y_2, radians):
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(radians) + \
            (y_2 - y_1) * math.sin(radians)
        y_change = (y_1 - y_2) * math.cos(radians) - \
            (x_1 - x_2) * math.sin(radians)
        new_x = x_change + x_1
        new_y = height - (y_change + y_1)
        return int(new_x), int(new_y)

    def get_rotated_BLE(self, x_1, y_1, x_2, y_2, radians):
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(radians) - \
            (y_2 - y_1) * math.sin(radians)
        y_change = (y_2 - y_1) * math.cos(radians) + \
            (x_2 - x_1) * math.sin(radians)
        new_x = (x_change +x_1)
        new_y = y_1+(y_change  )
        return int(new_x), int(new_y)

    def get_track_or_not(self, reading):
        if reading == THECOLORS['black']:
            return 0
        else:
            return 1

    def get_cat_or_not(self, reading):
        if reading == THECOLORS['orange']:
            return 0
        else:
            return 1





class InputThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("hello")
        global keyboard_in 
        #Read keyboard inputs to do some actions
        while keyboard_in != 't':
            keyboard_in= readchar.readchar()
            sys.stdout.flush()

        exit()
print("Exiting inputThread")



if __name__ == "__main__":
    game_state = GameState()
    while True:
        game_state.frame_step((random.randint(0, 2)))
