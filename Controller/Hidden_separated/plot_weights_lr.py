#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from parameters import *


h5f = h5py.File(path + '/training_data.h5', 'r')

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_r = w_r.reshape(w_r.shape[0], 1, w_r.shape[1])
w_i = np.array(h5f['w_i'], dtype=float)
print w_r.shape
print w_l.shape
weights_l = np.flipud(w_l[-1])
weights_r = np.flipud(w_r[-1])

weights_l = weights_l.reshape(1,weights_l.size)
weights_r = weights_r.reshape(1,weights_r.size)
fig = plt.figure(figsize=(12,12))
gs = gridspec.GridSpec(6, 1)

gs1 = gs[0,:]
gs2 = gs[1,:]
gs3 = gs[2:4,:]
gs4 = gs[4:,:]

xlim = w_i.max(axis=0)
ymin1 = w_l.min()*1.1
ymax1 = w_l.max()*1.1

ax1 = plt.subplot(gs1)
plt.title('Final left weights', color='0.4')
plt.imshow(np.int_(weights_l), interpolation='nearest', cmap='coolwarm', aspect='equal')
plt.axis('off')
for (j,i),label in np.ndenumerate(weights_l):
	ax1.text(i,j,int(label),ha='center',va='center')

ax2 = plt.subplot(gs2)
plt.title('Final right weights', color='0.4')
plt.imshow(np.int_(weights_r), interpolation='nearest', cmap='coolwarm', aspect='equal')
plt.axis('off')
for (j,i),label in np.ndenumerate(weights_r):
	ax2.text(i,j,int(label),ha='center',va='center')

ax3 = plt.subplot(gs3)
ax3.set_title('Weights to left neuron', color='0.4')
ax3.set_ylabel('Weight')
ax3.set_xlim((0,xlim))
ax3.set_ylim((ymin1, ymax1))
plt.grid(True)
ax3.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_l.shape[1]):
	plt.plot(w_i, w_l[:,i])


ymin2 = w_r.min()*1.1
ymax2 = w_r.max()*1.1
ax4 = plt.subplot(gs4, sharex=ax3)
ax4.set_title('Weights to right neuron', color='0.4')
# ax5.set_ylabel('Weight')
ax4.set_xlim((0,xlim))
ax4.set_ylim((ymin2,ymax2))
plt.grid(True)
ax4.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_r.shape[1]):
	for j in range(w_r.shape[2]):
		plt.plot(w_i, w_r[:,i,j])

ax4.set_xlabel('Simulation Time [1 step = 50 ms]')


fig.tight_layout()

filename = 'session_' + session_no + '_weights_lr.pdf'
filepath = '../../plots/hidden_separated/' + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
