import os
import numpy as np
import pandas as pd
import geotherm_interpolate
import data_processing_1
import data_import_2
from co2_gasp_run_options import *     #import the option file from within the same folder
import ModisData
import boto3
import sys

from file_paths import s3_data,s3_geotherm_result, s3_MODIS_results, s3_geochem_result, output_data


def boto3_download_results(file):
    url=boto3.client('s3').generate_presigned_url(
    ClientMethod='get_object',
    Params={'Bucket': 'co-2-gasp-bucket', 'Key': file},
    ExpiresIn=3600)
    print(url)
    return url


def read_in_data():
    """ Read in different datafiles
    1 - USGS PRODUCED WATER
    2- Geothermal gradient from SMUH
    Land surface temperatures read in seperate script
     """
    #rawusgs = pd.read_csv(boto3_file_read(data+'/USGS_Produced_Waters_v2'),sep='\t')
    rawusgs = pd.read_csv(s3_data+'/USGS_Produced_Waters_v2',sep='\t')
    geo=pd.read_csv(s3_data+'/core.template_heatflow_materialized.csv',sep=',')
    return rawusgs, geo

def run_geothermal_interpolate(geo):
    """ Program interpolates the SMUH geothermal gradient
    By default choice == False """
    if geo_interp_T_F == True:
        grad=geotherm_interpolate.main(geo)
    if geo_interp_T_F == False:
        grad=pd.read_csv(s3_geotherm_result+'/geotherm_grad_grouped_1dp_no_filter.csv')
        grad=grad.drop([grad.columns[0],'index_right','geometry'],axis=1)
        grad=grad.round({'Lat':1,'Lon':1})  #This is just formatting the csv correctly, for some reason wasn't happy
        grad=grad.round({'Grad':1})
    return grad

#def data_processing(rawusgs):

def MODIS_data_import():
    if MODIS_process_T_F == True:
        sur=ModisData.main()
        #print(sur.head(5))
    if MODIS_process_T_F == False:
        sur=pd.read_csv(s3_MODIS_results+'/merged_data_2')
        sur=sur.drop_duplicates(subset=['Lat','Lon'],keep='first')
        #print(sur.head(5))
    sur["TempSur_celsius"] = sur["TempSur"] - 273.15
    sur=sur.round({'TempSur_celsius':0})
    #print( 'lat n lon = ',sur[(sur.Lat == 41.1) & (sur.Lon == -79.7)])  # this one is fine
    return sur

def medusgs_data_import(rawusgs,grad,sur):
    if Merge_usgs_grad_T_F == True:
        medusgs=data_import_2.main(rawusgs,grad,sur)
    if Merge_usgs_grad_T_F == False:
        medusgs=pd.read_csv(s3_geochem_result+'/merged_data_all_samples')
        #print(len(medusgs))
        mgca_count=medusgs.groupby(['Lat', 'Lon']).size().reset_index(name='counts')
        mgca_count.to_csv(output_data+'/mgca_count_all_samples.txt')
        #print(medusgs.head(5))
    return medusgs




def main():
    rawusgs,geo =read_in_data()
    grad=run_geothermal_interpolate(geo)
    #data_processing(rawusgs)
    sur=MODIS_data_import()
    medusgs=medusgs_data_import(rawusgs,grad,sur)
    return rawusgs, grad, sur, medusgs

if __name__ == "__main__":
	main()
