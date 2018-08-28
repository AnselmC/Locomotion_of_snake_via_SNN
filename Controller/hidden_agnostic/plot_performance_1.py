#!/usr/bin/env python

import numpy as np
import h5py
from parameters import *
import matplotlib.pyplot as plt
from matplotlib import gridspec
filepath = '../../data_hidden_not_separated/session_'
h5f = h5py.File(filepath + '001' + '/performance_data_1.h5', 'r')
h5f2 = h5py.File(filepath + '002' + '/performance_data_1.h5', 'r')
h5f3 = h5py.File(filepath + '003' + '/performance_data_1.h5', 'r')

vrep_steps = np.array(h5f['vrep_steps'], dtype = float)
print 'Network Size 1, V-REP steps: ', vrep_steps
nest_steps = np.array(h5f['steps'], dtype = float)
print 'Network Size 1, NEST steps: ', nest_steps
avg_dist_to_middle = np.array(h5f['average_distance_to_middle'], dtype = float)
print 'Network Size 1, Average distance to middle: ', avg_dist_to_middle

vrep_steps2 = np.array(h5f2['vrep_steps'], dtype = float)
print 'Network Size 2, V-REP steps: ', vrep_steps2
nest_steps2 = np.array(h5f2['steps'], dtype = float)
print 'Network Size 2, NEST steps: ', nest_steps2
avg_dist_to_middle2 = np.array(h5f2['average_distance_to_middle'], dtype = float)
print 'Network Size 2, Average distance to middle: ', avg_dist_to_middle2

vrep_steps3 = np.array(h5f3['vrep_steps'], dtype = float)
print 'Network Size 3, V-REP steps: ', vrep_steps3
nest_steps3 = np.array(h5f3['steps'], dtype = float)
print 'Network Size 3, NEST steps: ', nest_steps3
avg_dist_to_middle3 = np.array(h5f3['average_distance_to_middle'], dtype = float)
print 'Network Size 3, Average distance to middle: ', avg_dist_to_middle3

dist_to_middle = np.array(h5f['distance_to_middle'], dtype = float)
dist_to_middle2 = np.array(h5f2['distance_to_middle'], dtype = float)
dist_to_middle3 = np.array(h5f3['distance_to_middle'], dtype = float)

gs = gridspec.GridSpec(3, 2, width_ratios=[6, 1])
gs.update(wspace=0.)
s1 = abs(dist_to_middle).mean()
s2 = abs(dist_to_middle2).mean()
s3 = abs(dist_to_middle3).mean()
b = [x*0.01 for x in range(-13,14)]

fig = plt.figure(figsize=(9,5))

ax1 = plt.subplot(gs[0])
#ax1.set_title('Network Size 1', color='0.4')
#ax1.set_ylabel('Distance to middle', color='b')
#ax1.set_xlabel('NEST time step')
x_max = max(dist_to_middle.size, dist_to_middle2.size, dist_to_middle3.size)
ax1.set_xlim((0,x_max))
ax1.set_xticks([dist_to_middle.size])
ax1.set_ylim((dist_to_middle.min(axis=0)*1.1,dist_to_middle.max(axis=0)))
ax1.plot(dist_to_middle, linewidth=1.0, color='r')

ax2 = plt.subplot(gs[1])
ax2.set_xticklabels([])
ax2.set_yticklabels([])
# ax2.set_ylim((-lim,lim))
ax2.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True)
ax2.set_title('Network Size 1\ne = '+str('{:4.3f}'.format(s1)), loc='left', size='medium', position=(1.1,0.2))
plt.axhline(y=0, linewidth=0.5, color='0.')
plt.hist(dist_to_middle, bins=b, normed=True, color='r', linewidth=0, orientation=u'horizontal')

ax3 = plt.subplot(gs[2])
#ax3.set_title('Network Size 2', color='0.4')
ax3.set_ylabel('Distance to middle', size='15')
ax3.set_xlim((0,x_max))
ax3.set_xticks([dist_to_middle2.size])
#ax3.set_xlabel('NEST time step')
#ax3.set_xlim((0,dist_to_middle2.size))
ax3.set_ylim((dist_to_middle2.min(axis=0)*1.1,dist_to_middle2.max(axis=0)))
ax3.plot(dist_to_middle2, linewidth=1.0, color='g')

ax4 = plt.subplot(gs[3])
ax4.set_xticklabels([])
ax4.set_yticklabels([])
# ax4.set_ylim((-lim,lim))
ax4.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True)
ax4.set_title('Network Size 2\ne = '+str('{:4.3f}'.format(s2)), loc='left', size='medium', position=(1.1,0.2))
plt.axhline(y=0, linewidth=0.5, color='0.')
plt.hist(dist_to_middle2, bins=b, normed=True, color='g', linewidth=0, orientation=u'horizontal')

ax5 = plt.subplot(gs[4])
#ax5.set_title('Network Size 3', color='0.4')
#ax5.set_ylabel('Distance to middle', color='b')
ax5.set_xlabel('NEST time step', size='15')
ax5.set_xlim((0,x_max))
ax5.set_xticks(list(ax5.get_xticks())[:-2] + [dist_to_middle3.size])
#ax5.set_xlim((0,dist_to_middle3.size))
ax5.set_ylim((dist_to_middle3.min(axis=0)*1.1,dist_to_middle3.max(axis=0)))
ax5.plot(dist_to_middle3, linewidth=1.0, color='y')

ax6 = plt.subplot(gs[5])
ax6.set_xticklabels([])
ax6.set_yticklabels([])
# ax6.set_ylim((-lim,lim))
ax6.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True)
ax6.set_title('Network Size 3\ne = '+str('{:4.3f}'.format(s3)), loc='left', size='medium', position=(1.1,0.2))
plt.axhline(y=0, linewidth=0.5, color='0.')
plt.hist(dist_to_middle3, bins=b, normed=True, color='y', linewidth=0, orientation=u'horizontal')
filename = 'performance_1.pdf'
filepath = '../../plots/hidden_not_separated/' + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)