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

directory='/Users/hamish/github/co2_gasp'
us_land='/Users/hamish/github/co2_gasp/INPUT_DATA/SHAPE_DATA/USA_adm'
co2_results='/Users/hamish/github/co2_gasp/co2_results'



def merge_data(grad, sur):
	grad_sur=grad.merge(sur,on=['Lat','Lon'])
	return grad_sur

def grad_sur_calcs(grad_sur):
	grad_sur['TempSur_c']=grad_sur['TempSur_celsius']
	grad_sur['temp_at_f']=(grad_sur['TempSur_c']+grad_sur['Grad']*(co2_depth[0]/1000))+273.15
	pw=(1+(42745*0.695e-6))*1000 #kg/m3
	grad_sur['pressure']=pw*9.81*co2_depth[0]  #kg/m-1 s-2
	grad_sur['CO2_dense']=grad_sur.apply(f1, axis=1)
	grad_sur['CO2_phase']=grad_sur.apply(f2, axis=1)
	return grad_sur

def f1(x):
	return CP.PropsSI('D', 'T', x['temp_at_f'], 'P', x['pressure'], 'CO2')

def f2(x):
	return CP.PropsSI('Phase', 'T', x['temp_at_f'], 'P', x['pressure'], 'CO2')

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
	exploded=boundary_us.explode()
	box=[(-128.600464,24.374619),(-128.600464,50.406767),(-60.748901,50.406767),(-60.748901,24.374619)]
	poly = Polygon(box)
	spoly = gpd.GeoSeries([poly],crs=crs)
	xmin, ymin, xmax, ymax = spoly.total_bounds
	#sub_explo=country_boundary_us.cx[xmin:xmax,ymin:ymax]
	sub_explo=exploded.cx[xmin:xmax,ymin:ymax]
	print(sub_explo.head())
	sub_explo=sub_explo.reset_index().drop(['ID_0' , 'ISO'   , 'NAME_0'  ],axis=1)
	print('sub explo read')
	return sub_explo

def intersecting_points_all_US(grad_sur,sub_explo):
	geometry=[Point(xy) for xy in zip(grad_sur.Lon, grad_sur.Lat)]
	grad_sur.drop(['Lon', 'Lat'], axis=1)
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	grad_sur = gpd.GeoDataFrame(grad_sur, crs=crs, geometry=geometry)
	pointsinPolys_intersects=sjoin(grad_sur,sub_explo,how="left")
	grouped = pointsinPolys_intersects.groupby('index_right')
	grouped=grouped.apply(lambda x: x.reset_index(drop = True))
	grouped=grouped.dropna(axis=0)
	grouped=grouped.set_index(grouped.columns[0]).reset_index()
	print(grouped.head(10))
	grouped.to_file(driver='ESRI Shapefile', filename=co2_results+'/temperature_depth_%i_all_US_%s.shp'%(co2_depth[0],co2_US_state[0]))
	pipe = subprocess.run([directory+'/gdal_command_1.sh',str(co2_depth[0]),co2_US_state[0]])
	print('gdal command run')
	print(grouped.head())
	grouped.to_csv(co2_results+'/temperature_depth_%i_all_US_%s.csv'%(co2_depth[0],co2_US_state[0]))
	return grouped


def read_shape_state():
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	state_boundary_us = gpd.read_file(us_land+'/USA_adm1.shp',crs=crs)
	print(state_boundary_us)
	exploded=state_boundary_us.loc[state_boundary_us['NAME_1']==co2_US_state[0]].explode()
	box=[(-128.600464,24.374619),(-128.600464,50.406767),(-60.748901,50.406767),(-60.748901,24.374619)]
	poly = Polygon(box)
	spoly = gpd.GeoSeries([poly],crs=crs)
	xmin, ymin, xmax, ymax = spoly.total_bounds
	#sub_explo=country_boundary_us.cx[xmin:xmax,ymin:ymax]
	sub_explo=exploded.cx[xmin:xmax,ymin:ymax]
	print(sub_explo.head())
	sub_explo=sub_explo.reset_index().drop(['ID_0' , 'ISO'   , 'NAME_0' , 'ID_1' ,'NAME_1' ,'TYPE_1', 'ENGTYPE_1' ,'NL_NAME_1', 'VARNAME_1' ],axis=1)
	print('sub explo read')
	return sub_explo

#def temp_at_form(grad_sur):
#	D_T=pd.DataFrame({'Depth':-np.arange(0,10000,1),'temp_cel_climate':(np.arange(0,10000,1)*(nesson.Grad.mean()/1000))+(nesson.TempSur_celsius.mean()+land_sur_correct[0]),	'temp_cel':(np.arange(0,10000,1)*(nesson.Grad.mean()/1000))+nesson.TempSur_celsius.mean(),'temp_min':(np.arange(0,10000,1)*(nesson.Grad.min()/1000))+nesson.TempSur_celsius.mean(),'temp_max':(np.arange(0,10000,1)*(nesson.Grad.max()/1000))+nesson.TempSur_celsius.mean()})


