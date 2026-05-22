import numpy as np
import uproot
from scipy import optimize
import subprocess
import os

#Reminder; you need to clear the output of any previous run.

#define a function to be opimized; returns the sqare root of the squared stds
def beam_deviance(scales):
    os.environ["SCALE15"] = str(scales[0])
    os.environ["SCALE16"] = str(scales[1])
    os.environ["SCALE17"] = str(scales[2])
    os.environ["SCALE18"] = str(scales[3])
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=True)
    with uproot.open("piM1_plastic_decay_bend_air_mu+_155_1.0_300_12348.root") as file:
        #get the standard deviation in x and y at the end
        branch_name = 'NTuple/22150'
        x_vals = file[branch_name]['x'].array(library="np")
        y_vals = file[branch_name]['y'].array(library="np")
        x_std = np.std(x_vals)
        y_std = np.std(y_vals)
    os.remove("piM1_plastic_decay_bend_air_mu+_155_1.0_300_12348.root")
    return np.sqrt(x_std**2+y_std**2)

print("Calling deviance")
ex_scales = [1,1,1,1]
print(beam_deviance(ex_scales))
raise Exception("STOP")

#Arbitrary bounds; if the minimum is found to be very close to 4 or 0.001 for any of them, I will change them.
bounds = [(0.001,4),(0.001,4),(0.001,4),(0.001,4)]

results = dict()
results['DE'] = optimize.differential_evolution(beam_deviance,bounds,workers=1) #Add maxiter = n if this takes too long
print(results['DE'])
