import os
import numpy as np
import pandas as pd
import sys

data='INPUT_DATA'
dolomite_stats='INPUT_DATA/dolomite_stats'

def depth_RI(experi,smallusgs):
	RI_vals = pd.read_csv('s3://co-2-gasp-bucket/'+dolomite_stats+'/DepthID_RI.csv',sep=',',header=0,usecols=list(range(4)))
	DepthID_VALS = pd.read_csv('s3://co-2-gasp-bucket/'+dolomite_stats+'/DepthID_VALUES.csv',sep=',',header=0,usecols=list(range(2)))
	FIELD_RI_vals = pd.read_csv('s3://co-2-gasp-bucket/'+dolomite_stats+'/Field_RI.csv',sep=',',header=0,usecols=list(range(4)))


	print(len(DepthID_VALS['DepthID'].unique()))
	print(len(RI_vals['DepthID'].unique()))
	DepthID_VALS_v2=pd.merge(DepthID_VALS,RI_vals,on=['DepthID'],how='left', indicator=True)
	#DepthID_VALS_v2 = pd.merge(DepthID_VALS, RI_vals, on='DepthID', how='outer', indicator=True)
	DepthID_VALS_v2.loc[DepthID_VALS_v2._merge=='left_only','DepthID']='BLANK' #change this to field RI value

	DepthID_VALS_v2=pd.merge(DepthID_VALS_v2,FIELD_RI_vals,on=['Field'],how='left')
	DepthID_VALS_v2.loc[DepthID_VALS_v2.DepthID=='BLANK','RI']=DepthID_VALS_v2.Field_RI#1.475448702559207881e+01  #RI field RI
	DepthID_VALS_v2.loc[DepthID_VALS_v2.DepthID=='BLANK','Log_KSP']=DepthID_VALS_v2.Field_Log_KSP#-17.27292936

	DepthID_VALS_v2.loc[DepthID_VALS_v2.DepthID=='BLANK','RI_J21']=DepthID_VALS_v2.Field_RI_J21#1.475448702559207881e+01  #RI field RI
	#DepthID_VALS_v2 = DepthID_VALS_v2.drop(DepthID_VALS_v2.columns[0], axis=1)
	DepthID_VALS_v2.to_csv('s3://co-2-gasp-bucket/'+dolomite_stats+'/DepthID_VALS_v2.csv',sep=',',index=False)
	#DepthID_VALS_v2=DepthID_VALS.merge(RI_vals,on='DepthID')
	#print(experi)
	#print(smallusgs)

	#print(DepthID_VALS_v2.head(10))

	#print(smallusgs.head(10))
	return DepthID_VALS_v2,RI_vals


def phreeqc_carb_capt_pre_eq(experi,smallusgs,DepthID_VALS_v2,RI_vals):
	"""For use in calculating the equilibrium constants"""
	smallusgs = smallusgs.rename(columns={'ID': 'Number','LITHOLOGY':'Description'})
	with open('s3://co-2-gasp-bucket/'+dolomite_stats+'/Carb_capt_v1_pre_eq.txt', 'w') as f:
		f.write('\n \n \n')
		f.write('PHASES \n')
		for i in range(len(RI_vals)):
			f.write('Dolomite_%s  \n '% RI_vals.iloc[i,0])
			f.write('CaMg(CO3)2 = Ca+2 + Mg+2 + 2 CO3-2 \n')
			f.write('log_k	%.10f \n' % RI_vals.iloc[i,2])
			f.write('-analytical_expression %.15f -6.249587568129059967e-02  -3.993501915103184274e+03 \n' % RI_vals.iloc[i,1])
			f.write('delta_h -7.147 kcal \n')
			f.write('-Vm 64.5 \n')
			f.write('\n')

	with open(data_import.temp+'/Carb_capt_v1_pre_eq.txt', 'a') as f:
			f.write('TITLE USGS Produced Water Database with new phases \n')
			f.write('SOLUTION_SPREAD \n')
			f.write('Units mg/l \n ')

	smallusgs.to_csv(data_import.temp+'/Carb_capt_v1_pre_eq.txt', header=True, index=False, mode='a', sep='\t')

	RI_vals_list=[]
	for i in range(len(RI_vals)):
		RI_vals_list.append('Dolomite_%s '% RI_vals.iloc[i,0])
	print(RI_vals_list)

	with open(data_import.temp+'/Carb_capt_v1_pre_eq.txt', 'a') as f:
			f.write('\n \n')
			f.write('SELECTED_OUTPUT \n')
			f.write('-file Carb_capt_out_co2_pre_eq.sel \n')
			f.write('-reset false \n')
			f.write('-solution true \n')
			f.write('-temperature true \n')
			f.write('-saturation_indices  Dolomite Calcite Halite CO2(g) \n')
			f.write('-activities Mg+2 Ca+2 CO3-2 \n')
			f.write('-ionic_strength true \n')
			f.write('-equilibrium_phases Calcite CO2(g) ')
			for i in range(len(RI_vals_list)):
				f.write('%s'  % RI_vals_list[i] )

	with open(data_import.temp+'/Carb_capt_v1_pre_eq.txt', 'a') as f:
		for i in range(len(smallusgs)):
			f.write('\n \n')
			f.write('USE SOLUTION %i \n' % experi.iloc[i,1])
			f.write('REACTION_TEMPERATURE %i \n'% (experi.iloc[i,1]))
			f.write('%i \n'% experi.iloc[i,0])
			f.write('REACTION_PRESSURE %i \n' % experi.iloc[i,1])
			f.write('%i \n' % experi.iloc[i,2])
			f.write('EQUILIBRIUM_PHASES %i \n' % experi.iloc[i,1])
			f.write('Dolomite_%s 0.0 100.0 \n '% DepthID_VALS_v2.iloc[i,0])
			f.write('Calcite 0.0 100.0 \n')
			f.write('SAVE SOLUTION %i \n'% (experi.iloc[i,3]))
			f.write('END \n')
			f.write('USE SOLUTION %i \n' % experi.iloc[i,3])
			f.write('REACTION_TEMPERATURE %i \n'% experi.iloc[i,3])
			f.write('%i \n'% experi.iloc[i,0])
			f.write('REACTION_PRESSURE %i \n' % experi.iloc[i,3])
			f.write('%i \n' % experi.iloc[i,2])
			f.write('EQUILIBRIUM_PHASES %i \n' % experi.iloc[i,3])
			f.write('Dolomite_%s 0.0 100.0 \n '% DepthID_VALS_v2.iloc[i,0])
			f.write('Calcite 0.0 100.0 \n')
			f.write('CO2(g) %.2f 10000 \n'% np.log10(experi.iloc[i,2]))  #partial pressure drop by 20%
			f.write('END \n')
