import os
import numpy as np
import pandas as pd

data='/Users/hamish/github/co2_gasp/INPUT_DATA'

def read_in_data():
    """ Read in different datafiles
    1 - USGS PRODUCED WATER
    2- Geothermal gradient from SMUH
    Land surface temperatures read in seperate script
     """
    rawusgs = pd.read_csv(data+'/USGS_Produced_Waters_v2',sep='\t')
    geo=pd.read_csv(data+'/core.template_heatflow_materialized.csv',sep=',')
    print(rawusgs.head())
    return rawusgs, geo

def run_geeothermal_interpolate(geo,choice):
    """ Program interpolates the SMUH geothermal gradient
    By default choice == False """
    if choice == True:
        grad=geotherm_interpolate.main(geo)
    if choice == False:
        grad=pd.read_csv(data+'filename')
    return grad

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

def main():
    rawusgs,geo =read_in_data()

if __name__ == "__main__":
	main()
