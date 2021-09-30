import os
import numpy as np
import pandas as pd
import sys

def main():
    """Script for calculating and plotting equilibrium constant for dolomite"""
    #eq_constants_value=True #usuall
    eq_constants_value=False
    print("running data_import")
    medusgs=data_import.main() # nodiff between scripts
    print("running subset_creation")
    smallusgs,tempnchem,experi1=subset_creation.main(medusgs) # nodiff between scripts
    print("running phreeqc_input")
    phreeqc_input_carb_capt.main(experi1,smallusgs,eq_constants_value) #change executable file & change bash script
    ####print("running phreeqc_execute")
    #phreeqc_execute.main(eq_constants_value)
    ##print("running eq_constants")  #turn back on!!
    carb_cap.main(smallusgs,medusgs)

if __name__ == '__main__':
    main()
