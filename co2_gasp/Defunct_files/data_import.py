import os
import numpy as np
import pandas as pd
import geotherm_interpolate
import data_processing_1
from co2_gasp_run_options import *     #import the option file from within the same folder
import ModisData

data='/Users/hamish/github/co2_gasp/INPUT_DATA'
directory='/Users/hamish/github/co2_gasp'
geotherm_result = '/Users/hamish/github/co2_gasp/INPUT_DATA/geothermal_result_files'
MODIS_results = '/Users/hamish/github/co2_gasp/INPUT_DATA/MODIS_result_files'


def read_in_data():
    """ Read in different datafiles
    1 - USGS PRODUCED WATER
    2- Geothermal gradient from SMUH
    Land surface temperatures read in seperate script
     """
    rawusgs = pd.read_csv(data+'/USGS_Produced_Waters_v2',sep='\t')
    geo=pd.read_csv(data+'/core.template_heatflow_materialized.csv',sep=',')
    print(geo.head())
    return rawusgs, geo

def run_geeothermal_interpolate(geo):
    """ Program interpolates the SMUH geothermal gradient
    By default choice == False """
    if geo_interp_T_F == True:
        grad=geotherm_interpolate.main(geo)
    if geo_interp_T_F == False:
        grad=pd.read_csv(geotherm_result+'/geotherm_grad_grouped_1dp_no_filter.csv')
        grad=grad.drop([grad.columns[0],'index_right','geometry'],axis=1)
        grad=grad.round({'Lat':1,'Lon':1})  #This is just formatting the csv correctly, for some reason wasn't happy
        grad=grad.round({'Grad':1})
    return grad

#def data_processing(rawusgs):

def MODIS_data_import():
    if MODIS_process_T_F == True:
        sur=ModisData.main()
        print(sur.head(5))
    if MODIS_process_T_F == False:
        sur=pd.read_csv(MODIS_results+'/merged_data_2')
        sur=sur.drop_duplicates(subset=['Lat','Lon'],keep='first')
        print(sur.head(5))
    sur["TempSur_celsius"] = sur["TempSur"] - 273.15
    sur=sur.round({'TempSur_celsius':0})
    #print( 'lat n lon = ',sur[(sur.Lat == 41.1) & (sur.Lon == -79.7)])  # this one is fine
    return sur





def main():
    rawusgs,geo =read_in_data()
    grad=run_geeothermal_interpolate(geo)
    #data_processing(rawusgs)
    sur=MODIS_data_import()
    return rawusgs, grad, sur
if __name__ == "__main__":
	main()
