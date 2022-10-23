import os
import numpy as np
import matplotlib.pyplot as plt

def session_statistics_saving(results_saving_path, param_set, Ag, input_layer, mEC_layer):
    '''Save the gridness score histogram, the trajectory and the parameters used for the session.

    Parameters
    ----------
    results_saving_path: string
        Folder in which the results will be saved
    Ag  :  
        Position of the rat for each time step.
    session: integer
        Index of the session
    param_set:
        Set of parameters used for the session  
    mEC_layer : MEC_Layer object
        list of mEC_neurons objects corresponding to the layer of mEC neurons.
    input_layer : Input_Layer object
        list of Input_Neuron objects corresponding to the input layer.
    arena_size : integer
        Size of the arena in which the virtual rat moves.
    mEC_max_firing_rate : float
        Maximal firing rate of mEC neurons. 
    '''    
    os.chdir(results_saving_path)
    results= {'parameters':param_set, 'trajectory':Ag}
    for key in results.keys():
        if  key=='parameters':
            fname = "Session_{session}_{key}".format(session=mEC_layer.session, key=key)
            np.save(fname, results[key])
        elif key=='trajectory':
             
            fname = "Session_{session}_{key}".format(session=mEC_layer.session, key=key)
            
            fig = Ag.plot_trajectory()
            """
            fig = plt.figure()
            plt.scatter(trajectory[0,:],trajectory[1,:], c='k', s=10, marker='+')
            plt.xlim(0, mEC_layer.arena_size)
            plt.ylim(0, mEC_layer.arena_size)
            plt.close(fig)
            """
            plt.savefig("{fname}.png".format(fname=fname), bbox_inches='tight')
            plt.close()
        else:
            fname = "Session_{session}_{key}".format(session=mEC_layer.session, key=key)
            fig=plt.figure()
            plt.imshow(results[key])
            plt.savefig("{fname}.png".format(fname=fname), bbox_inches='tight')
            plt.close(fig)
    mEC_layer.save_gridness_histogram()
    input_layer.save_input_layer_map()