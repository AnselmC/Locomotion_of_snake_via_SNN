#!/usr/bin/env python

from network import *
from environment import *
import parameters as p
import h5py
import json
import signal

snn = SpikingNeuralNetwork()
env = VrepEnvironment()

weights_r = []
weights_l = []
weights_i = []
steps = []
terminate_positions = []
params = {}
terminate = False


def handler(signum, frane):
    global terminate
    terminate = True


signal.signal(signal.SIGINT, handler)

# Initialize environment, get initial state, initial reward
state, reward = env.reset()

for i in range(p.training_length):

    # Simulate network for 50 ms
    # get number of output spikes and network weights
    n_l, n_r, weights = snn.simulate(state, reward)
    w_l = weights[0]
    w_r = weights[1]

    # Feed output spikes in model
    # Get state, distance, pos_data, reward, t, step
    (state, distance, pos_data, reward, t, step,
     terminate_position, travelled_distances, vrep_steps) = env.step(n_l, n_r)

    # if (i % modulo == 0):
    #     print "----------training.py----------"
    #     print "-----------step: ", i, "-----------"
    #     print "n_l: \t\t", n_l
    #     print "n_r: \t\t", n_r
    #     print "w_l: \n", w_l
    #     print "w_r: \n", w_r
    #     for j in range(len(weights[2])):
    #         print "weight_hidden[", j,"]: \n", weights[2][j]
    #     print "--------------------------------"

    # Save weights every 100 simulation steps
    if i % 100 == 0:
        weights_l.append(w_l)
        weights_r.append(w_r)
        weights_i.append(i)

    # Save no. of steps every episode
    if t:
        steps.append(step)
        terminate_positions.append(terminate_position)
        print "----------training.py----------"
        print "-----------terminate-----------"
        print "steps:\n", steps
        print "vrep_steps:\n", vrep_steps
        print "travelled_distances:\n", travelled_distances
        print "--------------------------------"

    if terminate:
        break

# Save training parameters
try:
    print "saving params"
    params = p.params_dict
    print params
    # Save to single json file
    json_data = json.dumps(params, indent=4, sort_keys=True)
    print "converted to json"
    with open(p.path+'/training_parameters.json','w') as file:
        file.write(json_data)
except:
    print "saving params failed"
    pass

# Save data
h5f = h5py.File(p.path + '/rstdp_data.h5', 'w')
h5f.create_dataset('w_l', data=weights_l)
h5f.create_dataset('w_r', data=weights_r)
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('steps', data=steps)
h5f.create_dataset('vrep_steps', data=vrep_steps)
h5f.create_dataset('terminate_positions', data=terminate_positions)
h5f.create_dataset('travelled_distances', data=travelled_distances)
h5f.close()
