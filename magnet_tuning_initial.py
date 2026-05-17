import numpy as np
import uproot
import subprocess
import os

#os.remove("piM1_plastic_decay_bend_air_mu+_155_1.0_300_12348.root")

range15 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
range16 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
range17 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
range18 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

#in the shape of [15,16,17,18,stdx,stdy,numHits]
result_array = np.empty((0, 7))

ranges = np.arange(0.1, 2.1, 0.1).tolist()
for scale15 in range15:
    print(scale15*10)
    #export the scale value
    os.environ["SCALE15"] = str(scale15)
    for scale16 in range16:
        #export the scale value
        os.environ["SCALE16"] = str(scale16)
        for scale17 in range17:
            #export the scale value
            os.environ["SCALE17"] = str(scale17)
            for scale18 in range18:
                #export the scale value
                os.environ["SCALE18"] = str(scale18)
                #run the simulation
                subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=True)
                #open the root file
                #it should be in the same directory this is being run in.
                with uproot.open("piM1_plastic_decay_bend_air_mu+_155_1.0_300_12348.root") as file:
                    #get the standard deviation in x and y at the end
                    x_vals = file["NTuple"]['Z22159;1']['x'].array(library="np")
                    y_vals = file["NTuple"]['Z22159;1']['y'].array(library="np")
                    num_hits = len(x_vals)
                    x_std = np.std(x_vals)
                    y_std = np.std(y_vals)
                #sqrt(sx^2 + sy^2) saved in numpy array
                new_values = np.array([scale15,scale16,scale17,scale18, x_std, y_std,num_hits])
                result_array = np.vstack([result_array, new_values])
                #delete file
                os.remove("piM1_plastic_decay_bend_air_mu+_155_1.0_300_12348.root")

#save the numpy array to a csv

np.savetxt("tuning_vals_tenths.csv", result_array, delimiter=",")
