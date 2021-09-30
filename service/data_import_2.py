
import os
import numpy as np
import pandas as pd
import sys

geochem_result = 'INPUT_DATA/geochemical_result_files'


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


def data_processing6(usgs1,sur,grad):
	"""Merge the dataframes into a single dataframe called medusgs
	"""
	print('usgs2 = ',len(usgs1))
	medusgs=usgs1.merge(sur,on=['Lat','Lon'])
	print('medusgs =',len(medusgs))
	medusgs=grad.merge(medusgs,on=['Lat','Lon'])
	print('medusgs with grad =',len(medusgs))
	print((len(medusgs)/len(usgs1))*100)

	print('Sandstone=',len(medusgs[medusgs.LITHOLOGY == 'Sandstone']),(len(medusgs[medusgs.LITHOLOGY == 'Sandstone'])/len(medusgs))*100)
	print('Dolomite=',len(medusgs[medusgs.LITHOLOGY == 'Dolomite']),(len(medusgs[medusgs.LITHOLOGY == 'Dolomite'])/len(medusgs))*100)
	print('Limestone=',len(medusgs[medusgs.LITHOLOGY == 'Limestone']),(len(medusgs[medusgs.LITHOLOGY == 'Limestone'])/len(medusgs))*100)
	print('Shale=',len(medusgs[medusgs.LITHOLOGY == 'Shale']),(len(medusgs[medusgs.LITHOLOGY == 'Shale'])/len(medusgs))*100)
	print('Mixed_Carbonate=',len(medusgs[medusgs.LITHOLOGY == 'Mixed_Carbonate']),(len(medusgs[medusgs.LITHOLOGY == 'Mixed_Carbonate'])/len(medusgs))*100)
	medusgs['TemperatureSMU']= (medusgs.Depth * medusgs.Grad) + medusgs.TempSur_celsius #Adding in the surface temperature correction
	print('medusgs.head',medusgs.head(5))
	print('medusgs=',len(medusgs))
	medusgs.to_csv('s3://co-2-gasp-bucket/'+geochem_result+'/merged_data', index=False)
	return medusgs



def main(rawusgs,grad,sur):
	usgs=data_processing1(rawusgs)
	usgs1=data_processing2(usgs)
	medusgs=data_processing6(usgs1,sur,grad)
	return medusgs

if __name__ == "__main__":
	main(rawusgs,grad,sur)
