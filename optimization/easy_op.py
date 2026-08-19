import numpy as np
import uproot
import subprocess
import os
import scipy.stats.qmc as qmc
from scipy.stats.qmc import Sobol

'''
A simple optimizing function I wrote that works relatively well for the degrder problem because it treats each variable relatively independently and uses few steps.
'''

def easy_op(dim_guess,function,steps,init_size,rounds):
    for round in range(rounds):
        for dim in range(len(dim_guess)):
            test_range = np.linspace(dim_guess[dim]-init_size/pow(1.5,round),dim_guess[dim]+init_size/pow(1.5,round),steps)
            test_input = dim_guess
            result = [0]*steps
            for istep,step in enumerate(test_range):
                test_input[dim] = step
                #Here you need to input the actual function.
                result[istep] = float(function(test_input))
            min_index = result.index(min(result))
            dim_guess[dim] = test_range[min_index]
    return dim_guess

def easier_op(guess,function,steps,init_size,rounds,workers):
    l_bounds = [x - init_size for x in guess]
    u_bounds = [x + init_size for x in guess]

    sampler = Sobol(d=4, scramble=False)
    sample = sampler.random_base2(m=int(np.ceil(np.log2(workers))))

    qmc.scale(sample, l_bounds, u_bounds)

    best_guess = [999]

    for istart,start in enumerate(sample):
        guess = easy_op(start,function,steps,init_size,rounds)
        if function(guess) < function(best_guess):
            best_guess = guess
    
    return(best_guess)

def beam_deviance(scales):
    os.environ["SCALE15"] = scales[0]
    os.environ["SCALE16"] = scales[1]
    os.environ["SCALE17"] = scales[2]
    os.environ["SCALE18"] = scales[3]
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=True)
    with uproot.open("piM1_plastic_decay_bend_air_mu+_155_1.0_300_12349.root") as file:
        #get the standard deviation in x and y at the end
        branch_name = 'NTuple/22150'
        x_vals = file[branch_name]['x'].array(library="np")
        y_vals = file[branch_name]['y'].array(library="np")
        x_std = np.std(x_vals)
        y_std = np.std(y_vals)
    os.remove("piM1_plastic_decay_bend_air_mu+_155_1.0_300_12349.root")
    return np.sqrt(x_std**2+y_std**2)

def beam_deviance_degrader(scales):
        os.environ["MOMENTUMSCALE"] = str(scales[0])
        subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
        with uproot.open("piM1_plastic_decay_bend_air_mu+_155_1.0_300_12349.root") as file:
            #get the standard deviation in x and y at the end
            branch_name = 'NTuple/Z22159'
            x_vals = file[branch_name]['x'].array(library="np")
        os.remove("piM1_plastic_decay_bend_air_mu+_155_1.0_300_12349.root")
        return -len(x_vals)

print(easier_op([1],beam_deviance_degrader,4,0.5,4,4))
