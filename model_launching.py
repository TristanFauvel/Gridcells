# %%
import os
from core import parameters_setting, run


if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dpath = os.path.dirname(abspath)
    os.chdir(dpath)
        
    path = os.getcwd()
    session_file = path + "/Results/session_index.npy"

    query_inputs= False
    parameters_file = parameters_setting(dpath, query_inputs)
    
    #path = os.path.dirname(dpath)
   
    run(parameters_file, session_file, dpath)



# %%
