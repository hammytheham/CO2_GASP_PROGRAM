import CoolProp.CoolProp as CP
import os
import numpy as np
import pandas as pd
from co2_gasp_run_options import *     #import the option file from within the same folder
import geopandas as gpd
import sys
from shapely.geometry import Point
from shapely.geometry import Polygon
from geopandas.tools import sjoin
import subprocess
import matplotlib.pyplot as plt
import ploting_vertical_co2
#from data_import import boto3_file_read

from file_paths import directory, us_land, co2_results, output_data


#could probably save merge data and grad_sur_calcs as pre-processed data
def merge_data(grad, sur):
	grad_sur=grad.merge(sur,on=['Lat','Lon'])
	return grad_sur



def grad_sur_calcs(grad_sur,co2_depth,land_sur_correct):
	grad_sur['TempSur_c']=grad_sur['TempSur_celsius']
	grad_sur['temp_at_f']=(grad_sur['TempSur_c']+grad_sur['Grad']*(co2_depth/1000))
	grad_sur['t_climate']=grad_sur['TempSur_c']+int(land_sur_correct)+(grad_sur['Grad']*(co2_depth/1000))
	pw=(1+(42745*0.695e-6))*1000 #kg/m3
	grad_sur['pressure']=pw*9.81*co2_depth  #kg/m-1 s-2
	grad_sur['CO2_dense']=grad_sur.apply(f1,args=['temp_at_f','pressure'], axis=1)
	grad_sur['CO2_phase']=grad_sur.apply(f2,args=['temp_at_f','pressure'], axis=1)
	grad_sur['C_den_cli']=grad_sur.apply(f1,args=['t_climate','pressure'], axis=1)
	grad_sur['C_pha_cli']=grad_sur.apply(f2,args=['t_climate','pressure'], axis=1)
	return grad_sur


def f1(x,temp,pres):
	return CP.PropsSI('D', 'T', x[temp]+273.15, 'P', x[pres], 'CO2')

def f2(x,temp,pres):
	return CP.PropsSI('Phase', 'T', x[temp]+273.15, 'P', x[pres], 'CO2')


#def f1(x):
#	return CP.PropsSI('D', 'T', x['temp_at_f'], 'P', x['pressure'], 'CO2')
#def f2(x):
#	return CP.PropsSI('Phase', 'T', x['temp_at_f'], 'P', x['pressure'], 'CO2')
#def f3(x):
#	return CP.PropsSI('D', 'T', x['temp_kel_min'], 'P', x['pressure'], 'CO2')
#def f4(x):
#	return CP.PropsSI('Phase', 'T', x['temp_kel_min'], 'P', x['pressure'], 'CO2')
#def f5(x):
#	return CP.PropsSI('D', 'T', x['temp_kel_max'], 'P', x['pressure'], 'CO2')
#def f6(x):
#	return CP.PropsSI('Phase', 'T', x['temp_kel_max'], 'P', x['pressure'], 'CO2')


#def vertical_profile(grad_sur):
#	surface_temp_mean=grad.loc[]
#	gradient_mean
#	D_T=pd.DataFrame({'Depth':-np.arange(0,5000,1),'temp_cel_climate':(np.arange(0,5000,1)*(nesson.Grad.mean()/1000))+nesson.TempSur_celsius.mean()+2,	'temp_cel':(np.arange(0,5000,1)*(nesson.Grad.mean()/1000))+nesson.TempSur_celsius.mean(),'temp_min':(np.arange(0,5000,1)*(nesson.Grad.min()/1000))+nesson.TempSur_celsius.mean(),'temp_max':(np.arange(0,5000,1)*(nesson.Grad.max()/1000))+nesson.TempSur_celsius.mean()})
#
#	D_T['pressure']=pw*9.81*D_T['Depth_m']*-1  #kg/m-1 s-2
#	D_T.drop(D_T.index[[0]],axis=0, inplace=True)
#
#
#
#	grayburg['pressure']=grayburg['pressure']*101325
#	grayburg['temp_k']=grayburg['temp_phreeqc']+273.15
#
#	def f1(x):
#		return CP.PropsSI('D', 'T', x['temp_k'], 'P', x['pressure'], 'CO2')
#	grayburg['co2_den']=grayburg.apply(f1, axis=1)



