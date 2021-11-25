import os
import numpy as np
import subprocess
from file_paths import directory
#Execute phreeqc
def main(eq_constants_value,path_to_user):
	pipe = subprocess.run([directory+'bash_phreeqc.sh',path_to_user])




if __name__ == "__main__":
    main()
