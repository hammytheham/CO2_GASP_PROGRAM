import os
import numpy as np
import subprocess

#Execute phreeqc
directory='/home/ec2-user/environment/CO2_GASP_PROGRAM/service/'
def main(eq_constants_value,path_to_user):
	pipe = subprocess.run([directory+'bash_phreeqc.sh',path_to_user])




if __name__ == "__main__":
    main()