def read_shape_all_US():
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	boundary_us = gpd.read_file(us_land+'/USA_adm0.shp',crs=crs)
	exploded=boundary_us.loc[boundary_us['NAME_0']=='United States'].explode()
	box=[(-128.600464,24.374619),(-128.600464,50.406767),(-60.748901,50.406767),(-60.748901,24.374619)]
	poly = Polygon(box)
	spoly = gpd.GeoSeries([poly],crs=crs)
	xmin, ymin, xmax, ymax = spoly.total_bounds
	#sub_explo=country_boundary_us.cx[xmin:xmax,ymin:ymax]
	sub_explo=exploded.cx[xmin:xmax,ymin:ymax]
	#print(sub_explo.head())
	sub_explo=sub_explo.reset_index().drop(['ID_0' , 'ISO'   , 'NAME_0' ,'OBJECTID_1', 'ISO3', 'NAME_ENGLI', 'NAME_ISO', 'NAME_FAO', 'NAME_LOCAL', 'NAME_OBSOL', 'NAME_VARIA', 'NAME_NONLA', 'NAME_FRENC', 'NAME_SPANI', 'NAME_RUSSI', 'NAME_ARABI', 'NAME_CHINE', 'WASPARTOF', 'CONTAINS', 'SOVEREIGN', 'ISO2', 'WWW', 'FIPS', 'ISON', 'VALIDFR', 'VALIDTO', 'POP2000', 'SQKM', 'POPSQKM', 'UNREGION1', 'UNREGION2', 'DEVELOPING', 'CIS', 'Transition', 'OECD', 'WBREGION', 'WBINCOME', 'WBDEBT', 'WBOTHER', 'CEEAC', 'CEMAC', 'CEPLG', 'COMESA', 'EAC', 'ECOWAS', 'IGAD', 'IOC', 'MRU', 'SACU', 'UEMOA', 'UMA', 'PALOP', 'PARTA', 'CACM', 'EurAsEC', 'Agadir', 'SAARC', 'ASEAN', 'NAFTA', 'GCC', 'CSN', 'CARICOM', 'EU', 'CAN', 'ACP', 'Landlocked', 'AOSIS', 'SIDS', 'Islands', 'LDC'],axis=1)
	#print('sub explo read')
	return sub_explo

def intersecting_points_all_US(grad_sur,sub_explo,co2_depth,user_job):
	geometry=[Point(xy) for xy in zip(grad_sur.Lon, grad_sur.Lat)]
	grad_sur.drop(['Lon', 'Lat'], axis=1)
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	grad_sur = gpd.GeoDataFrame(grad_sur, crs=crs, geometry=geometry)
	pointsinPolys_intersects=sjoin(grad_sur,sub_explo,how="left")
	grouped = pointsinPolys_intersects.groupby('index_right')
	grouped=grouped.apply(lambda x: x.reset_index(drop = True))
	grouped=grouped.dropna(axis=0)
	grouped=grouped.set_index(grouped.columns[0]).reset_index()
	#print(grouped.head(10))
	grouped.to_file(driver='ESRI Shapefile',filename= co2_results+'/temperature_depth_%i_all_US.shp'%(co2_depth))
	pipe = subprocess.run([directory+'gdal_command_1.sh',str(co2_depth)])
	#print('gdal command run')
	#print(grouped.head())
	grouped.to_csv(co2_results+'/'+user_job+'/temperature_depth_%i_all_US.csv'%(co2_depth))
	return grouped


def read_shape_state(co2_US_state):
	#print(co2_US_state)
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	state_boundary_us = gpd.read_file(us_land+'/USA_adm1.shp',crs=crs)
	#print(state_boundary_us)
	exploded=state_boundary_us.loc[state_boundary_us['NAME_1']==co2_US_state].explode()
	box=[(-128.600464,24.374619),(-128.600464,50.406767),(-60.748901,50.406767),(-60.748901,24.374619)]
	poly = Polygon(box)
	spoly = gpd.GeoSeries([poly],crs=crs)
	xmin, ymin, xmax, ymax = spoly.total_bounds
	#sub_explo=country_boundary_us.cx[xmin:xmax,ymin:ymax]
	sub_explo=exploded.cx[xmin:xmax,ymin:ymax]
	#print(sub_explo.head())
	sub_explo=sub_explo.reset_index().drop(['ID_0' , 'ISO'   , 'NAME_0' , 'ID_1' ,'NAME_1' ,'TYPE_1', 'ENGTYPE_1' ,'NL_NAME_1', 'VARNAME_1' ],axis=1)
	#print('sub explo read')
	return sub_explo

