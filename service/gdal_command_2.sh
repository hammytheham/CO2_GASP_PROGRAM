#!/bin/bash
#run gdal script to produce a interpolated geothemal gradient map for review
#cd $2

#Input parameters for gdal_rasterize
#{ 'BURN' : None, 'DATA_TYPE' : 5, 'EXTENT' : '-179.14733999999999,179.77847,-14.552548999999999,71.352561 [EPSG:4269]', 'EXTRA' : '', 'FIELD' : 'Grad', 'HEIGHT' : 0.1, 'INIT' : None, 'INPUT' : '/Users/hamish/github/co2_gasp/INPUT_DATA/geothermal_result_files/interp_masked_out_1dp_no_filter.shp', 'INVERT' : False, 'NODATA' : 999999999, 'OPTIONS' : '', 'OUTPUT' : 'TEMPORARY_OUTPUT', 'UNITS' : 1, 'WIDTH' : 0.1 }


gdal_rasterize -l temperature_depth_$1_state -a temp_at_f -tr 0.1 0.1 -a_nodata 999999999.0 -te -179.14733999999999 -14.552548999999999 179.77847 71.352561 -ot Float32 -of GTiff $2/temperature_depth_$1_state.shp $2/temperature_depth_$1_state.tif
gdal_rasterize -l temperature_depth_$1_state -a CO2_phase -tr 0.1 0.1 -a_nodata 999999999.0 -te -179.14733999999999 -14.552548999999999 179.77847 71.352561 -ot Float32 -of GTiff $2/temperature_depth_$1_state.shp $2/CO2_phase_val_depth_$1_state.tif
gdal_rasterize -l temperature_depth_$1_state -a CO2_dense -tr 0.1 0.1 -a_nodata 999999999.0 -te -179.14733999999999 -14.552548999999999 179.77847 71.352561 -ot Float32 -of GTiff $2/temperature_depth_$1_state.shp $2/CO2_density_val_depth_$1_state.tif

gdal_rasterize -l temperature_depth_$1_state -a t_climate -tr 0.1 0.1 -a_nodata 999999999.0 -te -179.14733999999999 -14.552548999999999 179.77847 71.352561 -ot Float32 -of GTiff $2/temperature_depth_$1_state.shp $2/temperature_climate_depth_$1_state.tif
gdal_rasterize -l temperature_depth_$1_state -a C_pha_cli -tr 0.1 0.1 -a_nodata 999999999.0 -te -179.14733999999999 -14.552548999999999 179.77847 71.352561 -ot Float32 -of GTiff $2/temperature_depth_$1_state.shp $2/CO2_phase_val_climate_depth_$1_state.tif
gdal_rasterize -l temperature_depth_$1_state -a C_den_cli -tr 0.1 0.1 -a_nodata 999999999.0 -te -179.14733999999999 -14.552548999999999 179.77847 71.352561 -ot Float32 -of GTiff $2/temperature_depth_$1_state.shp $2/CO2_density_val_climate_depth_$1_state.tif

gdal_rasterize -l temperature_depth_$1_state -a TempSur_c -tr 0.1 0.1 -a_nodata 999999999.0 -te -179.14733999999999 -14.552548999999999 179.77847 71.352561 -ot Float32 -of GTiff $2/temperature_depth_$1_state.shp $2/TempSur_c_depth_$1_state.tif
gdal_rasterize -l temperature_depth_$1_state -a Grad -tr 0.1 0.1 -a_nodata 999999999.0 -te -179.14733999999999 -14.552548999999999 179.77847 71.352561 -ot Float32 -of GTiff $2/temperature_depth_$1_state.shp      $2/Grad_depth_$1_state.tif