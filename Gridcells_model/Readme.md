# The emergence of grid cells
Tristan Fauvel (2017)

This program is an implementation of the model presented in Kropff E, Treves A. The emergence of grid cells: Intelligent design or just adaptation? Hippocampus. 2008;18(12):1256-69. doi: 10.1002/hipo.20520. PMID: 19021261.
Si B, Kropff E, Treves A. Grid alignment in entorhinal cortex. Biol Cybern. 2012 Oct;106(8-9):483-506. doi: 10.1007/s00422-012-0513-7. Epub 2012 Aug 15. PMID: 22892761.
This implementation is a computational neuroscience course project. Since some aspects of the original model are not presented in the paper (in particular the animal's trajectory generating process). In order to generate random rat trajectories, the model relies on the RatInABox toolbox (George T, de Cothi W, Clopath C, Stachenfeld K, Barry C. "RatInABox: A toolkit for modelling locomotion and neuronal activity in complex continuous environments" (2022)).

## What are grid cells?
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


## License
This software is distributed under the MIT License. Please refer to the file LICENCE.txt included for details.