#def temp_at_form(grad_sur):
#	D_T=pd.DataFrame({'Depth':-np.arange(0,10000,1),'temp_cel_climate':(np.arange(0,10000,1)*(nesson.Grad.mean()/1000))+(nesson.TempSur_celsius.mean()+land_sur_correct[0]),	'temp_cel':(np.arange(0,10000,1)*(nesson.Grad.mean()/1000))+nesson.TempSur_celsius.mean(),'temp_min':(np.arange(0,10000,1)*(nesson.Grad.min()/1000))+nesson.TempSur_celsius.mean(),'temp_max':(np.arange(0,10000,1)*(nesson.Grad.max()/1000))+nesson.TempSur_celsius.mean()})


def intersecting_points_state(grad_sur,sub_explo,co2_US_state,co2_depth,user_job):
	geometry=[Point(xy) for xy in zip(grad_sur.Lon, grad_sur.Lat)]
	grad_sur.drop(['Lon', 'Lat'], axis=1)
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	grad_sur = gpd.GeoDataFrame(grad_sur, crs=crs, geometry=geometry)
	pointsinPolys_intersects=sjoin(grad_sur,sub_explo,how="left")
	grouped = pointsinPolys_intersects.groupby('index_right')
	grouped=grouped.apply(lambda x: x.reset_index(drop = True))
	grouped=grouped.dropna(axis=0)
	grouped=grouped.set_index(grouped.columns[0]).reset_index()
	#print(grouped.head(10))
	grouped.to_file(driver='ESRI Shapefile', filename=co2_results+'/'+user_job+'/temperature_depth_%i_state.shp'%(co2_depth))
	pipe = subprocess.run([directory+'gdal_command_2.sh',str(co2_depth),str(co2_results+'/'+user_job)])
	#print('gdal command run')
	#print(grouped.head())
	grouped.to_csv(co2_results+'/'+user_job+'/temperature_depth_%i_state.csv'%(co2_depth))
	return grouped


def read_shape_county(co2_US_county,co2_US_state):
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	county_boundary_us = gpd.read_file(us_land+'/USA_adm2.shp',crs=crs)
	#print(list(co2_US_county))
	exploded=county_boundary_us.loc[(county_boundary_us['NAME_2'].isin(co2_US_county.split(",")))&(county_boundary_us['NAME_1'].isin([co2_US_state]))].explode()
	box=[(-128.600464,24.374619),(-128.600464,50.406767),(-60.748901,50.406767),(-60.748901,24.374619)]
	poly = Polygon(box)
	spoly = gpd.GeoSeries([poly],crs=crs)
	xmin, ymin, xmax, ymax = spoly.total_bounds
	#sub_explo=country_boundary_us.cx[xmin:xmax,ymin:ymax]
	sub_explo=exploded.cx[xmin:xmax,ymin:ymax]
	#print(sub_explo.head())
	sub_explo=sub_explo.reset_index().drop(['ID_0' , 'ISO'   , 'NAME_0' , 'ID_1' ,'NAME_1' ,'ID_2', 'NAME_2',  'TYPE_2', 'ENGTYPE_2', 'NL_NAME_2', 'VARNAME_2' ],axis=1)
	#print('sub explo read')
	return sub_explo


def intersecting_points_county(grad_sur,sub_explo,co2_US_county,co2_depth,user_job):
	geometry=[Point(xy) for xy in zip(grad_sur.Lon, grad_sur.Lat)]
	grad_sur.drop(['Lon', 'Lat'], axis=1)
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	grad_sur = gpd.GeoDataFrame(grad_sur, crs=crs, geometry=geometry)
	pointsinPolys_intersects=sjoin(grad_sur,sub_explo,how="left")
	grouped = pointsinPolys_intersects.groupby('index_right')
	grouped=grouped.apply(lambda x: x.reset_index(drop = True))
	grouped=grouped.dropna(axis=0)
	grouped=grouped.set_index(grouped.columns[0]).reset_index()
	#print(grouped.head(10))
	grouped.to_file(driver='ESRI Shapefile', filename=co2_results+'/'+user_job+'/temperature_depth_%i_county.shp'%(co2_depth))
	pipe = subprocess.run([directory+'gdal_command_3.sh',str(co2_depth),str(co2_results+'/'+user_job)])
	#print('gdal command run')
	#print(grouped.head())
	grouped.to_csv(co2_results+'/'+user_job+'/temperature_depth_%i_county.csv'%(co2_depth))
	return grouped


