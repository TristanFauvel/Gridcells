import numpy as np 
from core import network
from tqdm import tqdm
from ratinabox.Environment import Environment
from ratinabox.Agent import Agent

def rat_trajectory(n, arena_size, periodic=False): 
    '''This function draws a random trajectory followed by a virtual rat in a 2D space.
    Parameters
    ----------
    n : integer
        number of time steps
    arena_size : integer
        Size of the arena in which the virtual rat moves.   
    Returns
    -------
    trajectory: 2xn array
        Position of the rat for each time step.
    '''
    
    x0 = 0
    y0 = 0
    x1 = arena_size/100
    y1 = arena_size/100
    
    Agent.speed_mean = 0.08 #m/s
    Agent.speed_coherence_time = 0.7
    Agent.rotation_velocity_std = 120 * np.pi/180 #radians 
    Agent.rotational_velocity_coherence_time = 0.08

    Env= Environment()
    Env.add_wall([[x0,y0],[x1,y1]])

    Ag = Agent(Env)

    for _ in range(n):
        Ag.update()
    
    trajectory = np.array(Ag.history['pos'])*100
                
    return trajectory.transpose()


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
    b_2 = b_1/3
    a_0= 0.1*mEC_max_firing_rate #Mean of the mEC neurons firing rates
    threshold=0.01 
    gain=0.3
    arena_size=20
    total_J=1 
    R_act_0=0
    R_inact_0=0
    trajectory=rat_trajectory(n, arena_size) 
    mEC_layer, input_layer= network(n, NI, arena_size, input_max_firing_rate, sigma_x, sigma_y,  trajectory, NmEC, R_act_0, R_inact_0, total_J, a_0, s_0, gain, threshold, mEC_max_firing_rate, session, periodic, b_1, b_2, b_3, b_4, epsilon)
    print('Computing neural dynamics...')
    for t in tqdm(range(n)):        
        mEC_layer.layer_dynamics(t)
    return mEC_layer, trajectory, input_layer

