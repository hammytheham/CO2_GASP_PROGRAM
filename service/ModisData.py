from pydap.client import open_url
import pandas as pd
import numpy as np
import data_import
## MODIS data analysis - not run by the main file nor set up to
from file_paths import s3_MODIS_results
# MODIS_results = '/Users/hamish/github/co2_gasp/INPUT_DATA/MODIS_result_files' old



def read_files():
    h08v03=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h08v03%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h08v04=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h08v04%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h08v05=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h08v05%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h08v06=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h08v06%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h09v02=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h09v02%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h09v03=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h09v03%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h09v04=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h09v04%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h09v05=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h09v05%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h09v06=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h09v06%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h09v07=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h09v07%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h10v02=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h10v02%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h10v03=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h10v03%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h10v04=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h10v04%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h10v05=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h10v05%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h10v06=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h10v06%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h11v02=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h11v02%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h11v03=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h11v03%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h11v04=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h11v04%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h11v05=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h11v05%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h11v06=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h11v06%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h12v01=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h12v01%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h12v02=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h12v02%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h12v03=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h12v03%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h12v04=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h12v04%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h12v05=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h12v05%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h13v01=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h13v01%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h13v02=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h13v02%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h13v03=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h13v03%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h13v04=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h13v04%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h14v01=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h14v01%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h14v02=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h14v02%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h14v03=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h14v03%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h14v04=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h14v04%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h15v01=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h15v01%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')
    h15v02=open_url('http://icdc.cen.uni-hamburg.de/thredds/dodsC/ftpthredds/modis_lst_climatology/acp_2230MOD_h15v02%5By%5D2003-2014%5BQC%5Dall%5BmO%5D100%5Bv%5D0.7.nc?lat[0:1:1199][0:1:1199],lon[0:1:1199][0:1:1199],MAST[0:1:1199][0:1:1199]')

    tiles={'h08v03_data':h08v03,'h08v04_data':h08v04,'h08v05_data':h08v05,'h08v06_data':h08v06,'h09v02_data':h09v02,
           'h09v03_data':h09v03,'h09v04_data':h09v04,'h09v05_data':h09v05,'h09v06_data':h09v06,'h09v07_data':h09v07,
           'h10v02_data':h10v02,'h10v03_data':h10v03,'h10v04_data':h10v04,'h10v05_data':h10v05,'h10v06_data':h10v06,
           'h11v02_data':h11v02,'h11v03_data':h11v03,'h11v04_data':h11v04,'h11v05_data':h11v05,'h11v06_data':h11v06,
           'h12v01_data':h12v01,'h12v02_data':h12v02,'h12v03_data':h12v03,'h12v04_data':h12v04,'h12v05_data':h12v05,
           'h13v01_data':h13v01,'h13v02_data':h13v02,'h13v03_data':h13v03,'h13v04_data':h13v04,'h14v01_data':h14v01,
           'h14v02_data':h14v02,'h14v03_data':h14v03,'h14v04_data':h14v04,'h15v01_data':h15v01,'h15v02_data':h15v02}

    return tiles

def processing1(tile):
    lat=tile.lat[:].reshape(-1,1).data.flatten().byteswap().newbyteorder()
    lon=tile.lon[:].reshape(-1,1).data.flatten().byteswap().newbyteorder()
    mas=tile.MAST[:].reshape(-1,1).data.flatten().byteswap().newbyteorder()
    df=pd.DataFrame({'lat':lat[:],'lon':lon[:],'mas':mas[:]})
    df=df.round({'lat':1,'lon':1})
    df=df[df.mas != -9999.0]
    df=df.groupby([df.lat,df.lon]).mean()
    df=df.reset_index()
    return df

def processing2(tiles):
    tiles_df={}
    for key,value in tiles.items():
        tiles_df.update({key+str('_df'):processing1(value)})
    return tiles_df

def processing3(tiles_df):
    merged=pd.concat(tiles_df.values())
    merged=merged[merged.mas != -9999.0]
    merged.columns = ['Lat', 'Lon','TempSur']
    merged.to_csv(s3_MODIS_results+'/merged_data_2',index=False,float_format = "%.1f",)
    #return merged

def read_modis():
    print('Importing MODIS data')
    merged=pd.read_csv(s3_MODIS_results+'/merged_data_2') #names=['Lat','Lon','TempSur']
    print(merged.head(10))
    merged=merged.drop_duplicates(subset=['Lat','Lon'],keep='first')
    return merged

def trim_merged(merged):
    merged["TempSur_celsius"] = merged["TempSur"] - 273.15
    merged=merged.round({'TempSur_celsius':0})
    sur1=merged.copy()
    print( 'lat n lon = ',sur1[(sur1.Lat == 41.1) & (sur1.Lon == -79.7)])  # this one is fine
    print( 'lat n lon = ',sur1[(sur1.Lat == 41.0) & (sur1.Lon == -80.5)])
    return sur1

def processing4_testing(merged):
    lat1,lon1=np.meshgrid(merged.Lat, merged.Lon)
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = Axes3D(fig)
    print(merged.mas)
    surf = ax.plot_surface(lat1, lon1, merged.TempSur,rstride=1000,cstride=1000)
    print('trial of savefig')
    plt.savefig(data_import.fig+'/modis_test_testing123.jpg')

def processing4(merged):
    lat1,lon1=np.meshgrid(merged.lat, merged.lon)
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = Axes3D(fig)
    surf = ax.plot_surface(lat1, lon1, merged.mas)
    plt.savefig(data_import.fig+'/modis_test.png')

def main():
    tiles=read_files()
    tiles_df=processing2(tiles)
    processing3(tiles_df)
    merged=read_modis()  #import finished surface gradients - only line of code needed for normal operation, trim merged is performed in dataimport
    return merged


    #merged=trim_merged(merged)
    ####unused plotting
    #processing4(merged)
    #processing4_testing(merged) #I dont think it works so did the graphics plot in qgis
    #return merged

if __name__ == "__main__":
	main()

#merged_in=pd.read_csv('/Users/hamish/Desktop/temperature/merged_data_2')
#merged_in.head()
#
#merged_in[merged_in.mas != -9999.0]

#lat1,lon1=np.meshgrid(merged_in.lat, merged_in.lon)

#lat=h15v02.lat[:]
#lon=h15v02.lon[:]
#mas=h15v02.MAST[:]
#
#lat=lat.reshape(-1,1).data.flatten().byteswap().newbyteorder()
#lon=lon.reshape(-1,1).data.flatten().byteswap().newbyteorder()
#mas=mas.reshape(-1,1).data.flatten().byteswap().newbyteorder()

#df=pd.DataFrame({'lat':lat[:],'lon':lon[:],'mas':mas[:]})
#
#df=df.round({'lat':1,'lon':1})
#df=df.groupby([df.lat,df.lon]).mean()
#df=df.reset_index()

#
#data=gridA.lat
#data.shape

#float_format = "%.nf"

#var=data[:]


#var[101].round
