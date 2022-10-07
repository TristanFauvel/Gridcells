import os
import numpy as np
def parameters_setting(model_path):
    """
    This script creates a file containing all necessary parameters for the programm to be launched.
    
    """
    os.chdir(model_path)
    parameters_file='parameters.npy'
    
    number_of_sessions=input('Number of sets of parameters: ')
    
    if number_of_sessions == '' :
        number_of_sessions=1
    else : 
        number_of_sessions=eval(number_of_sessions)
    param_set=input('Do you want to set the parameters Y: yes, N: no (keep default parameters):')
    if param_set=='':
        param_set = 'N'
    parameters=np.zeros((number_of_sessions, 13))
    if param_set=='N':
        for i in range(number_of_sessions):
            n, NmEC, NI, b_1, b_3, b_4,mEC_max_firing_rate,s_0, epsilon, input_max_firing_rate, sigma_x, sigma_y, periodic = [1000, 1, 20, 0.1, 0.01, 0.1, 30, 0.03, 0.001, 1000, 3, 3, True]
            #parameters= {'Number of time steps':param_set, 'Number of mEC neurons':NmEC, 'Number of input place units':NI,
                         'Neuronal activation speed':b_1, 'Threshold update speed':b_3, 'Gain update speed':b_4, 'Sparseness':s_0,
                         'Maximal firing rate of input place units':input_max_firing_rate, 'Hebbian learning speed':epsilon, 'Maximal firing rate of mEC neurons':mEC_max_firing_rate,
                         'Standard deviation of each input neuron''s firing rate along the x axis':sigma_x, 'Standard deviation of each input neuron''s firing rate along the y axis':sigma_y, 'Periodicity':periodic}
            
            parameters[i,:]=np.array([[1000, 1, 20, 0.1, 0.01, 0.1, 30, 0.03, 0.001, 1000, 3, 3, True]])
            #n, NmEC, NI, b_1, b_3, b_4,mEC_max_firing_rate, s_0, epsilon, r, max_firing_rate, sigma_x, sigma_y
        np.save(parameters_file, parameters)
    else:
        manually=input('Do you want to import the parameters from a file? Y: yes, N: no (enter the values manually):')
        if manually == 'N' or manually == '':
            parameters_file=input('File name:')
        else:
            for i in range(number_of_sessions):
                n=eval(input('Number of time steps (original model value: 1000000):'))
                NmEC=eval(input('Number of mEC neurons (original model value: 100):'))
                NI = eval(input('Number of input place units(original model value: 200):'))
                b_1=eval(input('Control parameter of the neuronal activation speed(original model value: 0.1)'))
                b_3=eval(input('Control parameter of the threshold update(original model value: 0.01)'))
                b_4=eval(input('Control parameter of the gain update(original model value: 0.01)'))
                s_0=eval(input('Sparseness of the mEC layer activity (original model value: 0.03):'))
                input_max_firing_rate=eval(input('Maximal firing rate of input place units:'))
                epsilon=eval(input('Hebbian learning speed(original model value: 0.001):'))
                mEC_max_firing_rate=eval(input('Maximal firing rate of mEC neurons(original model value: 30):'))
                sigma_x=eval(input('Standard deviation of each input neuron''s firing rate along the x axis'))
                sigma_y=eval(input('Standard deviation of each input neuron''s firing rate along the y axis'))
                periodic=eval(input('Periodicity (True, False):'))
                parameters[i,:]=np.array([n, NmEC, NI, b_1, b_3, b_4, mEC_max_firing_rate, s_0, epsilon, input_max_firing_rate, sigma_x, sigma_y, periodic])
            np.save(parameters_file, parameters)
    return parameters_file
    
    