def intersecting_points_state(grad_sur,sub_explo):
	geometry=[Point(xy) for xy in zip(grad_sur.Lon, grad_sur.Lat)]
	grad_sur.drop(['Lon', 'Lat'], axis=1)
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	grad_sur = gpd.GeoDataFrame(grad_sur, crs=crs, geometry=geometry)
	pointsinPolys_intersects=sjoin(grad_sur,sub_explo,how="left")
	grouped = pointsinPolys_intersects.groupby('index_right')
	grouped=grouped.apply(lambda x: x.reset_index(drop = True))
	grouped=grouped.dropna(axis=0)
	grouped=grouped.set_index(grouped.columns[0]).reset_index()
	print(grouped.head(10))
	grouped.to_file(driver='ESRI Shapefile', filename=co2_results+'/temperature_depth_%i_state_%s.shp'%(co2_depth[0],co2_US_state[0]))
	pipe = subprocess.run([directory+'/gdal_command_2.sh',str(co2_depth[0]),co2_US_state[0]])
	print('gdal command run')
	print(grouped.head())
	grouped.to_csv(co2_results+'/temperature_depth_%i_state_%s.csv'%(co2_depth[0],co2_US_state[0]))
	return grouped


def read_shape_county():
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	county_boundary_us = gpd.read_file(us_land+'/USA_adm2.shp',crs=crs)
	print(county_boundary_us)
	exploded=county_boundary_us.loc[(county_boundary_us['NAME_2'].isin(co2_US_county))&(county_boundary_us['NAME_1'].isin(co2_US_state))].explode()
	box=[(-128.600464,24.374619),(-128.600464,50.406767),(-60.748901,50.406767),(-60.748901,24.374619)]
	poly = Polygon(box)
	spoly = gpd.GeoSeries([poly],crs=crs)
	xmin, ymin, xmax, ymax = spoly.total_bounds
	#sub_explo=country_boundary_us.cx[xmin:xmax,ymin:ymax]
	sub_explo=exploded.cx[xmin:xmax,ymin:ymax]
	print(sub_explo.head())
	sub_explo=sub_explo.reset_index().drop(['ID_0' , 'ISO'   , 'NAME_0' , 'ID_1' ,'NAME_1' ,'ID_2', 'NAME_2',  'TYPE_2', 'ENGTYPE_2', 'NL_NAME_2', 'VARNAME_2' ],axis=1)
	print('sub explo read')
	return sub_explo


def intersecting_points_county(grad_sur,sub_explo):
	geometry=[Point(xy) for xy in zip(grad_sur.Lon, grad_sur.Lat)]
	grad_sur.drop(['Lon', 'Lat'], axis=1)
	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	grad_sur = gpd.GeoDataFrame(grad_sur, crs=crs, geometry=geometry)
	pointsinPolys_intersects=sjoin(grad_sur,sub_explo,how="left")
	grouped = pointsinPolys_intersects.groupby('index_right')
	grouped=grouped.apply(lambda x: x.reset_index(drop = True))
	grouped=grouped.dropna(axis=0)
	grouped=grouped.set_index(grouped.columns[0]).reset_index()
	print(grouped.head(10))
	grouped.to_file(driver='ESRI Shapefile', filename=co2_results+'/temperature_depth_%i_county_%s.shp'%(co2_depth[0],co2_US_county[0]))
	pipe = subprocess.run([directory+'/gdal_command_3.sh',str(co2_depth[0]),co2_US_county[0]])
	print('gdal command run')
	print(grouped.head())
	grouped.to_csv(co2_results+'/temperature_depth_%i_county_%s.csv'%(co2_depth[0],co2_US_county[0]))
	return grouped



def data_CO2_density(grad, sur):
	at_form=grad.merge(sur,on=['Lat','Lon'])
	at_form['tmp']=1
	#depth=pd.DataFrame({'D':[100,200,300,400,500,600,700,800,900,1000,1250,1500,1750,2000,2250,2500,2750,3000,3500,4000,4500,5000,5500,6000,6500,7000]})
	depth=pd.DataFrame({'D':[5000]})

	depth['tmp']=1
	cross_df=pd.merge(at_form,depth,on=['tmp']) #how=cross
	pw=(1+(42745*0.695e-6))*1000 #kg/m3
	cross_df['P']=pw*9.81*cross_df['D']  #kg/m-1 s-2
	print(cross_df['P'])
	cross_df['T']= (((cross_df.D) * (cross_df.Grad/1000)) + cross_df.TempSur_celsius)+273.15
	#cross_df['co2_den']=PropsSI('D', 'T', 298.15, 'P', 100e5, 'CO2')
	def f1(x):
		return CP.PropsSI('D', 'T', x['T'], 'P', x['P'], 'CO2')
	cross_df['co2_den']=cross_df.apply(f1, axis=1)
	def f2(x):
		return CP.PropsSI('Phase', 'T', x['T'], 'P', x['P'], 'CO2')
	cross_df['co2_state']=cross_df.apply(f2, axis=1)


	crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
	geometry_interp=[Point(xy) for xy in zip(cross_df.Lon, cross_df.Lat)]
	cross_df_gpd = gpd.GeoDataFrame(cross_df, crs=crs, geometry=geometry_interp)
	cross_df_gpd.to_file(driver='ESRI Shapefile', filename='/Users/hamish/Desktop/temperature/cross_df_gpd_5000.shp')
	return cross_df

def main(grad, sur):
	grad_sur=merge_data(grad, sur)
	grad_sur=grad_sur_calcs(grad_sur)
	if co2_all_US_mapping==True:
		sub_explo=read_shape_all_US()
		intersecting_points_all_US(grad_sur,sub_explo)
	if co2_state_mapping==True:
		sub_explo=read_shape_state()
		intersecting_points_state(grad_sur,sub_explo)
	if co2_county_mapping==True:
		sub_explo=read_shape_county()
		intersecting_points_county(grad_sur,sub_explo)

	#vertical_profile(grad_sur)

if __name__ == '__main__':
	main()
