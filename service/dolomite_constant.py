import os
import numpy as np
import pandas as pd
import sys
import data_import_2
import subset_creation
import phreeqc_input_carb_capt
import phreeqc_execute
import carb_cap
import ploting_2d_geochem
import subprocess

from file_paths import geochemical_result, directory, output_data



def main(rawusgs, grad, sur,user_job,geochem_minerals,geochem_minerals_secondary,area,co2_US_state,co2_US_county,co2_lon_lat,radius,height,porosity,session,result):
    """Script for calculating and plotting equilibrium constant for dolomite"""
    #eq_constants_value=True #usuall
    os.mkdir(geochemical_result+'/'+user_job)
    with open(geochemical_result+'/'+user_job+'/session_parameters.txt', 'w') as f:
        print((session,result), file=f)
    eq_constants_value=False
    #print("running data_import")
    medusgs=data_import_2.main(rawusgs,grad,sur,area,co2_US_county,co2_US_state,co2_lon_lat) # nodiff between scripts
    #print("running subset_creation")
    smallusgs,tempnchem,experi1=subset_creation.main(medusgs) # nodiff between scripts
    #print("running phreeqc_input")
    phreeqc_input_carb_capt.main(experi1,smallusgs,eq_constants_value,user_job,geochem_minerals,geochem_minerals_secondary) #change executable file & change bash script
    #print("running phreeqc_execute")
    path_to_user=geochemical_result+'/'+user_job
    print(path_to_user)
    phreeqc_execute.main(eq_constants_value,path_to_user)
    ##print("running eq_constants")  #turn back on!!
    #user_job=89542475 #fix user_job for testing purposes and not having to resim
    merge_out=carb_cap.main(smallusgs,medusgs,user_job,geochem_minerals,geochem_minerals_secondary,radius,height,porosity)
    ploting_2d_geochem.main(merge_out,user_job)
    pipe = subprocess.run([directory+'aws_sync_geochem_results.sh',str(output_data), str('./geochemical_result/'+user_job),str(user_job)])


if __name__ == '__main__':
    main()
