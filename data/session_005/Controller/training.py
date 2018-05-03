#!/usr/bin/env python

import numpy as np
from network import *
from environment import *
from parameters import *
import h5py

snn = SpikingNeuralNetwork()
env = VrepEnvironment()

weights_r = []
weights_l = []
weights_i = []
steps = []

# Initialize environment, get initial state, initial reward
s,r = env.reset()

for i in range(training_length):
	
	# Simulate network for 50 ms
	# get number of output spikes and network weights
	n_l, n_r, w_l, w_r = snn.simulate(s,r)

	# Feed output spikes in steering wheel model
	# Get state, distance, reward, termination, step
	s,d,r,t,n = env.step(n_l, n_r)

	# Save weights every 100 simulation steps
	if i % 100 == 0:
		print "--------------------------------"
		print "-----------step: ", i, "-----------"
		print "--------------------------------"
		print "Left weights:\n", w_l
		print "Right weights:\n", w_r
		weights_l.append(w_l)
		weights_r.append(w_r)
		weights_i.append(i)

    # Save no. of steps every episode
	if t:
 		steps.append(n)
        
# Save data
h5f = h5py.File(path + '/rstdp_data.h5', 'w')
h5f.create_dataset('w_l', data=weights_l)
h5f.create_dataset('w_r', data=weights_r)
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('steps', data = steps)
h5f.close()
