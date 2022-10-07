import numpy as np 
from math import floor 
from random import randint, gauss
from core import network

def rat_trajectory(n, arena_size, periodic=True): 
    '''This function draws a random trajectory followed by a virtual rat in a 2D space.
    The rat begins at the center of the arena. New direction is randomly chosen following a normal law. 
    
    Parameters
    ----------
    n : integer
        number of time steps
    speed : integer
        The speed of the rat.
    arena_size : integer
        Size of the arena in which the virtual rat moves.
    periodic :boolean
        If periodic == True, the arena is a torus, otherwise it is a closed arena.
    
    Returns
    -------
    trajectory: 2xn array
        Position of the rat for each time step.
    
    '''
    speed=1
    trajectory=np.zeros((2,n))
    trajectory[:,0]=(floor(arena_size/2),floor(arena_size/2)) 
    i=1
    move_along_x=np.array([1,2,2,1,-1,-2,-2,-1])*speed
    move_along_y=np.array([2,1,-1,-2,-2,-1,1,2])*speed
    direction=randint(0,359) 
    if periodic==True:
        while i<n:
            direction=floor(gauss(direction,10))%360 
            position=trajectory[:,i-1]+(move_along_x[direction//45],move_along_y[direction//45])
            trajectory[:,i]=position%arena_size
            i=i+1 
    else:
        while i<n:
            direction=floor(gauss(direction,10))%360 
            position=trajectory[:,i-1]+(move_along_x[direction//45],move_along_y[direction//45])
            if 0<=position[0]<=arena_size and 0<=position[1]<=arena_size:
                trajectory[:,i]=position
                i=i+1
    return trajectory

def model(param_set, session): 
    '''Compute the spatial firing rate map of mEC neurons.

    Parameters
    ----------
    param_set : list
        param_set contains all the necessary parameters for the model to be run.
        
    Returns
    -------
    mEC_layer : MEC_Layer object
        list of MEC_Neuron objects corresponding to the layer of mEC neurons. 
    arena_size : integer
        Size of the arena in which the virtual rat moves.
    mEC_max_firing_rate : float
        Maximal firing rate of mEC neurons.
    input_layer : Input_Layer object. 
        list of Input_Neuron objects corresponding to the input layer.
    trajectory: 2xn array
        Position of the rat for each time step.
    '''
    n, NmEC, NI, b_1, b_3, b_4,mEC_max_firing_rate,s_0, epsilon, input_max_firing_rate, sigma_x, sigma_y, periodic = param_set
    n, NmEC, NI = np.int(n), np.int(NmEC), np.int(NI)
    b_2=b_1/3
    a_0= 0.1*mEC_max_firing_rate #Mean of the mEC neurons firing rates
    threshold=0.01 
    gain=0.3
    arena_size=20
    total_J=1 
    R_act_0=0
    R_inact_0=0
    trajectory=rat_trajectory(n, arena_size) 
    mEC_layer, input_layer= network(n, NI, arena_size, input_max_firing_rate, sigma_x, sigma_y,  trajectory, NmEC, R_act_0, R_inact_0, total_J, a_0, s_0, gain, threshold, mEC_max_firing_rate, session, periodic, b_1, b_2, b_3, b_4, epsilon)
    for t in range(n):        
        mEC_layer.layer_dynamics(t)
    return mEC_layer, trajectory, input_layer

