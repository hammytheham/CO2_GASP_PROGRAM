import os
import numpy as np
import pandas as pd
import data_import

def mean_depth(rawusgs):
	"""Sample depth.Create a mean of the depth between the upper and lower peforations (ingnoring NaN
	values). Convert to km. Append to database. Rename columns. Make a permant copy to new
	dataframe USGS
	incoming - rawusgs
	outgoing - formated USGS
	"""
	rawusgs['Depth']=rawusgs[['DEPTHUPPER', 'DEPTHLOWER']].mean(axis=1)
	rawusgs.Depth = rawusgs.Depth * 0.0003048 # Convert ft to km (km in smuh database)
	rawusgs = rawusgs.rename(columns={'LATITUDE': 'Lat', 'LONGITUDE': 'Lon'})
	rawusgs['Lat_OLD']=rawusgs['Lat'] #Preserved for full LATITUDE/LONGITUDE values. Lat/Lon.
	rawusgs['Lon_OLD']=rawusgs['Lon']
	usgs=rawusgs.copy()
	print('usgs=',len(usgs))
	return usgs

def quality_control(usgs):
		#Cull breakdown for stats
		print('Length of original usgs dataframe',len(usgs))
		ph=usgs[(usgs.PH >= 3.5 ) & (usgs.PH <= 11 )]
		print('pH fail - NaN or < 3.5 & > 11: (%)',100-((len(ph)/len(usgs))*100))
		chargebalance=usgs[(usgs.chargebalance >= -15.0 ) & (usgs.chargebalance <= 15.0 )]
		print('Charge balance fail - NaN or  <-15 & >+15 (%) ' ,100-((len(chargebalance)/len(usgs))*100))
		mg=usgs[(usgs.Mg > 0.0 ) & (usgs.Ca > 0.0 )]
		print('Mg fail - i.e. NaN or Ca or Mg <0.0  (%)',100-((len(mg)/len(usgs))*100))
		depth=usgs[(usgs.Depth > 0.0)]
		print('Depth fail - NaN or <0.0 (%)',100-((len(depth)/len(usgs))*100))
		lat=usgs[(usgs.Lat > 0.0) & (usgs.Lon < 0.0)]
		print('Lat fail Nan or Lat <0 or Lon >0  (%)',100-((len(lat)/len(usgs))*100))
		#sys.exit()
		lith=usgs.loc[~(pd.isnull(usgs.LITHOLOGY))] #not ~ null lithology
		print('No lithology information (%)',100-((len(lith)/len(usgs))*100))
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
		print('Lithology failing the simplified lithoogy criteria (%)',100-((len(lith)/len(usgs))*100))


def lithology_simple_CULL(usgs):
	""" Cull samples based on geochemical filtering criteria. Sinmplify lithology labels into  more organised, generalized groups of 5 different lithologies
	"""
	a=len(usgs)
	print('usgs=',a)
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
	usgs=usgs.round({'Lat':1,'Lon':1}) #round locations to 0.1dp - neccessary?

	usgs.loc[usgs.LITHOLOGY == 'Anhydrite and dolomite','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Chert, Dolomite, Other','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Chert, Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Limestone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Limestone, Sandstone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Limestone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Sandstone, Shale','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Shale','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Siltstone','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Sandstone','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Sandstone, Shale','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Sandstone, Siltstone','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Shale','LITHOLOGY'] = 'Shale'
	usgs.loc[usgs.LITHOLOGY == 'Carbonate','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Carbonate, Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Carbonate, Sandstone, Shale, Siltstone, Other','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Chalk','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Dolomite','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Dolomite, Limestone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Dolomite, Limestone, Sandstone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Dolomite, Sandstone, Shale','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Dolomite, Shale','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Limestone','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Sandstone','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite & Lime','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite - Lime','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Limestone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Limestone, Sandstone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Limestone, Sandstone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Limestone, Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Limestone, Sandstone, Siltstone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Limestone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Sandstone, Shale','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Sandstone, Siltstone','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Shale','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Siltstone','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Limestone & Dol','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Limestone & San','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone & Sha','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone - Dol','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Limestone Dolom','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Limestone, Sandstone','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone, Sandstone, Shale','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone, Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone, Sandstone, Siltstone','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone, Shale','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone; Dolostone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Sand','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sand Stone','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Other','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Shale','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Shale, Other','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Shale, Siltstone, Other','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Siltstone','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Siltstone, Other','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Shale, Other','LITHOLOGY'] = 'Shale'
	usgs.loc[usgs.LITHOLOGY == 'Shale, Siltstone','LITHOLOGY'] = 'Shale'
	usgs.loc[usgs.LITHOLOGY == 'Siltstone','LITHOLOGY'] = 'Shale'
	print("percent remaining from original ",((len(usgs)/len(a))*100))
	return usgs


