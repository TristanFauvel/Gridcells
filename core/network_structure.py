import numpy as np
from math import atan, pi
from scipy.signal import correlate2d
import os
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import rotate
from sklearn.preprocessing import normalize


class MEC_Neuron:
    def __init__(
        self,
        R_act_0,
        R_inact_0,
        J_0,
        neuron_index,
        input_layer,
        arena_size,
        session,
        epsilon,
        b_1,
        b_2,
    ):
        self.input_connectivity = J_0.reshape(1,-1)
        self.R_act = R_act_0
        self.R_inact = R_inact_0
        self.Firing_rate_mean = 0
        self.neuron_index = neuron_index
        self.inputs = input_layer
        self.arena_size = arena_size
        self.session = session
        self.epsilon = epsilon
        self.b_1 = b_1
        self.b_2 = b_2

    def transfer_function(self, total_synaptic_activation):
        return (
            self.layer.mEC_max_firing_rate
            * 2
            / pi
            * atan(self.layer.gain * (total_synaptic_activation - self.layer.threshold))
            * 0.5
            * (np.sign(total_synaptic_activation - self.layer.threshold) + 1)
        )

    def firing_rate_mean(self, total_synaptic_activation):
        self.Firing_rate_mean = self.Firing_rate_mean + 0.05 * (
            self.transfer_function(total_synaptic_activation) - self.Firing_rate_mean
        )
        return self.Firing_rate_mean

    @property
    def firing_rate_map(self):
        firing_map = np.zeros((self.arena_size, self.arena_size))
        X = np.arange(0, self.arena_size)
        Y = np.arange(0, self.arena_size)
        for xi, x in enumerate(X):
            for yi, y in enumerate(Y):
                inputs = np.array(
                    [
                        ineuron.firing_rate_map[xi, yi]
                        for ineuron in self.inputs.input_layer
                    ]
                )
                total_synaptic_activation = (
                    1 / self.inputs.size * np.sum(self.input_connectivity * inputs)
                )
                firing_map[xi, yi] = self.transfer_function(total_synaptic_activation)
        return firing_map

    @property
    def autocorrelogram(self):
        return correlate2d(self.firing_rate_map, self.firing_rate_map, mode= 'same')

    def save_plots(self, results_saving_path):
        path = "{results_saving_path}/Neuron_{neuron_index}".format(
            results_saving_path=results_saving_path,
            session=self.session,
            neuron_index=self.neuron_index,
        )
        os.makedirs(path)
        os.chdir(path)

        fname = "Session_{session}_{neuron_index}_firing_rate_map".format(
            session=self.session, neuron_index=self.neuron_index
        )
        fig = plt.figure()
        plt.imshow(self.firing_rate_map)
        plt.savefig("{fname}.png".format(fname=fname), bbox_inches="tight")
        plt.close(fig)

        fname = "Session_{session}_{neuron_index}_autocorrelogram".format(
            session=self.session, neuron_index=self.neuron_index
        )
        fig = plt.figure()
        plt.imshow(self.autocorrelogram)
        plt.savefig("{fname}.png".format(fname=fname), bbox_inches="tight")
        plt.close(fig)

    def hebbian_learning(self, t):
        self.firing_rate_mean(self.R_act)
        update = self.epsilon * (
            self.inputs.layer_inputs[:, t] * self.transfer_function(self.R_act)
            - self.inputs.mean_inputs[:, t] * self.Firing_rate_mean
        )
        self.input_connectivity += update.reshape(1,-1)
        self.input_connectivity = normalize(self.input_connectivity)

    def neuron_dynamics(self, t):
        synaptic_activation = (
            np.sum(self.input_connectivity * self.inputs.layer_inputs[:, t])
            / self.inputs.size
        )
        self.R_act +=  self.b_1 * (
            synaptic_activation - self.R_inact - self.R_act
        )
        self.R_inact = self.R_inact + self.b_2 * (synaptic_activation - self.R_inact)

    def gridness_score(self, corr_cutRmin):
        autoCorr = self.autocorrelogram
        autoC_xedges = np.arange(0, self.arena_size)
        autoC_yedges = np.arange(0, self.arena_size)

        # Remove the center point
        X, Y = np.meshgrid(autoC_xedges, autoC_yedges)
        autoCorr[np.sqrt(X**2 + Y**2) < corr_cutRmin] = 0

        da = 3
        angles = list(range(0, 180 + da, da))
        crossCorr = []
        # Rotate and compute correlation coefficient
        for angle in angles:
            autoCorrRot = rotate(autoCorr, angle, reshape=False)
            C = np.corrcoef(
                np.reshape(autoCorr, (1, autoCorr.size)),
                np.reshape(autoCorrRot, (1, autoCorrRot.size)),
            )
            crossCorr.append(C[0, 1])

        max_angles_i = np.array([30, 90, 150]) // da
        min_angles_i = np.array([60, 120]) // da

        maxima = np.max(np.array(crossCorr)[max_angles_i])
        minima = np.min(np.array(crossCorr)[min_angles_i])
        G = minima - maxima
        return G


