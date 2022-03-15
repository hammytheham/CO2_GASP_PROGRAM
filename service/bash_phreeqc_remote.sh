#!/bin/bash
#pwd #/service
#ls -l
cd $1 #/temp_files/OUTPUT_DATA/geochemical_result/395313063
#pwd
#ls -l
#cd .. #/temp_files/OUTPUT_DATA/geochemical_result/
#pwd
#ls -l
#cd ~ #/root
#pwd
#ls -l


#~/service/PHREEQC/phreeqc_files/bin/phreeqc Carb_capt_user_job.txt Carb_capt_user_job.txt.out ~/service/PHREEQC/phreeqc_files/PHREEQC/phreeqc_files/database/pitzer.dat
#./service/PHREEQC/phreeqc_files/bin/phreeqc Carb_capt_user_job.txt Carb_capt_user_job.txt.out ~/service/PHREEQC/phreeqc_files/PHREEQC/phreeqc_files/database/pitzer.dat
phreeqc Carb_capt_user_job.txt Carb_capt_user_job.txt.out ../pitzer.dat

#~/../service/PHREEQC/phreeqc_files/bin/phreeqc Carb_capt_user_job.txt Carb_capt_user_job.txt.out ~/../service/PHREEQC/phreeqc_files/PHREEQC/phreeqc_files/database/pitzer.dat
#/temp_files/OUTPUT_DATA/geochemical_result/395313063
#../../../../service/PHREEQC/phreeqc_files/bin/phreeqc
echo "phreeqc is run!"
