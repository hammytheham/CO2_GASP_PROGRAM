import os
import numpy as np
import pandas as pd
pd.options.display.max_rows = 4000
import sys

#import modules used in code
import data_import
import CO2_density_state
from co2_gasp_run_options import *     #import the option file from within the same folder

def CO2__thermal_only_sim(grad, sur):
	print('hi')
	CO2_density_state.main(grad, sur)


def main():
	rawusgs, grad, sur =data_import.main()
	if CO2_thermal_only == True:
		CO2__thermal_only_sim(grad, sur)



if __name__ == "__main__":
	main()