def intersecting_points_custom(grad_sur,spoly,co2_depth,user_job):
	geometry=[Point(xy) for xy in zip(grad_sur.Lon, grad_sur.Lat)]
	grad_sur.drop(['Lon', 'Lat'], axis=1)
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	grad_sur = gpd.GeoDataFrame(grad_sur, crs=crs, geometry=geometry)
	pointsinPolys_intersects=sjoin(grad_sur,spoly,how="left")
	grouped = pointsinPolys_intersects.groupby('index_right')
	grouped=grouped.apply(lambda x: x.reset_index(drop = True))
	grouped=grouped.dropna(axis=0)
	grouped=grouped.set_index(grouped.columns[0]).reset_index()
	#print(grouped.head(10))
	grouped.to_file(driver='ESRI Shapefile', filename=co2_results+'/'+user_job+'/temperature_depth_%i_custom.shp'%(co2_depth)) #'s3://co-2-gasp-bucket/'+co2_results+'/temperature_depth_%i_custom.shp'%(co2_depth))
	pipe = subprocess.run([directory+'gdal_command_4.sh',str(co2_depth),str(co2_results+'/'+user_job)])
	#print('gdal command run')
	#print(grouped.head())
	grouped.to_csv(co2_results+'/'+user_job+'/temperature_depth_%i_custom.csv'%(co2_depth))
	return grouped


def bounding_box(co2_lon_lat):
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	co2_lat_lon_list=zip(*co2_lon_lat.values())
	poly = Polygon(co2_lat_lon_list)
	spoly = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[poly])
	return spoly



def intersecting_points_state_vertical(grad_sur,sub_explo,min_vert_depth,max_vert_depth,land_sur_correct,user_job):
	geometry=[Point(xy) for xy in zip(grad_sur.Lon, grad_sur.Lat)]
	grad_sur.drop(['Lon', 'Lat','pressure','CO2_dense','temp_at_f','CO2_phase'], axis=1)
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	grad_sur = gpd.GeoDataFrame(grad_sur, crs=crs, geometry=geometry)
	pointsinPolys_intersects=sjoin(grad_sur,sub_explo,how="left")
	grouped = pointsinPolys_intersects.groupby('index_right')
	grouped=grouped.apply(lambda x: x.reset_index(drop = True))
	grouped=grouped.dropna(axis=0)
	grouped=grouped.set_index(grouped.columns[0]).reset_index()
	#print(grouped.head(15))
	lw=int(min_vert_depth)
	up=int(max_vert_depth)
	pw=(1+(42745*0.695e-6))*1000 #kg/m3
	D_T=pd.DataFrame({'Depth':np.arange(lw,up,1)*-1,
	'pressure':np.arange(lw,up,1)*pw*9.81,
	'temp_cel_climate':(np.arange(lw,up,1)*(grouped.Grad.median()/1000))+grouped.TempSur_c.median()+int(land_sur_correct),
	'temp_cel':(np.arange(lw,up,1)*(grouped.Grad.median()/1000))+grouped.TempSur_c.median(),
	'temp_min':(np.arange(lw,up,1)*(grouped.Grad.min()/1000))+grouped.TempSur_c.median(),
	'temp_max':(np.arange(lw,up,1)*(grouped.Grad.max()/1000))+grouped.TempSur_c.median(),
	'Grad':grouped.Grad.median(),
	'Sur':grouped.TempSur_c.median()})
	#print('D_T')
	#print(D_T.head(15))

	
	#print(D_T.apply(f1,args=('temp_cel','pressure'), axis=1))
	D_T['co2_den']=D_T.apply(f1,args=('temp_cel','pressure'), axis=1)
	D_T['co2_state']=D_T.apply(f2,args=('temp_cel','pressure'), axis=1)
	D_T['co2_den_climate']=D_T.apply(f1,args=('temp_cel_climate','pressure'), axis=1)
	D_T['co2_state_climate']=D_T.apply(f2,args=('temp_cel_climate','pressure'), axis=1)
	D_T['co2_den_min']=D_T.apply(f1,args=('temp_min','pressure'), axis=1)
	D_T['co2_state_min']=D_T.apply(f2,args=('temp_min','pressure'), axis=1)
	D_T['co2_den_max']=D_T.apply(f1,args=('temp_max','pressure'), axis=1)
	D_T['co2_state_max']=D_T.apply(f2,args=('temp_max','pressure'), axis=1)

	D_T.to_csv(co2_results+'/'+user_job+'/vertical_temperature_depth_state.csv')
	#print(D_T.describe())
	return D_T



