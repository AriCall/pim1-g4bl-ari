import uproot
import os
import subprocess
import numpy as np

'''
This will iterate over all combinations of material, length, and energy regimes listed, then result in a csv with:
material (as a number), length, energy, mucount limitless, poscount limitless, mucount, poscount
Limitless refers to whether there is a 20 mm square cut at the end or not.
'''

material_dict = {
    'Al':np.linspace(0.01,3,50),
    'Be':np.linspace(0.01,8,40),
    'POLYOXYMETHYLENE':np.linspace(2,12,75),
    'Au':np.linspace(0.001,2,50),
}

energy_dict = {
    80:['musource_upsampled_pcut_80.txt','esource_upsampled_pcut_80.txt'],
    100:['musource_upsampled_pcut_100.txt','esource_upsampled_pcut_100.txt'],
    155:['musource_upsampled_pcut_155.txt','esource_upsampled_pcut_155.txt'],
    200:['musource_upsampled_pcut_200.txt','esource_upsampled_pcut_200.txt']
}

seed = os.environ['SEED']
collopen = os.environ['COLLOPEN']
num_events = '50000'

results = np.empty((0,7))

for key, items in material_dict.items():
    os.environ['DEGMATERIAL'] = key
    for length in items:
        os.environ['DEGLENGTH'] = str(length)
        for ekey,eitems in energy_dict.items():
            os.environ['BEAMMOMENTUM']=str(ekey)
            os.environ['SOURCEFILE']=eitems[0]
            os.environ['BEAMPART'] = 'mu+'
            os.environ['NUMEVENTS'] = '50000'
            subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
            with uproot.open(f'piM1_plastic_decay_bend_air_mu+_{ekey}_1_{collopen}_{seed}.root') as file:
                branch_name = 'NTuple/Z12140;1'
                mu_end_momenta = np.mean(file[branch_name]['Pz'].array(library="np"))
                branch_name = 'NTuple/Z10620;1'
                mu_start_momenta = np.mean(file[branch_name]['Pz'].array(library="np"))
            os.environ['MOMENTMUMSCALE'] = str(mu_end_momenta/mu_start_momenta)
            os.environ['NUMEVENTS'] = num_events
            subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
            with uproot.open(f'piM1_plastic_decay_bend_air_mu+_{ekey}_1_{collopen}_{seed}.root') as file:
                branch_name = 'NTuple/Z22159'
                mu_x = file[branch_name]['x'].array(library="np")
                mu_y = file[branch_name]['y'].array(library="np")
                mucount_limitless = len(mu_x)
                mucount = ((mu_x < 10) & (mu_y < 10)).sum()
            os.environ['BEAMPART']='e+'
            os.environ['SOURCEFILE']=eitems[1]
            subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
            with uproot.open(f'piM1_plastic_decay_bend_air_mu+_{ekey}_1_{collopen}_{seed}.root') as file:
                branch_name = 'NTuple/Z22159'
                pos_x = file[branch_name]['x'].array(library="np")
                pos_y = file[branch_name]['y'].array(library="np")
                poscount_limitless = len(mu_x)
                poscount = ((pos_x < 10) & (pos_y < 10)).sum()
            result = np.array([list(material_dict).index(key),length,ekey,mucount_limitless,poscount_limitless,mucount,poscount])
            results = np.vstack((result, results))
np.savetxt('degrader_length_energy_combinations.csv',results,delimiter=',')
