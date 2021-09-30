#!/bin/bash
cd $1
zip -r co2_results_$3.zip $2

rm -r $2

aws s3 sync . s3://co-2-gasp-bucket/temp/OUTPUT_DATA/co2_results --delete

rm co2_results_$3.zip



