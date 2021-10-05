#!/bin/bash
cd $1

phreeqc Carb_capt_user_job.txt Carb_capt_user_job.txt.out /home/ec2-user/environment/PHREEQC/phreeqc_files/database/pitzer.dat

echo "phreeqc is run!"
