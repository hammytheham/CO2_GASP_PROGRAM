import os
import numpy as np
import sys
import pandas as pd
import json
import geopandas as gpd

from file_paths import geochemical_result, directory


def read_in(user_job):
	carb_co2_pre_eq = pd.read_csv(geochemical_result+'/'+str(user_job)+'/Carb_capt_user_job.sel',sep='\t',skipinitialspace=True,header=0) #present equilibrium
	#carb_co2_pre_eq = pd.read_csv(geochemical_result+'/'+user_job+'/Carb_capt_user_job.sel',sep='\t', skiprows=[i for j in (range(1, 11482), range(11483,34442,2)) for i in j],skipinitialspace=True,header=0) #present equilibrium
	initial_chem=carb_co2_pre_eq.iloc[:(int(len(carb_co2_pre_eq)/3))]
	#print(initial_chem.head(10))
	#print(initial_chem.tail(10))
	init_equi=carb_co2_pre_eq.iloc[(int(len(carb_co2_pre_eq)/3)):(int(len(carb_co2_pre_eq))-1):2]
	fin_equi=carb_co2_pre_eq.iloc[((int(len(carb_co2_pre_eq)/3))+1):int(len(carb_co2_pre_eq)):2]
	#print(init_equi.head(10))
	#print(init_equi.tail(10))
	#print(fin_equi.head(10))
	#print(fin_equi.tail(10))	
	
	return initial_chem,init_equi,fin_equi

def poro_converter(fin_equi,geochem_minerals,geochem_minerals_secondary,radius,height,porosity):
	mineral_density = eval(open(directory+'Mineral_dictionary_density.txt').read())
	mineral_mr = eval(open(directory+'Mineral_dictionary_mr.txt').read())
	geochem_minerals = {**geochem_minerals, **geochem_minerals_secondary}
	for col in fin_equi.loc[:,(fin_equi.columns.str.startswith("d_"))].columns:
		if (str(col)) != 'd_CO2(g)':
			colname_out=str(col)+'_vol'
			init_vol=str(col).replace('d_', '')+'_initvol'
			init_min=str(col).replace('d_', '')
			colname_in=str(col)
			fin_equi[colname_out]=(fin_equi[colname_in]*mineral_mr[colname_in])/mineral_density[colname_in]
			fin_equi[init_vol]=(float(geochem_minerals[init_min])*float(mineral_mr[colname_in]))/float(mineral_density[colname_in])
	fin_equi['net_vol_change']=fin_equi.loc[:,(fin_equi.columns.str.startswith("d_"))].sum(axis=1)
	fin_equi['init_vol_sum']=fin_equi.loc[:,(fin_equi.columns.str.endswith("_initvol"))].sum(axis=1)
	fin_equi['change_vol_pc']=((fin_equi['init_vol_sum']+fin_equi['net_vol_change'])-fin_equi['init_vol_sum'])/fin_equi['init_vol_sum']
	fin_equi['mass_g_co2_kgw']=fin_equi['d_CO2(g)']*mineral_mr['CO2']
	#print(fin_equi['mass_g_co2_kgw'].head(10))
	water_volume = np.pi * np.power(float(radius),2) * float(height) * float(porosity)
	pw=(1+(42745*0.695e-6))*1000 #kg/m3
	fin_equi['tonne_co2']=((fin_equi['mass_g_co2_kgw']*pw*water_volume)/1000000)*-1 #g/kgw kg/m3 m3 so /1000 for kg / 1000 for tonne
	fin_equi['tonne_co2_euros']=fin_equi['tonne_co2']*60
	#print(fin_equi['tonne_co2'].head(100))
	#print(fin_equi['tonne_co2_euros'].head(100))
	#print(water_volume)
	#print(fin_equi.head(10))
	return fin_equi





def merge_medusgs(fin_equi_modified,medusgs,user_job):
	#print(fin_equi_modified.head(10))
	#print(medusgs.head(10))
	fin_equi_modified['Number']=fin_equi_modified['soln']-len(fin_equi_modified)
	medusgs['Number']=medusgs.index.values + 1
	merge_out=fin_equi_modified.merge(medusgs,on='Number')
	#print(merge_out.head(10))
	#print(merge_out.tail(10))
	merge_out.to_csv(geochemical_result+'/'+user_job+'/output_data.csv')
	geo_merge_out = gpd.GeoDataFrame(merge_out, geometry=merge_out['geometry'])
	geo_merge_out.to_file(driver='ESRI Shapefile', filename=geochemical_result+'/'+user_job+'/merge_out.shp')
	return merge_out


def main(smallusgs,medusgs,user_job,geochem_minerals,geochem_minerals_secondary,radius,height,porosity):

	initial_chem,init_equi,fin_equi = read_in(user_job)
	fin_equi_modified=poro_converter(fin_equi,geochem_minerals,geochem_minerals_secondary,radius,height,porosity)
	merge_out=merge_medusgs(fin_equi_modified,medusgs,user_job)
	return merge_out

if __name__ == "__main__":
	main()
