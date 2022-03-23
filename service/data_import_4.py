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

def data_processing1(user_data):
	"""Create a mean of the depth between the upper and lower peforations (ingnoring NaN
	values). Concert to km. Append to database. Rename columns. Make a permant copy to new
	dataframe USGS
	incoming - rawusgs
	outgoing - formated USGS
	"""
	if user_data['DepthKM'].empty == True:
		if user_data['DepthFT'].empty == False:
			user_data['Depth']=  user_data['DepthFT'] * 0.0003048
		if user_data['DepthUpper'].empty == False:
			user_data['Depth']=user_data[['DEPTHUPPER', 'DEPTHLOWER']].mean(axis=1)
			user_data.Depth = user_data.Depth * 0.0003048 # Convert ft to km (km in smuh database)
	print(user_data.head(20))

	user_data = user_data.rename(columns={'LATITUDE': 'Lat', 'LONGITUDE': 'Lon'})
	user_data['Lat_OLD']=user_data['Lat']
	user_data['Lon_OLD']=user_data['Lon']
	print('user_data=',len(user_data))
	sys.exit()
	return user_data

def data_processing2_all_samples(user_data):
	""" Filter the USGS database to a set of geochemical quality control parameters defined
	in the text document. USER - THIS IS WHERE YOU EDIT FILTERING CRITERIA!
	The data is also rounded to the nearest 0.1 lat/lon
	incoming-usgs
	outgoing-usgs1
	"""
	#Cull breakdown for stats
	print('len of original user_data datafram',len(user_data))
	ph=user_data[(user_data.PH >= 3.5 ) & (user_data.PH <= 11 )]
	print('pH fail',100-((len(ph)/len(user_data))*100))
	chargebalance=user_data[(user_data.chargebalance >= -15.0 ) & (user_data.chargebalance <= 15.0 )]
	print('chargebalance',100-((len(chargebalance)/len(user_data))*100))
	mg=user_data[(user_data.Mg > 0.0 ) & (user_data.Ca > 0.0 )]
	print('mg fail',100-((len(mg)/len(user_data))*100))
	depth=user_data[(user_data.Depth > 0.0)]
	print('depth fail',100-((len(depth)/len(user_data))*100))
	lat=user_data[(user_data.Lat > 0.0) & (user_data.Lon < 0.0)]
	print('lat fail',100-((len(lat)/len(user_data))*100))
	lith=user_data
	lith.loc[lith.LITHOLOGY == 'Anhydrite and dolomite','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Chert, Dolomite, Other','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Chert, Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Dolomite','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Dolomite, Limestone','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Dolomite, Limestone, Sandstone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Dolomite, Limestone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Dolomite, Sandstone, Shale','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Dolomite, Shale','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Dolomite, Siltstone','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Sandstone','LITHOLOGY'] = 'Sandstone'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Sandstone, Shale','LITHOLOGY'] = 'Sandstone'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Sandstone, Siltstone','LITHOLOGY'] = 'Sandstone'
	lith.loc[lith.LITHOLOGY == 'Anhydrite, Shale','LITHOLOGY'] = 'Shale'
	lith.loc[lith.LITHOLOGY == 'Carbonate','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Carbonate, Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Carbonate, Sandstone, Shale, Siltstone, Other','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Chalk','LITHOLOGY'] = 'Limestone'
	lith.loc[lith.LITHOLOGY == 'Chert, Dolomite','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Chert, Dolomite, Limestone','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Chert, Dolomite, Limestone, Sandstone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Chert, Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Chert, Dolomite, Sandstone, Shale','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Chert, Dolomite, Shale','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Chert, Limestone','LITHOLOGY'] = 'Limestone'
	lith.loc[lith.LITHOLOGY == 'Chert, Sandstone','LITHOLOGY'] = 'Sandstone'
	lith.loc[lith.LITHOLOGY == 'Dolomite & Lime','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Dolomite - Lime','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Dolomite, Limestone','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Dolomite, Limestone, Sandstone','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Dolomite, Limestone, Sandstone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Dolomite, Limestone, Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Dolomite, Limestone, Sandstone, Siltstone','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Dolomite, Limestone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Dolomite, Sandstone, Shale','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Dolomite, Sandstone, Siltstone','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Dolomite, Shale','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Dolomite, Siltstone','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Limestone & Dol','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Limestone & San','LITHOLOGY'] = 'Limestone'
	lith.loc[lith.LITHOLOGY == 'Limestone & Sha','LITHOLOGY'] = 'Limestone'
	lith.loc[lith.LITHOLOGY == 'Limestone - Dol','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Limestone Dolom','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Limestone, Sandstone','LITHOLOGY'] = 'Limestone'
	lith.loc[lith.LITHOLOGY == 'Limestone, Sandstone, Shale','LITHOLOGY'] = 'Limestone'
	lith.loc[lith.LITHOLOGY == 'Limestone, Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Limestone'
	lith.loc[lith.LITHOLOGY == 'Limestone, Sandstone, Siltstone','LITHOLOGY'] = 'Limestone'
	lith.loc[lith.LITHOLOGY == 'Limestone, Shale','LITHOLOGY'] = 'Limestone'
	lith.loc[lith.LITHOLOGY == 'Limestone; Dolostone','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Sand','LITHOLOGY'] = 'Sandstone'
	lith.loc[lith.LITHOLOGY == 'Sand Stone','LITHOLOGY'] = 'Sandstone'
	lith.loc[lith.LITHOLOGY == 'Sandstone, Other','LITHOLOGY'] = 'Sandstone'
	lith.loc[lith.LITHOLOGY == 'Sandstone, Shale','LITHOLOGY'] = 'Sandstone'
	lith.loc[lith.LITHOLOGY == 'Sandstone, Shale, Other','LITHOLOGY'] = 'Sandstone'
	lith.loc[lith.LITHOLOGY == 'Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Sandstone'
	lith.loc[lith.LITHOLOGY == 'Sandstone, Shale, Siltstone, Other','LITHOLOGY'] = 'Sandstone'
	lith.loc[lith.LITHOLOGY == 'Sandstone, Siltstone','LITHOLOGY'] = 'Sandstone'
	lith.loc[lith.LITHOLOGY == 'Sandstone, Siltstone, Other','LITHOLOGY'] = 'Sandstone'
	lith.loc[lith.LITHOLOGY == 'Shale, Other','LITHOLOGY'] = 'Shale'
	lith.loc[lith.LITHOLOGY == 'Shale, Siltstone','LITHOLOGY'] = 'Shale'
	lith.loc[lith.LITHOLOGY == 'Siltstone','LITHOLOGY'] = 'Shale'
	print('lith fail',100-((len(lith)/len(usgs))*100))
	#Sequential cull
	print('lith=',len(lith))
	lith=lith[(lith.PH >= 3.5 ) & (lith.PH <= 11 )]
	print('lith ph=',len(lith))
	lith=lith[(lith.chargebalance >= -15.0 ) & (lith.chargebalance <= 15.0 )]
	print('lith chargebalance=',len(lith))
	lith=lith[(lith.Mg > 0.0 ) & (lith.Ca > 0.0 )]
	print('lith non-zero Mg Ca=',len(lith))
	lith=lith[(lith.Depth > 0.0)]
	print('lith depth=',len(lith))
	lith=lith[(lith.Lat > 0.0) & (lith.Lon < 0.0)]
	print('lith lat-lon=',len(lith))
	#lith=lith.loc[~(pd.isnull(lith.LITHOLOGY))] #not ~ null lithology
	print('lith lithology=',len(lith))
	lith=lith.round({'Lat':1,'Lon':1})
	print("percent remaining", len(lith), 1 - len(lith)/165960 )
	user_data_1=lith.copy()
	print('user_data_1=',len(user_data_1))
	return user_data_1

def data_processing6(user_data_1,sur,grad):
	"""Merge the dataframes into a single dataframe called medusgs
	currently the field mapping section is working but generating inaccurate results relativel yot the original codes so
	is unused at present
	"""
	print('usgs2 = ',len(usgs1))
	medusgs=usgs1.merge(sur,on=['Lat','Lon'])
	print('medusgs =',len(medusgs))
	medusgs=grad.merge(medusgs,on=['Lat','Lon'])
	print('medusgs with grad =',len(medusgs))
	print((len(medusgs)/len(usgs1))*100)

	print(medusgs.FIELD.head(30))
	unknown_field_list=[]
	for i in list(range(len(medusgs[medusgs['FIELD'].isnull()]))):
		val='unknown_field_'+str(i)
		unknown_field_list.append(val)
	#print(unknown_field_list)
	medusgs.loc[medusgs['FIELD'].isnull(),'FIELD']=unknown_field_list

	from string import ascii_uppercase
	import itertools


	def iter_all_strings():
		size = 1
		while True:
			for s in itertools.product(ascii_uppercase, repeat=size):
				yield "".join(s)
			size +=1
	a=[]
	for s in iter_all_strings():
		a.append(s)
		if len(a) == len(medusgs.FIELD.unique()):
			break

	#with open(geochemical_input+'/FIELD_unique.txt', 'w') as f: #change from backup if neccessary
	#	f.write("{")
	#	for i in list(range(len(medusgs.FIELD.unique()))):
	#		f.write('"%(spss)s" : "%(a)s", \n'  %{'spss':medusgs.FIELD.unique()[i],'a':a[i]})
	#	f.write("}") #note need to read in formated version i.e. lose last comma

	with open(geochemical_input+'/FIELD_unique.txt') as f:
		data = f.read()
	field_1 = json.loads(data)

	with open(geochemical_input+'/FIELD_unique_backup_backup.txt') as f:
		data = f.read()
	field_2 = json.loads(data)

	dictionary=dict(field_1, **field_2)

	with open(geochemical_input+'/FIELD_all_fields.txt', 'w') as f:
		f.write(json.dumps(dictionary))
	#print(dictionary)



	print('Sandstone=',len(medusgs[medusgs.LITHOLOGY == 'Sandstone']),(len(medusgs[medusgs.LITHOLOGY == 'Sandstone'])/len(medusgs))*100)
	print('Dolomite=',len(medusgs[medusgs.LITHOLOGY == 'Dolomite']),(len(medusgs[medusgs.LITHOLOGY == 'Dolomite'])/len(medusgs))*100)
	print('Limestone=',len(medusgs[medusgs.LITHOLOGY == 'Limestone']),(len(medusgs[medusgs.LITHOLOGY == 'Limestone'])/len(medusgs))*100)
	print('Shale=',len(medusgs[medusgs.LITHOLOGY == 'Shale']),(len(medusgs[medusgs.LITHOLOGY == 'Shale'])/len(medusgs))*100)
	print('Mixed_Carbonate=',len(medusgs[medusgs.LITHOLOGY == 'Mixed_Carbonate']),(len(medusgs[medusgs.LITHOLOGY == 'Mixed_Carbonate'])/len(medusgs))*100)
	medusgs['TemperatureSMU']= (medusgs.Depth * medusgs.Grad) + medusgs.TempSur_celsius #Adding in the surface temperature correction
	print('medusgs.head',medusgs.head(5))
	print('medusgs=',len(medusgs))

	di=dictionary
	print(di)
	print(medusgs.columns.values)
	medusgs.FIELD_code=medusgs.FIELD.map(di)
	medusgs['DepthID']=medusgs.FIELD_code+medusgs.groupby('FIELD')['TemperatureSMU'].apply(lambda x:x.astype('category').cat.codes).astype(str)
	print(medusgs[['DepthID','FIELD']].head(20))
	#medusgs.to_csv(S3_geochem_result+'/merged_data', index=False)
	medusgs.to_csv(s3_geochem_result+'/merged_data_all_samples', index=False)
	return medusgs


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
	return grouped



def main(rawusgs,grad,sur,area,co2_US_county,co2_US_state,co2_lon_lat):
	'''Reads the collated main PWGD dataset - no procesing but is compatible with main_read_in'''
	#usgs=data_processing1(rawusgs) #not used unless accessing/testing full functionality
	#usgs1=data_processing2_all_samples(usgs) #not used unless accessing/testing full functionality
	#medusgs=data_processing6(usgs1,sur,grad) #not used unless accessing/testing full functionality
	medusgs=pd.read_csv(s3_geochem_result+'/merged_data_all_samples')
	medusgs_new=location_select(medusgs,area,co2_US_county,co2_US_state,co2_lon_lat)
	return medusgs_new

def main_user_supply(rawusgs,grad,sur):
	'''For user supplied data'''
	usgs=data_processing1(rawusgs) 
	usgs1=data_processing2_all_samples(usgs) 
	medusgs=data_processing6(usgs1,sur,grad)
	medusgs_new=location_select(medusgs,area,co2_US_county,co2_US_state,co2_lon_lat)
	return medusgs_new
	
if __name__ == "__main__":
	main(rawusgs,grad,sur,area,co2_US_county,co2_US_state,co2_lon_lat)
