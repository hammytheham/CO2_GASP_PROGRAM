import json
import os
import numpy as np
import pandas as pd
import sys
import CO2_density_state
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import Polygon
from geopandas.tools import sjoin

from file_paths import s3_geochem_result, geochemical_input



def intersecting_points(grad_sur,sub_explo):
	geometry=[Point(xy) for xy in zip(grad_sur.Lon_OLD, grad_sur.Lat_OLD)]
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	grad_sur = gpd.GeoDataFrame(grad_sur, crs=crs, geometry=geometry)
	pointsinPolys_intersects=sjoin(grad_sur,sub_explo,how="left")
	grouped = pointsinPolys_intersects[pointsinPolys_intersects['index_right'].notna()]
	grouped.reset_index(inplace=True)
	print('grouped.head')
	print(grouped.head(10))
	return grouped



def location_select(medusgs,area,co2_US_county,co2_US_state,co2_lon_lat):
	if area=='All US':
		sub_explo=CO2_density_state.read_shape_all_US()
		grouped=intersecting_points(medusgs,sub_explo)
	if area=='US state':
		sub_explo=CO2_density_state.read_shape_state(co2_US_state)
		grouped=intersecting_points(medusgs,sub_explo)
	if area=='US county':
		sub_explo=CO2_density_state.read_shape_county(co2_US_county,co2_US_state)
		grouped=intersecting_points(medusgs,sub_explo)
	if area=='Custom mapping':
		spoly=CO2_density_state.bounding_box(co2_lon_lat)
		grouped=intersecting_points(medusgs,sub_explo)
	return groupe d





def main(rawusgs,grad,sur,area,co2_US_county,co2_US_state,co2_lon_lat):
	medusgs=pd.read_csv(s3_geochem_result+'/merged_data_all_samples')
	medusgs_new=location_select(medusgs,area,co2_US_county,co2_US_state,co2_lon_lat)
	return medusgs_new

if __name__ == "__main__":
	main()
