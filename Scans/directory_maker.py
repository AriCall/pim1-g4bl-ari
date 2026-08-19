import os
import subprocess
import numpy as np
from pathlib import Path
import shutil
import csv

'''
This creates large directories of energy, material, and collimator length files.
Saves the paths to each file in simulation directory csv.
However, the old directories had issues and have been removed.  
If you want to use this, make sure that the correct sourcefiles are used
'''

energy_dict = {
    150:np.array(['musource.txt','mu+'],['musource_but_positron.txt','e+']),
    100:np.array(['musource_100.txt','mu+'],['esource_100.txt','e+'])
}

material_dict = {
    'Be':np.linspace(0.001,3,50),
    'POLYOXYMETHYLENE':np.linspace(0.001,15,50),
    'Au':np.linspace(0.001,1,50),
}

coll_options = [5,10,25,50,100,150]

for material,lengths in material_dict.items():
    os.environ["DEGMATERIAL"]=material
    for length in lengths:
        os.environ['DEGLENGTH']=length
        output_dir = Path(f'{material}/{length:.4f}')
        output_dir.mkdir(parents = True,exist_ok=True)
        for energy,files in energy_dict.items():
            os.environ['BEAMMOMENTUM']=str(energy)
            for row in files:
                os.environ['SOURCEFILE']=row[0]
                os.environ['BEAMPART']-row[1]
                for coll_open in coll_options:
                    os.environ['COLLOPEN']=str(coll_open)
                    file_path = Path(f'{material}/{length:.4f}/piM1_plastic_decay_bend_air_{row[1]}_{coll_open}_1_5_12351.root')
                    if file_path.exists():
                        print(f'{file_path.name} exists; moving on...')
                        pass
                    else:
                        subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
                        shutil.move(str(file_path),str(output_dir/file_path.name))
                        new_entry = [file_path.name,material,length,energy,row[1],coll_open]
                        with open("simulation_directory.csv","a",newline="",encoding="utf-8") as file:
                            writer = csv.writer(file)
                            writer.writerow(new_entry)


                        
        