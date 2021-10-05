import os
import numpy as np
import pandas as pd
import sys
import data_import_2
import subset_creation
import phreeqc_input_carb_capt
import phreeqc_execute
import carb_cap

geochemical_result='/home/ec2-user/environment/CO2_GASP_PROGRAM/temp/OUTPUT_DATA/geochemical_result'


def main(rawusgs,grad,sur,user_job,geochem_minerals):
    """Script for calculating and plotting equilibrium constant for dolomite"""
    #eq_constants_value=True #usuall
    eq_constants_value=False
    print("running data_import")
    medusgs=data_import_2.main(rawusgs,grad,sur) # nodiff between scripts
    print("running subset_creation")
    smallusgs,tempnchem,experi1=subset_creation.main(medusgs) # nodiff between scripts
    print("running phreeqc_input")
    phreeqc_input_carb_capt.main(experi1,smallusgs,eq_constants_value,user_job,geochem_minerals) #change executable file & change bash script
    print("running phreeqc_execute")
    path_to_user=geochemical_result+'/'+user_job
    print(path_to_user)
    phreeqc_execute.main(eq_constants_value,path_to_user)
    ##print("running eq_constants")  #turn back on!!
    carb_cap.main(smallusgs,medusgs,user_job)

if __name__ == '__main__':
    main(rawusgs,grad,sur,user_job,geochem_minerals)
