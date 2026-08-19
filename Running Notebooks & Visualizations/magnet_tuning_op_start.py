import numpy as np
import uproot
from scipy import optimize
import subprocess
import os

#Tunes the first three - but, could be repurposed.

#Reminder; you need to clear the output of any previous run.

#define a function to be opimized; returns the sqare root of the squared stds
def beam_deviance(scales):
    os.environ["SCALE1"] = str(scales[0])
    os.environ["SCALE2"] = str(scales[1])
    os.environ["SCALE3"] = str(scales[2])
    os.environ["FIRSTTURNSCALE"] = str(scales[3])
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=True)
    with uproot.open("piM1_plastic_decay_bend_air_mu+_100_1_300_12349.root") as file:
        #get the standard deviation in x and y at the end
        momenta = file['NTuple/Z8040;1']['Pz'].array(library="np")
    os.remove("piM1_plastic_decay_bend_air_mu+_100_1_300_12349.root")
    return -momenta.size

#Arbitrary bounds; if the minimum is found to be very close to 4 or 0.001 for any of them, I will change them.
bounds = [(0.4,4),(0.4,4),(0.4,4),(0.4,4)]

results = dict()
results['DE'] = optimize.differential_evolution(beam_deviance,bounds,workers=2,maxiter=100) #Add maxiter = n if this takes too long
print(results['DE'])
#with open("tuningOutput.txt", "w") as text_file:
#    text_file.write(f'{results['DE'][x]}, {results['DE'][fun]})