def intersecting_points_bounding_vertical(grad_sur,spoly,min_vert_depth,max_vert_depth,land_sur_correct,user_job):
	geometry=[Point(xy) for xy in zip(grad_sur.Lon, grad_sur.Lat)]
	grad_sur.drop(['Lon', 'Lat'], axis=1)
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	grad_sur = gpd.GeoDataFrame(grad_sur, crs=crs, geometry=geometry)
	pointsinPolys_intersects=sjoin(grad_sur,spoly,how="left")
	grouped = pointsinPolys_intersects.groupby('index_right')
	grouped=grouped.apply(lambda x: x.reset_index(drop = True))
	grouped=grouped.dropna(axis=0)
	grouped=grouped.set_index(grouped.columns[0]).reset_index()
	#print(grouped.head(20))
	lw=int(min_vert_depth)
	up=int(max_vert_depth)
	pw=(1+(42745*0.695e-6))*1000 #kg/m3
	D_T=pd.DataFrame({'Depth':np.arange(lw,up,1)*-1,
	'pressure':np.arange(lw,up,1)*pw*9.81,
	'temp_cel_climate':(np.arange(lw,up,1)*(grouped.Grad.median()/1000))+grouped.TempSur_c.median()+int(land_sur_correct),
	'temp_cel':(np.arange(lw,up,1)*(grouped.Grad.median()/1000))+grouped.TempSur_c.median(),
	'temp_min':(np.arange(lw,up,1)*(grouped.Grad.min()/1000))+grouped.TempSur_c.median(), #uses the median surface temperature
	'temp_max':(np.arange(lw,up,1)*(grouped.Grad.max()/1000))+grouped.TempSur_c.median(),
	'Grad':grouped.Grad.median(),
	'Sur':grouped.TempSur_c.median()})

	D_T['co2_den']=D_T.apply(f1,args=('temp_cel','pressure'), axis=1)
	D_T['co2_state']=D_T.apply(f2,args=('temp_cel','pressure'), axis=1)
	D_T['co2_den_climate']=D_T.apply(f1,args=('temp_cel_climate','pressure'), axis=1)
	D_T['co2_state_climate']=D_T.apply(f2,args=('temp_cel_climate','pressure'), axis=1)
	D_T['co2_den_min']=D_T.apply(f1,args=('temp_min','pressure'), axis=1)
	D_T['co2_state_min']=D_T.apply(f2,args=('temp_min','pressure'), axis=1)
	D_T['co2_den_max']=D_T.apply(f1,args=('temp_max','pressure'), axis=1)
	D_T['co2_state_max']=D_T.apply(f2,args=('temp_max','pressure'), axis=1)

	D_T.to_csv(co2_results+'/'+user_job+'/vertical_temperature_depth_custom.csv')
	#print(D_T.describe())
	return D_T