class Input_Neuron:
    def __init__(
        self,
        arena_size,
        x_0,
        y_0,
        input_max_firing_rate,
        sigma_x,
        sigma_y,
        n,
        trajectory,
        periodic,
    ):
        self.Place_field_center = (x_0, y_0)
        self.arena_size = arena_size
        self.sigma = (sigma_x, sigma_y)
        self.input_max_firing_rate = input_max_firing_rate
        self.inputs = np.zeros(n)
        self.periodic = periodic
        self.firing_rate = np.vectorize(self.firing_rate)
        self.firing_rate_along_trajectory = self.firing_rate(
            trajectory[0, :], trajectory[1, :]
        )
        self.Firing_rate_mean = np.zeros(n)
        for t in range(n - 1):
            self.Firing_rate_mean[t + 1] = self.Firing_rate_mean[t] + 0.05 * (
                self.firing_rate_along_trajectory[t + 1] - self.Firing_rate_mean[t]
            )

        self.firing_rate_map = np.zeros((arena_size, arena_size))
        X = np.arange(0, arena_size)
        Y = np.arange(0, arena_size)
        for xi, x in enumerate(X):
            for yi, y in enumerate(Y):
                self.firing_rate_map[xi, yi] = self.firing_rate(x, y)

    def firing_rate(self, x, y):
        if self.periodic == True:
            period = [(0, 0), (0, 1), (1, 1), (1, 0)]
            values = np.array(
                [
                    self.input_max_firing_rate
                    * np.exp(
                        -(
                            (x + self.arena_size * per[0] - self.Place_field_center[0])
                            ** 2
                            / (2 * self.sigma[0] ** 2)
                            + (
                                y
                                + self.arena_size * per[1]
                                - self.Place_field_center[1]
                            )
                            ** 2
                            / (2 * self.sigma[1] ** 2)
                        )
                    )
                    for per in period
                ]
            )
            return np.max(values)
        else:
            return self.input_max_firing_rate * np.exp(
                -(
                    (x - self.Place_field_center[0]) ** 2 / (2 * self.sigma[0] ** 2)
                    + (y - self.Place_field_center[1]) ** 2 / (2 * self.sigma[1] ** 2)
                )
            )


class MEC_Layer:
    def __init__(
        self,
        R_act_0,
        R_inact_0,
        input_layer,
        total_J,
        NmEC,
        a_0,
        s_0,
        gain,
        threshold,
        mEC_max_firing_rate,
        arena_size,
        b_3,
        b_4,
        session,
        epsilon,
        b_1,
        b_2,
    ):
        J_0 = np.zeros((input_layer.size, NmEC))
        for i in range(NmEC):
            J = np.random.rand(1, input_layer.size)
            J_0[:, i] = J * total_J / np.sum(J)
        self.mEC_layer = [
            MEC_Neuron(
                R_act_0,
                R_inact_0,
                J_0[:, i],
                i,
                input_layer,
                arena_size,
                session,
                epsilon,
                b_1,
                b_2,
            )
            for i in range(NmEC)
        ]
        self.size = NmEC
        self.fixed_mean_activity = a_0
        self.fixed_sparseness = s_0
        self.gain = gain
        self.threshold = threshold
        self.mEC_max_firing_rate = mEC_max_firing_rate
        self.b_3 = b_3
        self.b_4 = b_4
        self.session = session
        self.arena_size = arena_size
        for neuron in self.mEC_layer:
            neuron.layer = self

    def layer_dynamics(self, t):
        ok = 0
        # adaptation of the threshold and the gain to ensure that the mean activity and the sparseness stay constant
        while ok == 0:
            for neuron in self.mEC_layer:
                neuron.firing_rate = neuron.transfer_function(neuron.R_act)
                
            layer_activity = np.array([neuron.firing_rate for neuron in self.mEC_layer])
            self.mean_activity = (
                np.sum(layer_activity) / self.size
            )
            s = np.sum(layer_activity**2)
            self.sparseness = 0
            if s != 0:
                self.sparseness = self.size * self.mean_activity**2 / s
            if (
                t < 3000
                or self.size < 100
                or (
                    abs(self.mean_activity - self.fixed_mean_activity)
                    < 0.1 * self.fixed_mean_activity
                    and abs(self.sparseness - self.fixed_sparseness)
                    < 0.1 * self.fixed_sparseness
                )
            ):
                ok = 1
            else:
                if s != 0:
                    self.gain = self.gain + self.b_4 * self.gain * (
                        self.sparseness - self.fixed_sparseness
                    )
                self.threshold = self.threshold + self.b_3 * (
                    self.mean_activity - self.fixed_mean_activity
                )
        for neuron in self.mEC_layer:
            neuron.hebbian_learning(t)
            neuron.neuron_dynamics(t)

    def gridness_score_histogram(self):
        corr_cutRmin = 4  # Corresponds to the size of the central region that will be removed to compute the gridness score.
        gridness_scores = np.array(
            [neuron.gridness_score(corr_cutRmin) for neuron in self.mEC_layer]
        )
        return gridness_scores

    def save_gridness_histogram(self):
        fname = "Session_{session}_gridness_histogram".format(session=self.session)
        fig = plt.figure()
        bins = np.linspace(0, 10, 11)
        plt.hist(self.gridness_score_histogram(), bins, density = True, histtype="bar")
        plt.savefig("{fname}.png".format(fname=fname), bbox_inches="tight")
        plt.close(fig)

    def save_layer_plots(self, results_saving_path):
        for neuron in self.mEC_layer:
            neuron.save_plots(results_saving_path)


