# %%
import os
from core import parameters_setting, run

if __name__ == "__main__":

    path = input(
        "Enter the path to the folder named Gridcells (press enter to choose the default path):"
    )
    if path == "":
        path = "../"

    model_path = "{path}/Gridcells_model".format(path=path)
    os.chdir(model_path)
    session_file = "session_index.npy"

    parameters_file = parameters_setting(model_path)
    run(parameters_file, session_file, path)



# %%
