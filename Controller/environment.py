#!/usr/bin/env python
import sys
import rospy

import math
import time
import numpy as np
from numpy.linalg import norm

from std_msgs.msg import Int8MultiArray, Float32, Bool, String, Float32MultiArray
from geometry_msgs.msg import Transform

from parameters import *

sys.path.append('/usr/lib/python2.7/dist-packages')  # weil ROS nicht mit Anaconda installiert


class VrepEnvironment():
    def __init__(self):
        # Image Subscriber
        self.dvs_sub = rospy.Subscriber('dvsData', Int8MultiArray, self.dvs_callback)
        self.dvs_data = np.array([0, 0])
        self.resize_factor = [dvs_resolution[0]//resolution[0],
                              (dvs_resolution[1]-crop_bottom-crop_top)//resolution[1]]

        # Position Subscriber
        self.pos_sub = rospy.Subscriber('transformData', Transform, self.pos_callback)
        self.pos_data = []

        # Distances Subscriber
        self.distances_sub = rospy.Subscriber('distances', Float32MultiArray, self.distances_callback)
        self.distances = []

        # Radius Publisher
        self.radius_pub = rospy.Publisher('turningRadius', Float32, queue_size=1)

        # Reset Publisher
        self.reset_pub = rospy.Publisher('resetRobot', Bool, queue_size=1)

        self.steps = 0

        self.turn_pre = turn_pre
        self.radius = 0
        self.radius_buffer = 0

        self.distance = 0

        self.reward = 0
        self.state = []

        # TODO
        # self.positive_direction = False
        self.positive_direction = True

        self.terminate = False
        self.terminate_position = 0

        rospy.init_node('rstdp_controller')
        self.rate = rospy.Rate(rate)

    def dvs_callback(self, msg):
        # Store incoming DVS data
        self.dvs_data = msg.data
        return

    def pos_callback(self, msg):
        # Store incoming position data
        self.pos_data = np.array([msg.translation.x, msg.translation.y, time.time()])
        return

    def distances_callback(self, msg):
        # Store incoming distances
        self.distances = msg.data
        return

    def reset(self):
        # Reset model
        self.radius_pub.publish(0.0)
        self.turn_pre = 0.0

        # Change direction
        # TODO
        # self.positive_direction = not self.positive_direction

        self.reset_pub.publish(Bool(self.positive_direction))

        time.sleep(1)
        return np.zeros((resolution[0], resolution[1]), dtype=int), 0.

    def step(self, n_l, n_r):

        self.steps += 1

        # Snake turning model
        m_l = n_l/n_max
        m_r = n_r/n_max
        # TODO:
        a = m_r - m_l
#        a = m_l - m_r
        c = math.sqrt((m_l**2 + m_r**2)/2.0)

        self.turn_pre = c*a*0.5 + (1-c)*self.turn_pre

        if abs(self.turn_pre) < 0.001:
            self.radius = 0
        else:
            self.radius = r_min/self.turn_pre

        # Publish mean turning radius every 5 steps
        if (self.steps % 5 != 0):
            self.radius_buffer = self.radius_buffer + self.radius
        else:
            self.radius = self.radius_buffer/5
            self.radius_buffer = 0

        self.radius_pub.publish(self.radius)
        self.rate.sleep()

        # Get distance
        self.distance = 1.5 - self.distances[0]

        # Set reward signal
        if self.positive_direction is True:
            self.reward = self.distance
        else:
            self.reward = -self.distance

        # Get state
        self.state = self.getState()

        if (abs(self.distance) > reset_distance):
            print "Reset_distance reached: ", abs(self.distance)
            self.terminate = True
        if (abs(self.pos_data[0]) > reset_position):
            print "End of maze reached: ", abs(self.pos_data[0])
            self.terminate = True

        t = self.terminate
        n = self.steps

        if t is True:
            self.steps = 0
            self.terminate_position = abs(self.pos_data[0])
            self.reset()
            self.terminate = False

        if (self.steps % modulo == 0):
            print "---------environment.py---------"
            print "-----------step: ", self.steps, "-----------"
            # print "dvs_data: \n", self.dvs_data
            print "pos_data[0]: \t", abs(self.pos_data[0])
            print "pos_data[1]: \t", self.pos_data[1]
            print "n_l: \t\t", n_l
            print "n_r: \t\t", n_r
            print "a: \t\t", a
            print "c: \t\t", c
            print "turn_pre: \t", self.turn_pre
            print "radius: \t", self.radius
            print "distance: \t", self.distance
            print "reward: \t", self.reward
#            print "state: \n", self.state
            print "--------------------------------"

        # Return state, distance, pos_data, reward, terminate, steps
        return self.state, self.distance, self.pos_data, self.reward, t, n, self.terminate_position

    def getState(self):
        new_state = np.zeros((resolution[0], resolution[1]), dtype=int)
        for i in range(len(self.dvs_data)//2):
            try:
                if crop_bottom <= self.dvs_data[i*2+1] < (dvs_resolution[1]-crop_top):
                    idx = ((self.dvs_data[i*2])//self.resize_factor[0], (self.dvs_data[i*2+1]-crop_bottom)//self.resize_factor[1])
                    new_state[idx] += 1
            except:
                pass
        return new_state
