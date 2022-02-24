import os
directory=os.getcwd()+'/'
co2_results='../temp_files/OUTPUT_DATA/co2_results'
geochemical_result='../temp_files/OUTPUT_DATA/geochemical_result'
#directory=''
output_data='../temp_files/OUTPUT_DATA'
us_land='../INPUT_DATA/SHAPE_DATA/USA_adm'
geochemical_input='../INPUT_DATA/geochemical_result'

s3_data='s3://co2-gasp-bucket-input/INPUT_DATA'
s3_geotherm_result = 's3://co2-gasp-bucket-input/INPUT_DATA/geothermal_result_files'
s3_MODIS_results = 's3://co2-gasp-bucket-input/INPUT_DATA/MODIS_result_files'
s3_geochem_result = 's3://co2-gasp-bucket-input/INPUT_DATA/geochemical_result_files'
s3_dolomite_stats='s3://co2-gasp-bucket-input/INPUT_DATA/dolomite_stats'