class Input_Layer:
    def __init__(
        self,
        n,
        NI,
        arena_size,
        input_max_firing_rate,
        sigma_x,
        sigma_y,
        trajectory,
        session,
        periodic,
    ):
        Place_field_centers = np.random.randint(0, arena_size, (2, NI))
        self.input_layer = [
            Input_Neuron(
                arena_size,
                Place_field_centers[0, i],
                Place_field_centers[1, i],
                input_max_firing_rate,
                sigma_x,
                sigma_y,
                n,
                trajectory,
                periodic,
            )
            for i in range(int(NI))
        ]
        self.layer_inputs = np.zeros((NI, n))
        self.mean_inputs = np.zeros((NI, n))
        self.size = NI
        self.session = session
        for t in range(n):
            self.layer_inputs[:, t] = np.array(
                [ineuron.inputs[t] for ineuron in self.input_layer]
            )
            self.mean_inputs[:, t] = np.array(
                [ineuron.Firing_rate_mean[t] for ineuron in self.input_layer]
            )
        self.input_layer_map = sum(
            np.array([ineuron.firing_rate_map for ineuron in self.input_layer])
        )

    def save_input_layer_map(self):
        fname = "Session_{session}_input_layer_map".format(session=self.session)
        fig = plt.figure()
        plt.imshow(self.input_layer_map)
        plt.savefig("{fname}.png".format(fname=fname), bbox_inches="tight")
        plt.close(fig)


def network(
    n,
    NI,
    arena_size,
    input_max_firing_rate,
    sigma_x,
    sigma_y,
    trajectory,
    NmEC,
    R_act_0,
    R_inact_0,
    total_J,
    a_0,
    s_0,
    gain,
    threshold,
    mEC_max_firing_rate,
    session,
    periodic,
    b_1,
    b_2,
    b_3,
    b_4,
    epsilon,
):
    """Compute the spatial firing rate map of mEC neurons.

    Parameters
    ----------
    NI : integer
        Number of input neurons.
    NmEC : integer
        Number of mEC neurons.
    n : integer
        number of time steps
    trajectory: 2xn array
        Position of the rat for each time step.
    sigma_x : float
        Standard deviation of each input neuron's firing rate along the x axis
    sigma_y : float
        Standard deviation of each input neuron's firing rate along the y axis
    total_J : float
        Sum of a mEC neuron input synaptic weights.
    arena_size : integer
        Size of the arena in which the virtual rat moves.
    mEC_max_firing_rate : float
        Maximal firing rate of input place units.

    Returns
    -------
    mEC_layer : MEC_Layer object
        list of mEC_neurons objects corresponding to the layer of mEC neurons.
    input_layer : Input_Layer object
        list of Input_Neuron objects corresponding to the input layer.
    """
    input_layer = Input_Layer(
        n,
        NI,
        arena_size,
        input_max_firing_rate,
        sigma_x,
        sigma_y,
        trajectory,
        session,
        periodic,
    )
    mEC_layer = MEC_Layer(
        R_act_0,
        R_inact_0,
        input_layer,
        total_J,
        NmEC,
        a_0,
        s_0,
        gain,
        threshold,
        mEC_max_firing_rate,
        arena_size,
        b_3,
        b_4,
        session,
        epsilon,
        b_1,
        b_2,
    )
    return mEC_layer, input_layer
