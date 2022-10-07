# Gridcell (Tristan Fauvel)

This program is a modified version of the model presented in Kropff, E. and Treves, A. (2008), The emergence of grid cells: Intelligent design or just adaptation?. Hippocampus, 
Some parameters (b3, b4) come from Si, B., Kropff, E., & Treves, A. (2012). Grid alignment in entorhinal cortex. Biological Cybernetics, 106(8�9), 483�506. http://doi.org/10.1007/s00422-012-0513-7

What are grid cells?
A grid cell is a place-modulated neuron whose multiple firing locations define a periodic triangular array covering the entire available surface of an open two-dimensional environment. 
Grid cells are thought to form an essential part of the brain�s coordinate system for metric navigation. 
They have attracted attention because the crystal-like structure underlying their firing fields is not imported from the outside world, but created within the nervous system. Understanding the origin and properties of grid cells is an attractive challenge for anybody wanting to know how brain circuits compute. 

This program implements a competitive hebbian learning process in a medial enthorinal cortex (mEC) neuronal layer receiving inputs from place modulated units in a freely moving virtual rat. 

## Instructions: 

In order to run the model, you should run the script named 'model_lauching.py'.


## Output :

The program creates a file folder containing files reporting the parameters used for the simulation, the gridness score histogram and a plot of the virtual rat's trajectory, as well as folders containing a plot of the autocorrelogram and the firing map of each mEC neuron.


## How the model works:

The model network is composed of a layer of medial enthorinal cortex (mEC) threshold-linear neurons (putative grid cells) receiving inputs from place cells-like space modulated units.
The network is fully connected, with no intra-layer connectivity. The initial synaptic weights are randomly chosen so that there sum is the same between mEC neurons.
A virtual rat follows a smooth random walk in a periodic square box. At each time step mEC neurons receive inputs from place cells depending on their connectivity and the position of the rat.
The network undergoes a competitive hebbian learning, with competition between inputs implemented through synaptic weights normalization. Moreover mEC neurons undergo a fatigue dynamics, so that their
is a time delay between synaptic activation and activity rise of the neuron, as well as an activity decay after sustained activation.
The model also include intra-mEC competition through activity mean and variance control. The values of the gain and the threshold in the neurons' transfer function are indeed updated at each time step to ensure 
that the activity mean and its sparseness stay constant.