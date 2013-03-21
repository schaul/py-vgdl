'''
Video game description language -- plotting functions.

@author: Tom Schaul
'''

import pylab
from scipy import ones
from pylab import cm
from random import random

def featurePlot(size, states, fMap, plotdirections=False):
    """ Visualize a feature that maps each state in a maze to a continuous value.  
    
    If the states depend on the agent's current orientation, they are split into 4.
    
    Optionally indicate this orientation on the plot too.
    
    Black corresponds to non-state positions. """
    
    from ontology import LEFT, RIGHT, UP, DOWN
    if len(states[0]) > 3:
        polar = True
        M = ones((size[0] * 2, size[1] * 2))
        offsets = {LEFT: (1, 0),
                   UP: (0, 0),
                   RIGHT: (0, 1),
                   DOWN: (1, 1)}    
    else:
        polar = False
        M = ones(size)
    
    cmap = cm.RdGy  # @UndefinedVariable
    vmax = -min(fMap) + (max(fMap) - min(fMap)) * 1
    vmin = -max(fMap)
    M *= vmin 
    
    for si, s in enumerate(states):
        obs = fMap[si]
        if polar:
            x, y, d = s[:3]
            o1, o2 = offsets[d]
            M[2 * x + o1, 2 * y + o2] = obs
        else:
            x, y = s[:2]
            M[x, y] = obs
    
    pylab.imshow(-M.T, cmap=cmap, interpolation='nearest', vmin=vmin, vmax=vmax) 
    if polar and plotdirections:
        for i in range(1, size[0]):
            pylab.plot([i * 2 - 0.5] * 2, [2 - 0.5, (size[1] - 1) * 2 - 0.5], 'k')    
        for i in range(1, size[1]):
            pylab.plot([2 - 0.49, (size[0] - 1) * 2 - 0.49], [i * 2 - 0.49] * 2, 'k')    
        for s in states:
            x, y, d = s[:3]
            o1, o2 = offsets[d]
            pylab.plot([o1 + 2 * x, o1 + 2 * x + d[0] * 0.4], [o2 + 2 * y, o2 + 2 * y + d[1] * 0.4], 'k-')
            pylab.plot([o1 + 2 * x], [o2 + 2 * y], 'k.')
    if polar:
        pylab.xlim(-0.5, size[0] * 2 - 0.5)
        pylab.ylim(-0.5, size[1] * 2 - 0.5)
    else:
        pylab.xlim(-0.5, size[0] - 0.5)
        pylab.ylim(-0.5, size[1] - 0.5)
        
    pylab.xticks([])
    pylab.yticks([])
    
def addTrajectory(state_seq, color='r'):
    """ Draw the trajectory corresponding to a sequence of states on top of a featureplot. """
    def transform(s):
        x, y = s[:2]
        x += random() * 0.6 - 0.3
        y += random() * 0.6 - 0.3
        if len(s) > 3:
            x = x * 2 + 0.5
            y = y * 2 + 0.5
        return x, y
     
    oldx, oldy = transform(state_seq[0])
    
    for s in state_seq[1:]:
        x, y = transform(s)
        pylab.plot([oldx, x], [oldy, y], '.-' + color)
        oldx, oldy = x, y
        
        
    
