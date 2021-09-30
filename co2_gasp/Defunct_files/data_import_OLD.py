import os
import numpy as np

import functools
import pandas as pd
pd.options.display.max_rows = 4000
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import sys
import ModisData
import geotherm_interpolate
import CoolProp.CoolProp as CP

from scipy.interpolate import griddata
from shapely.geometry import Point
from shapely.geometry import Polygon
import geopandas as gpd
from geopandas.tools import sjoin


data='/Users/hamish/Documents/AWSprojects/data'
temp='/Users/hamish/Documents/AWSprojects/temp'
bin='/Users/hamish/Documents/AWSprojects/bin'
fig='/Users/hamish/Documents/AWSprojects/fig'

#This could be the first script that does all the filtering of files.
#This can essentially be optionally run.
#This output file is whats read back in by the user in the next script.
#The next script - main? Handles all phreeqc work and running stuff.
# i.e subdivide the scripts into a nice series of seperate testable scripts
#Also helps emotionally as you actually see stuff growing and can break.


#Update 1 - 30/12- This file shows concordent results up to 'create a subset
# of the data for p[arsing to phreeq input file'


### Data Filtering ####
#Goal of data filtering is to return a static csv file containing the post-filtered data
#for use in the pandas-lookup and PHREEQC calculations.
# Turn this into an Arc-Gis python toolkit - or not.


def read_in_data():
	"""Read in raw data from various sources
	rawusgs - raw produced water database
	grad_old - geothermal gradient interpolated in QGIS from smu - old methodology
	grad - completely integrated python interpolation
	sur - surface temperatrues from MODIS
	"""
	rawusgs = pd.read_csv(data+'/USGS_Produced_Waters_v2',sep='\t')
	#    geo=pd.read_csv(data+'/core.template_heatflow_materialized.csv',sep=',') - old version
	#grad_old=pd.read_csv(data+'/geothermgrad.xyz',sep=',',header=None,names=['Lon','Lat','Gradient']) # -newest 'old version', fully integrated interpolated script now
	#print(grad_old.head())
	grad=geotherm_interpolate.main()
	#print(grad.head())

	#sur=pd.read_csv(data+'/merged_data_2_land_surface_temperature.txt',sep=',',header=0,names=['Lat','Lon','TempSur'],float_precision='round_trip') #old i think
	sur=ModisData.main()

	#rawgradients=pd.read_csv(data+'/gradients',sep='\t')
	print('rawusgs=', len(rawusgs), 'grad=',len(grad), 'sur='  , len(sur))
	print ('data imported')
	return rawusgs, grad, sur
	#rawgradients


def data_processing1(rawusgs):
	"""Create a mean of the depth between the upper and lower peforations (ingnoring NaN
	values). Concert to km. Append to database. Rename columns. Make a permant copy to new
	dataframe USGS
	incoming - rawusgs
	outgoing - formated USGS
	"""
	rawusgs['Depth']=rawusgs[['DEPTHUPPER', 'DEPTHLOWER']].mean(axis=1)
	rawusgs.Depth = rawusgs.Depth * 0.0003048 # Convert ft to km (km in smuh database)
	rawusgs = rawusgs.rename(columns={'LATITUDE': 'Lat', 'LONGITUDE': 'Lon'})
	rawusgs['Lat_OLD']=rawusgs['Lat']
	rawusgs['Lon_OLD']=rawusgs['Lon']
	usgs=rawusgs.copy()
	print('usgs=',len(usgs))
	return usgs

