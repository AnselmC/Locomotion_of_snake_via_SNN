#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
from parameters import *


h5f = h5py.File(path + '/training_data.h5', 'r')

w_faster = np.array(h5f['w_faster'], dtype=float)
w_slower = np.array(h5f['w_slower'], dtype=float)
w_i = np.array(h5f['w_i'], dtype=float)
print w_faster.shape
weights_faster = np.flipud(w_faster[-1])
weights_slower = np.flipud(w_slower[-1])
print weights_slower.shape
fig = plt.figure(figsize=(12,12))

xlim = w_i.max(axis=0)
ymin1 = w_slower.min()*1.1
ymax1 = w_slower.max()*1.1

ax1 = plt.subplot(411)
plt.title('Final left weights', color='0.4')
plt.imshow(weights_slower, alpha=0.5, aspect='auto')
plt.axis('off')
for (j,i),label in np.ndenumerate(weights_slower):
	ax1.text(i,j,int(label),ha='center',va='center', size='10')

ax2 = plt.subplot(412)
plt.title('Final right weights', color='0.4')
plt.imshow(weights_faster, alpha=0.5, aspect='auto')
plt.axis('off')
for (j,i),label in np.ndenumerate(weights_faster):
	ax2.text(i,j,int(label),ha='center',va='center', size='10')

ax3 = plt.subplot(413)
ax3.set_title('Weights to left neuron', color='0.4')
ax3.set_ylabel('Weight')
ax3.set_xlim((0,xlim))
ax3.set_ylim((ymin1, ymax1))
plt.grid(True)
ax3.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_slower.shape[1]):
	for j in range(w_slower.shape[2]):
		plt.plot(w_i, w_slower[:,i,j])


ymin2 = w_faster.min()*1.1
ymax2 = w_faster.max()*1.1
ax4 = plt.subplot(414, sharex=ax3)
ax4.set_title('Weights to right neuron', color='0.4')
# ax5.set_ylabel('Weight')
ax4.set_xlim((0,xlim))
ax4.set_ylim((ymin2,ymax2))
plt.grid(True)
ax4.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_faster.shape[1]):
	for j in range(w_faster.shape[2]):
		plt.plot(w_i, w_faster[:,i,j])

ax4.set_xlabel('Simulation Time [1 step = 50 ms]')


fig.tight_layout()

filename = 'session_' + session_no + '_weights_lr.pdf'
filepath = '../../plots/regular/' + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)