#!/bin/bash
#run gdal script to produce a interpolated geothemal gradient map for review
cd /Users/hamish/github/co2_gasp/co2_results

#Input parameters for gdal_rasterize
#{ 'BURN' : None, 'DATA_TYPE' : 5, 'EXTENT' : '-179.14733999999999,179.77847,-14.552548999999999,71.352561 [EPSG:4269]', 'EXTRA' : '', 'FIELD' : 'Grad', 'HEIGHT' : 0.1, 'INIT' : None, 'INPUT' : '/Users/hamish/github/co2_gasp/INPUT_DATA/geothermal_result_files/interp_masked_out_1dp_no_filter.shp', 'INVERT' : False, 'NODATA' : 999999999, 'OPTIONS' : '', 'OUTPUT' : 'TEMPORARY_OUTPUT', 'UNITS' : 1, 'WIDTH' : 0.1 }

gdal_rasterize -l temperature_depth_$1_state_$2 -a temp_at_f -tr 0.1 0.1 -a_nodata 999999999.0 -te -179.14733999999999 -14.552548999999999 179.77847 71.352561 -ot Float32 -of GTiff /Users/hamish/github/co2_gasp/co2_results/temperature_depth_$1_state_$2.shp /Users/hamish/github/co2_gasp/co2_results/temperature_depth_$1_state_$2_output.tif

gdal_rasterize -l temperature_depth_$1_state_$2 -a CO2_phase -tr 0.1 0.1 -a_nodata 999999999.0 -te -179.14733999999999 -14.552548999999999 179.77847 71.352561 -ot Float32 -of GTiff /Users/hamish/github/co2_gasp/co2_results/temperature_depth_$1_state_$2.shp /Users/hamish/github/co2_gasp/co2_results/CO2_phase_val_depth_$1_state_$2_output.tif

gdal_rasterize -l temperature_depth_$1_state_$2 -a CO2_dense -tr 0.1 0.1 -a_nodata 999999999.0 -te -179.14733999999999 -14.552548999999999 179.77847 71.352561 -ot Float32 -of GTiff /Users/hamish/github/co2_gasp/co2_results/temperature_depth_$1_state_$2.shp /Users/hamish/github/co2_gasp/co2_results/CO2_density_val_depth_$1_state_$2_output.tif

gdal_rasterize -l temperature_depth_$1_state_$2 -a TempSur_c -tr 0.1 0.1 -a_nodata 999999999.0 -te -179.14733999999999 -14.552548999999999 179.77847 71.352561 -ot Float32 -of GTiff /Users/hamish/github/co2_gasp/co2_results/temperature_depth_$1_state_$2.shp /Users/hamish/github/co2_gasp/co2_results/TempSur_c_depth_$1_state_$2_output.tif

gdal_rasterize -l temperature_depth_$1_state_$2 -a Grad -tr 0.1 0.1 -a_nodata 999999999.0 -te -179.14733999999999 -14.552548999999999 179.77847 71.352561 -ot Float32 -of GTiff /Users/hamish/github/co2_gasp/co2_results/temperature_depth_$1_state_$2.shp /Users/hamish/github/co2_gasp/co2_results/Grad_depth_$1_state_$2_output.tif
