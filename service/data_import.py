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


data='INPUT_DATA'
#directory='/Users/hamish/github/co2_gasp'
geotherm_result = 'INPUT_DATA/geothermal_result_files'
MODIS_results = 'INPUT_DATA/MODIS_result_files'
geochem_result = 'INPUT_DATA/geochemical_result_files'

#this method is now mostly defunct....probably...can use S3 like local filesystem....mostly....
def boto3_file_read(file):
    print(file)
    s3_client = boto3.client('s3')
    response=s3_client.get_object(Bucket='co-2-gasp-bucket',Key=file)
    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    if status == 200:
        return response.get('Body')
    else:
       print ('Error retrieving file:',file)

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
    rawusgs = pd.read_csv('s3://co-2-gasp-bucket/'+data+'/USGS_Produced_Waters_v2',sep='\t')
    geo=pd.read_csv('s3://co-2-gasp-bucket/'+data+'/core.template_heatflow_materialized.csv',sep=',')
    return rawusgs, geo

def run_geothermal_interpolate(geo):
    """ Program interpolates the SMUH geothermal gradient
    By default choice == False """
    if geo_interp_T_F == True:
        grad=geotherm_interpolate.main(geo)
    if geo_interp_T_F == False:
        grad=pd.read_csv('s3://co-2-gasp-bucket/'+geotherm_result+'/geotherm_grad_grouped_1dp_no_filter.csv')
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
        sur=pd.read_csv('s3://co-2-gasp-bucket/'+MODIS_results+'/merged_data_2')
        sur=sur.drop_duplicates(subset=['Lat','Lon'],keep='first')
        print(sur.head(5))
    sur["TempSur_celsius"] = sur["TempSur"] - 273.15
    sur=sur.round({'TempSur_celsius':0})
    #print( 'lat n lon = ',sur[(sur.Lat == 41.1) & (sur.Lon == -79.7)])  # this one is fine
    return sur

def medusgs_data_import(rawusgs,grad,sur):
    if Merge_usgs_grad_T_F == True:
        medusgs=data_import_2.main(rawusgs,grad,sur)
    if Merge_usgs_grad_T_F == False:
        medusgs=pd.read_csv('s3://co-2-gasp-bucket/'+geochem_result+'/merged_data')
        print(medusgs.head(5))
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
