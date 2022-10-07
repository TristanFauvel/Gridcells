import numpy as np
from core import results_saving, grid_learning


def run(parameters_file, session_file, path):
    """Run the model.

    Parameters
    ----------
    parameters_file : str
        Name of the .npy file containing the model's parameters.
    session_file : str
        Name of the .npy file containing the model's parameters.
    Returns
    -------
    Returns a folder for each parameters set. Each folder contains plots
    representing mEC neurons firing rate maps, autocorrelogramms, gridness score histogram, trajectory scatter plot.
    It also contains a file with parameter values used for each session..

    """
    model_parameters = np.load(parameters_file)
    for i in range(model_parameters.shape[0]):
        param_set = model_parameters[
            i,
        ]
        session = np.int(np.array(np.load(session_file) + 1))
        np.save(session_file, session)
        results_saving_path = "{path}\\Results\\Session_{session}".format(
            path=path, session=session
        )
        mEC_layer, trajectory, input_layer = grid_learning.model(param_set, session)
        mEC_layer.save_layer_plots(results_saving_path)
        results_saving.session_statistics_saving(
            results_saving_path, param_set, trajectory, input_layer, mEC_layer
        )
