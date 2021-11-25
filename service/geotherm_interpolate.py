from pydap.client import open_url
import pandas as pd
import numpy as np
import data_import
import os
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from shapely.geometry import Point
from shapely.geometry import Polygon
import geopandas as gpd
from geopandas.tools import sjoin
import data_import
import subprocess

from file_paths import s3_geotherm_result,directory

##Need to upgrade geopandas to 8.1 for this part of the script to work.
"""Script run at 0.1 dp resolution 
Note have changed the INPUT_DATA/geochemical_result_files type locations (old), was data_import.geotherm_result etc, to S3 locations. Script hasnt been run yet
"""



def read_geotherm(geo):
    #read heatflow csv. IntervalCorrectedGradient is the geothermal gradient
    geo=geo[(geo.IntervalCorrectedGradient >= 0) & (geo.IntervalCorrectedGradient <= 200)]
    geo=geo.round({'LatDegreeWGS84': 1, 'LongDegreeWGS84': 1}) # round columns to 1 dp
    geo=geo.groupby([geo.LatDegreeWGS84,geo.LongDegreeWGS84]).mean()
    geo=geo.unstack()
    interp=geo.IntervalCorrectedGradient
    interp=interp.stack().reset_index()
    interp.columns=['Lat','Lon','Grad']
    interp=interp.round({'Grad': 0})
    #interp.to_csv(data+'/geotherm_gradient_locations.csv')
    print('read in geo therm')
    print(interp.head())
    return interp

def interp_gradient(interp):
    geometry_interp = [Point(xy) for xy in zip(interp.Lon, interp.Lat)]
    crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
    interp_df = gpd.GeoDataFrame(interp, crs=crs, geometry=geometry_interp)
    box=[(-128.600464,24.374619),(-128.600464,50.406767),(-60.748901,50.406767),(-60.748901,24.374619)]
    poly = Polygon(box)
    crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
    spoly = gpd.GeoSeries([poly],crs=crs)
    xmin, ymin, xmax, ymax = spoly.total_bounds
    print(interp_df.__dict__)
    sub_interp=interp_df.cx[xmin:xmax,ymin:ymax]
    #sub_interp.total_bounds=array([-124.2,   24.4,  -68.6,   49. ])
    sub_interp=sub_interp.drop_duplicates(subset=['Lat','Lon'],keep='first')
    lat_grid = np.arange(24.3,49.1,0.1)
    lon_grid = np.arange(-68.5,-124.3,-0.1) #interp area just outside of bounds of data 0.1 decimal resolution
    lon_grid, lat_grid =np.meshgrid(lon_grid ,lat_grid )
    zi=griddata((sub_interp.Lon,sub_interp.Lat),sub_interp.Grad,(lon_grid,lat_grid),method='linear')
    lat_flat=lat_grid.flatten()
    lon_flat=lon_grid.flatten()
    grad_flat=zi.flatten()
    crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
    df = pd.DataFrame({'Grad':grad_flat,'Lon':lon_flat,'Lat':lat_flat})
    geometry_interp = [Point(xy) for xy in zip(df.Lon, df.Lat)]
    interp = gpd.GeoDataFrame(df, crs=crs, geometry=geometry_interp)
    interp=interp.dropna()
    #df.to_csv('geotherm_grad_cubic_0_01_dropna.csv',index=False,float_format='%.2f')
    print('interp complete')
    print(interp.head())
    return interp

def read_shape():
    country_boundary_us = gpd.read_file(s3_geotherm_result+'/cb_2018_us_nation_5m/cb_2018_us_nation_5m.shp')
    print('read in')
    exploded=country_boundary_us.explode()
    box=[(-128.600464,24.374619),(-128.600464,50.406767),(-60.748901,50.406767),(-60.748901,24.374619)]
    poly = Polygon(box)
    crs = {'init': 'epsg:4269'} #http://www.spatialreference.org/ref/epsg/2263/
    spoly = gpd.GeoSeries([poly],crs=crs)
    xmin, ymin, xmax, ymax = spoly.total_bounds
    #sub_explo=country_boundary_us.cx[xmin:xmax,ymin:ymax]
    sub_explo=exploded.cx[xmin:xmax,ymin:ymax]
    sub_explo=sub_explo.reset_index().drop(['level_0','level_1','AFFGEOID','GEOID','NAME'],axis=1)
    print('sub explo read')
    return sub_explo

def intersecting_points(interp,sub_explo):
    pointsinPolys_intersects=sjoin(interp,sub_explo,how="left")
    grouped = pointsinPolys_intersects.groupby('index_right')
    grouped=grouped.apply(lambda x: x.reset_index(drop = True))
    grouped=grouped.dropna(axis=0)
    grouped=grouped.set_index(grouped.columns[0]).reset_index()
    grouped.to_file(driver='ESRI Shapefile', filename=s3_geotherm_result+'/interp_masked_out_1dp_no_filter.shp')
    pipe = subprocess.run(directory+'gdal_command.sh')
    print('gdal command run')
    print(grouped.head())
    grouped.to_csv(s3_geotherm_result+'/geotherm_grad_grouped_1dp_no_filter.csv')
    return grouped

def read_grouped():
    print('Importing geothermal gradients')
    grouped=pd.read_csv(s3_geotherm_result+'/geotherm_grad_grouped_1dp_no_filter.csv')
    grouped=grouped.drop([grouped.columns[0],'index_right','geometry'],axis=1)
    grouped=grouped.round({'Lat':1,'Lon':1})  #This is just formatting the csv correctly, for some reason wasn't happy
    grouped=grouped.round({'Grad':1})
    return grouped

def main(geo):
    """only running the finished database """
    interp=read_geotherm(geo)
    interp=interp_gradient(interp)
    sub_explo=read_shape()
    grouped=intersecting_points(interp,sub_explo)
    grouped=read_grouped()
    return grouped


if __name__ == "__main__":
	main()
