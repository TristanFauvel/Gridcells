# %%
import os
from core import parameters_setting, run


if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    query_inputs = False
    if query_inputs:
        model_path = input(
            "Enter the path to the folder named Gridcells (press enter to choose the default path):"
        )
        if model_path == "":
            model_path = dname
    else:        
         model_path = dname

    os.chdir(model_path)
    session_file = "session_index.npy"

     
    parameters_file = parameters_setting(model_path, query_inputs)
    
    path = os.path.dirname(model_path)
   
    run(parameters_file, session_file, path)



# %%