def data_processing2(usgs):
	""" Filter the USGS database to a set of geochemical quality control parameters defined
	in the text document. USER - THIS IS WHERE YOU EDIT FILTERING CRITERIA!
	The data is also rounded to the nearest 0.1 lat/lon
	incoming-usgs
	outgoing-usgs1
	"""
	#Cull breakdown for stats
	print('len of original usgs datafram',len(usgs))
	ph=usgs[(usgs.PH >= 3.5 ) & (usgs.PH <= 11 )]
	print('pH fail',100-((len(ph)/len(usgs))*100))
	chargebalance=usgs[(usgs.chargebalance >= -15.0 ) & (usgs.chargebalance <= 15.0 )]
	print('chargebalance',100-((len(chargebalance)/len(usgs))*100))
	mg=usgs[(usgs.Mg > 0.0 ) & (usgs.Ca > 0.0 )]
	print('mg fail',100-((len(mg)/len(usgs))*100))
	depth=usgs[(usgs.Depth > 0.0)]
	print('depth fail',100-((len(depth)/len(usgs))*100))
	lat=usgs[(usgs.Lat > 0.0) & (usgs.Lon < 0.0)]
	print('lat fail',100-((len(lat)/len(usgs))*100))
	lith=usgs.loc[~(pd.isnull(usgs.LITHOLOGY))] #not ~ null lithology
	lith = lith[lith.LITHOLOGY != 'Anhydrite']                    #CULLED
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
	lith = lith[lith.LITHOLOGY != 'Chat']                         #CULLED
	lith = lith[lith.LITHOLOGY != 'Chert']                         #CULLED
	lith.loc[lith.LITHOLOGY == 'Chert, Dolomite','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Chert, Dolomite, Limestone','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Chert, Dolomite, Limestone, Sandstone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	lith.loc[lith.LITHOLOGY == 'Chert, Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Chert, Dolomite, Sandstone, Shale','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Chert, Dolomite, Shale','LITHOLOGY'] = 'Dolomite'
	lith.loc[lith.LITHOLOGY == 'Chert, Limestone','LITHOLOGY'] = 'Limestone'
	lith.loc[lith.LITHOLOGY == 'Chert, Sandstone','LITHOLOGY'] = 'Sandstone'
	lith = lith[lith.LITHOLOGY != 'Coal']                         #CULLED
	lith = lith[lith.LITHOLOGY != 'Conglomerate']                 #CULLED
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
	lith = lith[lith.LITHOLOGY != 'Ga1g']                         #CULLED
	lith = lith[lith.LITHOLOGY != 'Ga1n']                         #CULLED
	lith = lith[lith.LITHOLOGY != 'Ga1r']                         #CULLED
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
	lith = lith[lith.LITHOLOGY != 'Other']                        #CULLED
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
	lith = lith[lith.LITHOLOGY != 'Unknown']
	print('lith fail',100-((len(lith)/len(usgs))*100))

	#Sequential cull
	print('usgs=',len(usgs))
	usgs=usgs[(usgs.PH >= 3.5 ) & (usgs.PH <= 11 )]
	print('usgs ph=',len(usgs))
	usgs=usgs[(usgs.chargebalance >= -15.0 ) & (usgs.chargebalance <= 15.0 )]
	print('usgs chargebalance=',len(usgs))
	usgs=usgs[(usgs.Mg > 0.0 ) & (usgs.Ca > 0.0 )]
	print('usgs non-zero Mg Ca=',len(usgs))
	usgs=usgs[(usgs.Depth > 0.0)]
	print('usgs depth=',len(usgs))
	usgs=usgs[(usgs.Lat > 0.0) & (usgs.Lon < 0.0)]
	print('usgs lat-lon=',len(usgs))
	usgs=usgs.loc[~(pd.isnull(usgs.LITHOLOGY))] #not ~ null lithology
	print('usgs lithology=',len(usgs))
	usgs=usgs.round({'Lat':1,'Lon':1})
	print("percent remaining", len(usgs), 1 - len(usgs)/165960 )
	usgs1=usgs.copy()
	print('usgs1=',len(usgs1))

	return usgs1

def data_processing3(usgs1,usgs):
	""" Cull and modify lithology labels into  more organised, generalized groupds
	according the criteria listed bellow.
	This is the last stage in the USGS processing.
	incoming usgs1
	outgoing usgs2
	"""
	print('usgs1=',len(usgs1))
	usgs1 = usgs1[usgs1.LITHOLOGY != 'Anhydrite']                    #CULLED
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite and dolomite','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Chert, Dolomite, Other','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Chert, Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Dolomite','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Dolomite, Limestone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Dolomite, Limestone, Sandstone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Dolomite, Limestone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Dolomite, Sandstone, Shale','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Dolomite, Shale','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Dolomite, Siltstone','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Sandstone','LITHOLOGY'] = 'Sandstone'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Sandstone, Shale','LITHOLOGY'] = 'Sandstone'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Sandstone, Siltstone','LITHOLOGY'] = 'Sandstone'
	usgs1.loc[usgs1.LITHOLOGY == 'Anhydrite, Shale','LITHOLOGY'] = 'Shale'
	usgs1.loc[usgs1.LITHOLOGY == 'Carbonate','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Carbonate, Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Carbonate, Sandstone, Shale, Siltstone, Other','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Chalk','LITHOLOGY'] = 'Limestone'
	usgs1 = usgs1[usgs1.LITHOLOGY != 'Chat']                         #CULLED
	usgs1 = usgs1[usgs1.LITHOLOGY != 'Chert']                         #CULLED
	usgs1.loc[usgs1.LITHOLOGY == 'Chert, Dolomite','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Chert, Dolomite, Limestone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Chert, Dolomite, Limestone, Sandstone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Chert, Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Chert, Dolomite, Sandstone, Shale','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Chert, Dolomite, Shale','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Chert, Limestone','LITHOLOGY'] = 'Limestone'
	usgs1.loc[usgs1.LITHOLOGY == 'Chert, Sandstone','LITHOLOGY'] = 'Sandstone'
	usgs1 = usgs1[usgs1.LITHOLOGY != 'Coal']                         #CULLED
	usgs1 = usgs1[usgs1.LITHOLOGY != 'Conglomerate']                 #CULLED
	usgs1.loc[usgs1.LITHOLOGY == 'Dolomite & Lime','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Dolomite - Lime','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Dolomite, Limestone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Dolomite, Limestone, Sandstone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Dolomite, Limestone, Sandstone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Dolomite, Limestone, Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Dolomite, Limestone, Sandstone, Siltstone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Dolomite, Limestone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Dolomite, Sandstone, Shale','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Dolomite, Sandstone, Siltstone','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Dolomite, Shale','LITHOLOGY'] = 'Dolomite'
	usgs1.loc[usgs1.LITHOLOGY == 'Dolomite, Siltstone','LITHOLOGY'] = 'Dolomite'
	usgs1 = usgs1[usgs1.LITHOLOGY != 'Ga1g']                         #CULLED
	usgs1 = usgs1[usgs1.LITHOLOGY != 'Ga1n']                         #CULLED
	usgs1 = usgs1[usgs1.LITHOLOGY != 'Ga1r']                         #CULLED
	usgs1.loc[usgs1.LITHOLOGY == 'Limestone & Dol','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Limestone & San','LITHOLOGY'] = 'Limestone'
	usgs1.loc[usgs1.LITHOLOGY == 'Limestone & Sha','LITHOLOGY'] = 'Limestone'
	usgs1.loc[usgs1.LITHOLOGY == 'Limestone - Dol','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Limestone Dolom','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1.loc[usgs1.LITHOLOGY == 'Limestone, Sandstone','LITHOLOGY'] = 'Limestone'
	usgs1.loc[usgs1.LITHOLOGY == 'Limestone, Sandstone, Shale','LITHOLOGY'] = 'Limestone'
	usgs1.loc[usgs1.LITHOLOGY == 'Limestone, Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Limestone'
	usgs1.loc[usgs1.LITHOLOGY == 'Limestone, Sandstone, Siltstone','LITHOLOGY'] = 'Limestone'
	usgs1.loc[usgs1.LITHOLOGY == 'Limestone, Shale','LITHOLOGY'] = 'Limestone'
	usgs1.loc[usgs1.LITHOLOGY == 'Limestone; Dolostone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs1 = usgs1[usgs1.LITHOLOGY != 'Other']                        #CULLED
	usgs1.loc[usgs1.LITHOLOGY == 'Sand','LITHOLOGY'] = 'Sandstone'
	usgs1.loc[usgs1.LITHOLOGY == 'Sand Stone','LITHOLOGY'] = 'Sandstone'
	usgs1.loc[usgs1.LITHOLOGY == 'Sandstone, Other','LITHOLOGY'] = 'Sandstone'
	usgs1.loc[usgs1.LITHOLOGY == 'Sandstone, Shale','LITHOLOGY'] = 'Sandstone'
	usgs1.loc[usgs1.LITHOLOGY == 'Sandstone, Shale, Other','LITHOLOGY'] = 'Sandstone'
	usgs1.loc[usgs1.LITHOLOGY == 'Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Sandstone'
	usgs1.loc[usgs1.LITHOLOGY == 'Sandstone, Shale, Siltstone, Other','LITHOLOGY'] = 'Sandstone'
	usgs1.loc[usgs1.LITHOLOGY == 'Sandstone, Siltstone','LITHOLOGY'] = 'Sandstone'
	usgs1.loc[usgs1.LITHOLOGY == 'Sandstone, Siltstone, Other','LITHOLOGY'] = 'Sandstone'
	usgs1.loc[usgs1.LITHOLOGY == 'Shale, Other','LITHOLOGY'] = 'Shale'
	usgs1.loc[usgs1.LITHOLOGY == 'Shale, Siltstone','LITHOLOGY'] = 'Shale'
	usgs1.loc[usgs1.LITHOLOGY == 'Siltstone','LITHOLOGY'] = 'Shale'
	usgs1 = usgs1[usgs1.LITHOLOGY != 'Unknown']                      #CULLED
	usgs2=usgs1.copy()
	print('len of original usgs datafram',len(usgs))
	print('usgs2 - total cull from original dataframe',100-((len(usgs2)/len(usgs))*100))

	#print('usgs2.head',usgs2.head(5))
	#print('usgs2.tail',usgs2.tail(5))
	return usgs2

def data_processing4(grad):
	""" New geothermal gradients - this is section defunct? Rounding functions and other bits now included in the geotherm_interpolate file

	OLD - A rather gritty interpolation is performed in qgis which works i believe slightly
	better than a worse interpolation in python. By no means is the QGIS version very good but its
	probably good enough. The data is rounded to the nearest degree celscius here and averaged over 0.1
	x0.1 grid. The resulting XYZ file is quite large (~170MB)! If the SMU were to supply
	their interpolated version I would use it in a heartbeat.

	incoming geo
	outgoing usgs2
	"""
	print('grad head')
	grad=grad[grad.Grad!=0]
	grad=grad.round({'Lat':1,'Lon':1})
	grad=grad.groupby([grad.Lat,grad.Lon]).mean()

	grad=grad.round({'Grad':0})

	grad=grad.reset_index()

	return grad

def data_processing5(sur):
	"""
	I think i could move this functionality to the MODIS script

	Python based averaging of MODIS data - see methodology section
	Surface temperatures were derived through a limited reprocessing
	(see .ipynb) of the mean annual land surface temperature (MAST)
	for North America between 2003-2014 (\cite{bechtel2015new}). Data
	was averaged over a $0.1$x$0.1 \degree$ Lat/Lon resolution
	(Fig.\ref{fig:surfacetemp} ). Surface temperatures were then rounded
	from 5 decimal places to the nearest degree celsius before being
	used further in PHREEQC calculations.
	incoming sur
	outgoing sur1
	"""
	sur["TempSur_celsius"] = sur["TempSur"] - 273.15
	sur=sur.round({'TempSur_celsius':0})
	sur1=sur.copy()
	print( 'lat n lon = ',sur1[(sur1.Lat == 41.1) & (sur1.Lon == -79.7)])  # this one is fine
	print( 'lat n lon = ',sur1[(sur1.Lat == 41.0) & (sur1.Lon == -80.5)])  # this one is fine
	#print (sur.head(50))
	return sur1


def data_CO2_density(grad, sur1):
	at_form=grad.merge(sur1,on=['Lat','Lon'])
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

	#print(cross_df.head(60))
	#print(CP.PropsSI('D', 'T', 279.15, 'P', 30124, 'CO2'))
	#cross_df_100=cross_df.loc[cross_df['D']==100][['co2_den','Lat','Lon']]
	#cross_df_100.to_file(driver='ESRI Shapefile', filename=data_import.temp+'/CRASS_DF_100.shp')


def data_processing6(usgs2,sur1,grad):
	"""Merge the dataframes into a single dataframe called medusgs
	"""
	print('usgs2 = ',len(usgs2))
	medusgs=usgs2.merge(sur1,on=['Lat','Lon'])
	print('medusgs =',len(medusgs))
	medusgs=grad.merge(medusgs,on=['Lat','Lon'])
	print('medusgs with grad =',len(medusgs))
	print((len(medusgs)/len(usgs2))*100)

	print('Sandstone=',len(medusgs[medusgs.LITHOLOGY == 'Sandstone']),(len(medusgs[medusgs.LITHOLOGY == 'Sandstone'])/len(medusgs))*100)
	print('Dolomite=',len(medusgs[medusgs.LITHOLOGY == 'Dolomite']),(len(medusgs[medusgs.LITHOLOGY == 'Dolomite'])/len(medusgs))*100)
	print('Limestone=',len(medusgs[medusgs.LITHOLOGY == 'Limestone']),(len(medusgs[medusgs.LITHOLOGY == 'Limestone'])/len(medusgs))*100)
	print('Shale=',len(medusgs[medusgs.LITHOLOGY == 'Shale']),(len(medusgs[medusgs.LITHOLOGY == 'Shale'])/len(medusgs))*100)
	print('Mixed_Carbonate=',len(medusgs[medusgs.LITHOLOGY == 'Mixed_Carbonate']),(len(medusgs[medusgs.LITHOLOGY == 'Mixed_Carbonate'])/len(medusgs))*100)

	medusgs['TemperatureSMU']= (medusgs.Depth * medusgs.Grad) + medusgs.TempSur_celsius #Adding in the surface temperature correction
	print('medusgs.head',medusgs.head(5))
	print('medusgs=',len(medusgs))

	return medusgs



def main():
	rawusgs,grad,sur=read_in_data()
	usgs=data_processing1(rawusgs)
	usgs1=data_processing2(usgs)
	usgs2=data_processing3(usgs1,usgs)
	#grad=data_processing4(grad)
	sur1=data_processing5(sur)
	#co2_density=data_CO2_density(grad,sur1)
	medusgs=data_processing6(usgs2,sur1,grad)
	return medusgs

if __name__ == "__main__":
	main()

#def user_input():
#    lat=user_input
#    lon=user_input
#    formation=user_input
#
#def processing():
#    testing123
#    take user inputs
#    create graphs showing geothermal gradient vs a normal 25 degC gradient for the area
#    run phreeqc analyses on waters and return txt.out files stick them in some kind of temp folderavailible to download along with those displaying results
#    highlight the waters were determined to be of good quality through filtering and thus those considered valuable