def intersecting_points_county_vertical(grad_sur,sub_explo,min_vert_depth,max_vert_depth,land_sur_correct,user_job):
	geometry=[Point(xy) for xy in zip(grad_sur.Lon, grad_sur.Lat)]
	grad_sur.drop(['Lon', 'Lat','pressure','CO2_dense','temp_at_f','CO2_phase'], axis=1)
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	grad_sur = gpd.GeoDataFrame(grad_sur, crs=crs, geometry=geometry)
	pointsinPolys_intersects=sjoin(grad_sur,sub_explo,how="left")
	grouped = pointsinPolys_intersects.groupby('index_right')
	grouped=grouped.apply(lambda x: x.reset_index(drop = True))
	grouped=grouped.dropna(axis=0)
	grouped=grouped.set_index(grouped.columns[0]).reset_index()
	#print(grouped.head(15))
	lw=int(min_vert_depth)
	up=int(max_vert_depth)
	pw=(1+(42745*0.695e-6))*1000 #kg/m3
	D_T=pd.DataFrame({'Depth':np.arange(lw,up,1)*-1,
	'pressure':np.arange(lw,up,1)*pw*9.81,
	'temp_cel_climate':(np.arange(lw,up,1)*(grouped.Grad.median()/1000))+grouped.TempSur_c.median()+int(land_sur_correct),
	'temp_cel':(np.arange(lw,up,1)*(grouped.Grad.median()/1000))+grouped.TempSur_c.median(),
	'temp_min':(np.arange(lw,up,1)*(grouped.Grad.min()/1000))+grouped.TempSur_c.median(),
	'temp_max':(np.arange(lw,up,1)*(grouped.Grad.max()/1000))+grouped.TempSur_c.median(),
	'Grad':grouped.Grad.median(),
	'Sur':grouped.TempSur_c.median()})
	#print('D_T')
	#print(D_T.head(15))

	
	#print(D_T.apply(f1,args=('temp_cel','pressure'), axis=1))
	D_T['co2_den']=D_T.apply(f1,args=('temp_cel','pressure'), axis=1)
	D_T['co2_state']=D_T.apply(f2,args=('temp_cel','pressure'), axis=1)
	D_T['co2_den_climate']=D_T.apply(f1,args=('temp_cel_climate','pressure'), axis=1)
	D_T['co2_state_climate']=D_T.apply(f2,args=('temp_cel_climate','pressure'), axis=1)
	D_T['co2_den_min']=D_T.apply(f1,args=('temp_min','pressure'), axis=1)
	D_T['co2_state_min']=D_T.apply(f2,args=('temp_min','pressure'), axis=1)
	D_T['co2_den_max']=D_T.apply(f1,args=('temp_max','pressure'), axis=1)
	D_T['co2_state_max']=D_T.apply(f2,args=('temp_max','pressure'), axis=1)

	D_T.to_csv(co2_results+'/'+user_job+'/vertical_temperature_depth_county.csv')
	#print(D_T.describe())
	return D_T



def main(grad, sur, co2_profile, co2_depth,min_vert_depth,max_vert_depth,land_sur_correct,co2_US_state,co2_US_county,co2_lon_lat,area,climate,user_job,session,result):
    os.mkdir(co2_results+'/'+user_job)
    with open(co2_results+'/'+user_job+'/session_parameters.txt', 'w') as f:
    	print((session,result), file=f)
    if type(co2_depth)==str:
    	co2_depth=int(co2_depth)
    if min_vert_depth==0:
    	min_vert_depth==1
    grad_sur_a=merge_data(grad, sur)
    grad_sur=grad_sur_calcs(grad_sur_a,co2_depth,land_sur_correct)
    if co2_profile =='Horizontal':
    	if area=='All US':
    		sub_explo=read_shape_all_US()
    		intersecting_points_all_US(grad_sur,sub_explo,co2_depth,user_job)
    	if area=='US state':
    		sub_explo=read_shape_state(co2_US_state)
    		intersecting_points_state(grad_sur,sub_explo,co2_US_state,co2_depth,user_job)
    	if area=='US county':
    		sub_explo=read_shape_county(co2_US_county,co2_US_state)
    		intersecting_points_county(grad_sur,sub_explo,co2_US_county,co2_depth,user_job)
    	if area=='Custom mapping':
    		spoly=bounding_box(co2_lon_lat)
    		intersecting_points_custom(grad_sur,spoly,co2_depth,user_job)
    elif co2_profile =='Vertical':
    	if area=='US state':
    		sub_explo=read_shape_state(co2_US_state)
    		D_T=intersecting_points_state_vertical(grad_sur,sub_explo,min_vert_depth,max_vert_depth,land_sur_correct,user_job)
    		ploting_vertical_co2.main(D_T,user_job,climate,land_sur_correct)
    	if area=='US county':
    		sub_explo=read_shape_county(co2_US_county,co2_US_state)
    		D_T=intersecting_points_county_vertical(grad_sur,sub_explo,min_vert_depth,max_vert_depth,land_sur_correct,user_job)
    		ploting_vertical_co2.main(D_T,user_job,climate,land_sur_correct)
    	if area=='Custom mapping':
    		spoly=bounding_box(co2_lon_lat)
    		D_T=intersecting_points_bounding_vertical(grad_sur,spoly,min_vert_depth,max_vert_depth,land_sur_correct,user_job)
    		ploting_vertical_co2.main(D_T,user_job,climate,land_sur_correct)
    pipe = subprocess.run([directory+'aws_sync_co2_results.sh',str(output_data), str('./co2_results/'+user_job),str(user_job)])

	#vertical_profile(grad_sur)

if __name__ == '__main__':
	main()
