import numpy as np
import subprocess
import os
import uproot

#generates a series of csv files with x, y, and pz distributions for different degrader combinations.
#for use with degrader_end_vis.  Please forgive the worst spaghetticode you've ever seen.

length_dict = {
    'Be':np.linspace(0.01,2,200),
    'Pb':np.linspace(0.1,1.5,15),
    'Al':np.linspace(0.1,3,30),
    'Au':np.linspace(0.1,1,10)
}

for material, length_list in length_dict.items():
    os.environ["DEGMATERIAL"] = material
    for length in length_list:
        os.environ["DEGLENGTH"] = str(length)
        for source in ['musource.txt','musource_but_positron.txt']:
            os.environ['SOURCEFILE'] = source
            if source == 'musource.txt':
                particle = 'mu+'
            else:
                particle = 'e+'
            os.environ['BEAMPART'] = particle
            subprocess.run("g4bl piM1_mu.g4bl", shell=True, check=False)
            with uproot.open(f'piM1_plastic_decay_bend_air_{particle}_155_1_300_12349.root') as file:
                result = file['NTuple/Z22159;1']['Pz'].array(library="np")
                result = np.vstack((result,file['NTuple/Z22159;1']['x'].array(library="np")))
                result = np.vstack((result,file['NTuple/Z22159;1']['y'].array(library="np")))
            print(f'{material},{particle},{source},{length}')
            os.remove(f"piM1_plastic_decay_bend_air_{particle}_155_1_300_12349.root")
            np.savetxt(f"degrader_datafiles/{material},{str(length)},{particle}.csv", result, delimiter=",")




    