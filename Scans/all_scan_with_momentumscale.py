import uproot
import os
import subprocess
import numpy as np

'''
This will iterate over all combinations of material, length, and energy regimes listed, alongside momentumscale then result in a csv with:
material (as a number), length, energy, mucount limitless, poscount limitless, mucount, poscount
Limitless refers to whether there is a 20 mm square cut at the end or not.
'''

energy_dict = {
    80:['POLYOXYMETHYLENE',np.linspace(8,12,12),'musource_upsampled_pcut_80.txt','esource_upsampled_pcut_80.txt',np.linspace(0.75,0.9,10)],
    100:['POLYOXYMETHYLENE',np.linspace(8,11,12),'musource_upsampled_pcut_100.txt','esource_upsampled_pcut_100.txt',np.linspace(0.9,0.98,10)],
    155:['Au',np.linspace(0.25,0.5,12),'musource_upsampled_pcut_155.txt','esource_upsampled_pcut_155.txt',np.linspace(0.96,1,10)],
    200:['Au',np.linspace(0.001,1.5,12)'musource_upsampled_pcut_200.txt','esource_upsampled_pcut_200.txt',np.linspace(0.98,1,10)]
}

seed = os.environ['SEED']
collopen = os.environ['COLLOPEN']
num_events = '50000'
os.environ['NUMEVENTS']=num_events

results = np.empty((0,8))

for energy,items in energy_dict.items():
    os.environ['BEAMMOMENTUM']=str(energy)
    os.environ['DEGMATERIAL'] = items[0]
    for length in items[1]:
        os.environ['DEGLENGTH']=length
        for momentum_scale in items[-1]:
            os.environ['MOMENTUMSCALE']=str(momentum_scale)
            os.environ['BEAMPART']='mu+'
            os.environ['SOURCEFILE']=items[2]
            subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
            with uproot.open(f'piM1_plastic_decay_bend_air_mu+_{energy}_1_{collopen}_{seed}.root') as file:
                branch_name = 'NTuple/Z22159'
                mu_x = file[branch_name]['x'].array(library="np")
                mu_y = file[branch_name]['y'].array(library="np")
                mucount_limitless = len(mu_x)
                mucount = ((mu_x < 10) & (mu_y < 10)).sum()
            os.environ['BEAMPART']='e+'
            os.environ['SOURCEFILE']=items[3]
            subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
            with uproot.open(f'piM1_plastic_decay_bend_air_mu+_{energy}_1_{collopen}_{seed}.root') as file:
                branch_name = 'NTuple/Z22159'
                pos_x = file[branch_name]['x'].array(library="np")
                pos_y = file[branch_name]['y'].array(library="np")
                poscount_limitless = len(mu_x)
                poscount = ((pos_x < 10) & (pos_y < 10)).sum()
            result = np.array([list(energy_dict).index(energy),length,energy,mucount_limitless,poscount_limitless,mucount,poscount,momentum_scale])
            results = np.vstack((result,results))
                    
np.savetxt('momentum_scale_quicktest.csv',results,delimiter=',')