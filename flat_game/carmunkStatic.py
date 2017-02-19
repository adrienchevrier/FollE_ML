import random
import math
import numpy as np

import pygame
from pygame.color import THECOLORS

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

# PyGame init
width = 1000
height = 700
init_x = 200
init_y = 150
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Turn off alpha since we don't use it.
screen.set_alpha(None)

# Showing sensors and redrawing slows things down.
show_sensors = True
draw_screen = True


class GameState:
    def __init__(self):
        # Global-ish.
        self.crashed = False

        # Physics stuff.
        self.space = pymunk.Space()
        self.space.gravity = pymunk.Vec2d(0., 0.)

        # Create the car.
        self.create_car(init_x, init_y-50, 45)

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
        #self.obstacles.append(self.create_obstacle(200, 350, 100))
        self.obstacles.append(self.create_obstacle(700, 200, 125))
        self.obstacles.append(self.create_obstacle(600, 600, 35))


        # Create a cat.
        #self.create_cat()

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
        #self.cat_body.position = init_x+150, init_y
        self.cat_body.position = init_x+200, init_y+20
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
        #if action == 0:  # Turn left.
        #    self.car_body.angle -= .2
        #elif action == 1:  # Turn right.
        #    self.car_body.angle += .2

        # Move obstacles.
        #if self.num_steps % 100 == 0:
            #self.move_obstacles()

        # Move cat.
        #if self.num_steps % 5 == 0:
            #self.move_cat()


        #driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        #self.car_body.velocity = 100 * driving_direction


        #if action == 3:
            #self.car_body.velocity = 0*Vec2d(1, 0).rotated(self.car_body.angle)

        # Update the screen and stuff.
        screen.fill(THECOLORS["black"])
        draw(screen, self.space)
        #self.space.step(1./10)
        if draw_screen:
            pygame.display.flip()
        clock.tick()

        # Get the current location and the readings there.
        x, y = self.car_body.position
        readings = self.get_sonar_readings(x, y, self.car_body.angle)
        color = self.verify_detected(x, y, self.car_body.angle)
        state = np.array([readings])

        # Set the reward.
        # Car crashed when any reading == 1
        if self.car_is_crashed(readings):
            self.crashed = True
            reward = -500
            #self.recover_from_crash(driving_direction)
        else:
            ############        Reward max*376*    catClose*124      no cat*11  obectClose*
            #We use a gaussian function to set the reward to the maximum value if the user is bellow the car
            reward= ((40*color[0]+60*color[1]+(6000*mlab.normpdf(readings[2], 15, 2))*color[2]+60*color[3]+40*color[4])) +( (int(self.sum_readings(readings))-10) / 10)
            #print("cat detected")
            #reward = 0
            #print("no cat")
            #reward = 2
            #print("color: %s",self.get_color(arm_middle, x, y, self.car_body.angle))
            #reward = -5 + int(self.sum_readings(readings) / 10)

        #print data
        print("\n reward:%d" % (reward))
        print("detail reward:",'--',color[0],'--',color[1],'--',color[2],'--',color[3],'--',color[4])
        print('--',(1700*mlab.normpdf(readings[0], 20, 2))*color[0],'--',(3000*mlab.normpdf(readings[1], 15, 2))*color[1],'--',(6000*mlab.normpdf(readings[2], 15, 2))*color[2],'--',(3000*mlab.normpdf(readings[3], 15, 2))*color[3],'--',(3000*mlab.normpdf(readings[4], 20, 2))*color[4],'--',int(self.sum_readings(readings)))

        print("\n reading left2: ",readings[0])
        print(" reading left: ",readings[1])
        print(" reading mid: ",readings[2])
        print(" reading right: ",readings[3])
        print(" reading right2: ",readings[4])


        self.num_steps += 1

        return reward, state

    def move_obstacles(self):
        # Randomly move obstacles around.
        for obstacle in self.obstacles:
            speed = random.randint(1, 5)
            direction = Vec2d(1, 0).rotated(self.car_body.angle + random.randint(-2, 2))
            obstacle.velocity = speed * direction

    def move_cat(self):
        speed = random.randint(20, 200)
        self.cat_body.angle -= random.randint(-1, 1)
        direction = Vec2d(1, 0).rotated(self.cat_body.angle)
        self.cat_body.velocity = speed * direction

    def move_humans(self):
        for human in self.humans:
            speed = random.randint(20, 200)
            human.human_shape.angle -= random.randint(-1, 1)
            direction = Vec2d(1, 0).rotated(human.human_shape.angle)
            human.velocity = speed * direction

    def car_is_crashed(self, readings):
        if readings[0] == 1 or readings[1] == 1 or readings[2] == 1:
            return True
        else:
            return False

    def recover_from_crash(self, driving_direction):
        """
        We hit something, so recover.
        """
        while self.crashed:
            # Go backwards.
            #self.car_body.velocity = -100 * driving_direction
            self.cat_body.position = init_x+300, init_y
            self.cat_body.position = init_x+300, init_y
            self.cat_body.angle = 0

            self.car_body.position = init_x, init_y
            self.car_body.position = init_x, init_y
            self.car_body.angle = 0
            self.crashed = False
            
            for i in range(10):
                #self.car_body.angle += .2  # Turn a little.
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
        readings.append(self.get_arm_distance(arm_right, x, y, angle, -0.30))
        readings.append(self.get_arm_distance(arm_right2, x, y, angle, -0.75))

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
        arm_middle = arm_left
        arm_right = arm_left
        arm_left2 = arm_left
        arm_right2 = arm_left

        # Rotate them and get readings.
        readings.append(self.get_arm_distance(arm_left2, x, y, angle, 0.75))
        readings.append(self.get_arm_distance(arm_left, x, y, angle, 0.30))
        readings.append(self.get_arm_distance(arm_middle, x, y, angle, 0))
        readings.append(self.get_arm_distance(arm_right, x, y, angle, -0.30))
        readings.append(self.get_arm_distance(arm_right2, x, y, angle, -0.75))

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
                pygame.draw.circle(screen, (255, 255, 255), (rotated_p), 2)

        # Return the distance for the arm.
        return i

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


    def make_sonar_arm(self, x, y):
        spread = 10  # Default spread.
        distance = 20  # Gap before first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for i in range(1, 40):
            arm_points.append((distance + x + (spread * i), y))

        return arm_points

    def get_rotated_point(self, x_1, y_1, x_2, y_2, radians):
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(radians) + \
            (y_2 - y_1) * math.sin(radians)
        y_change = (y_1 - y_2) * math.cos(radians) - \
            (x_1 - x_2) * math.sin(radians)
        new_x = x_change + x_1
        new_y = height - (y_change + y_1)
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

if __name__ == "__main__":
    game_state = GameState()
    while True:
        game_state.frame_step((random.randint(0, 2)))