def lithology_small_CULL(usgs):
	""" Cull samples based on geochemical filtering criteria. Sinmplify lithology labels into  more organised, generalized groups of 5 different lithologies.
	Cull samples without a lithology or an unclear lithology.
	"""
	a=len(usgs)
	print('usgs=',a)
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


	usgs = usgs[usgs.LITHOLOGY != 'Anhydrite']                    #CULLED
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite and dolomite','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Chert, Dolomite, Other','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Chert, Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Limestone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Limestone, Sandstone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Limestone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Sandstone, Shale','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Shale','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Dolomite, Siltstone','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Sandstone','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Sandstone, Shale','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Sandstone, Siltstone','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Anhydrite, Shale','LITHOLOGY'] = 'Shale'
	usgs.loc[usgs.LITHOLOGY == 'Carbonate','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Carbonate, Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Carbonate, Sandstone, Shale, Siltstone, Other','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Chalk','LITHOLOGY'] = 'Limestone'
	usgs = usgs[usgs.LITHOLOGY != 'Chat']                         #CULLED
	usgs = usgs[usgs.LITHOLOGY != 'Chert']                         #CULLED
	usgs.loc[usgs.LITHOLOGY == 'Chert, Dolomite','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Dolomite, Limestone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Dolomite, Limestone, Sandstone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Dolomite, Sandstone, Shale','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Dolomite, Shale','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Limestone','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Chert, Sandstone','LITHOLOGY'] = 'Sandstone'
	usgs = usgs[usgs.LITHOLOGY != 'Coal']                         #CULLED
	usgs = usgs[usgs.LITHOLOGY != 'Conglomerate']                 #CULLED
	usgs.loc[usgs.LITHOLOGY == 'Dolomite & Lime','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite - Lime','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Limestone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Limestone, Sandstone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Limestone, Sandstone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Limestone, Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Limestone, Sandstone, Siltstone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Limestone, Shale','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Sandstone','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Sandstone, Shale','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Sandstone, Siltstone','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Shale','LITHOLOGY'] = 'Dolomite'
	usgs.loc[usgs.LITHOLOGY == 'Dolomite, Siltstone','LITHOLOGY'] = 'Dolomite'
	usgs = usgs[usgs.LITHOLOGY != 'Ga1g']                         #CULLED
	usgs = usgs[usgs.LITHOLOGY != 'Ga1n']                         #CULLED
	usgs = usgs[usgs.LITHOLOGY != 'Ga1r']                         #CULLED
	usgs.loc[usgs.LITHOLOGY == 'Limestone & Dol','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Limestone & San','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone & Sha','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone - Dol','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Limestone Dolom','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs.loc[usgs.LITHOLOGY == 'Limestone, Sandstone','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone, Sandstone, Shale','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone, Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone, Sandstone, Siltstone','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone, Shale','LITHOLOGY'] = 'Limestone'
	usgs.loc[usgs.LITHOLOGY == 'Limestone; Dolostone','LITHOLOGY'] = 'Mixed_Carbonate'
	usgs = usgs[usgs.LITHOLOGY != 'Other']                        #CULLED
	usgs.loc[usgs.LITHOLOGY == 'Sand','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sand Stone','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Other','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Shale','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Shale, Other','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Shale, Siltstone','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Shale, Siltstone, Other','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Siltstone','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Sandstone, Siltstone, Other','LITHOLOGY'] = 'Sandstone'
	usgs.loc[usgs.LITHOLOGY == 'Shale, Other','LITHOLOGY'] = 'Shale'
	usgs.loc[usgs.LITHOLOGY == 'Shale, Siltstone','LITHOLOGY'] = 'Shale'
	usgs.loc[usgs.LITHOLOGY == 'Siltstone','LITHOLOGY'] = 'Shale'
	usgs = usgs[usgs.LITHOLOGY != 'Unknown']                      #CULLED
	print("percent remaining from original ",((len(usgs)/len(a))*100))
	return usgs

def lithology_ALL_CULL(usgs):
	""" Cull samples based on geochemical filtering criteria. Sinmplify lithology labels into  more organised, generalized groups of 5 different lithologies.
	Cull samples without a lithology or an unclear lithology.
	"""
	a=len(usgs)
	print('usgs=',a)
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
	usgs=usgs.round({'Lat':1,'Lon':1})
	print("percent remaining from original ",((len(usgs)/len(a))*100))
	return usgs



def lithology_no_geochem_CULL(usgs):
	""" Cull samples based on geochemical filtering criteria. Sinmplify lithology labels into  more organised, generalized groups of 5 different lithologies.
	Cull samples without a lithology or an unclear lithology.
	"""
	a=len(usgs)
	print('usgs=',a)
	usgs=usgs.round({'Lat':1,'Lon':1})
	print("percent remaining from original ",((len(usgs)/len(a))*100))
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
	#sys.exit()
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


def main():
	usgs,grad,sur=read_in_data()
	quality_control(usgs)
	if lithology_simple ==True:
		usgs2=lithology_simple_CULL(usgs)
	if lithology_small==True:
		usgs2=lithology_small_CULL(usgs)
	if lithology_all==True:
		usgs2=lithology_ALL_CULL(usgs)
	if lithology_all_no_geochem_filter==True:
		usgs2=lithology_no_geochem_CULL(usgs)





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
