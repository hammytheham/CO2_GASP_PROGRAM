import os
import numpy as np
import sys
import pandas as pd

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
import datetime
import matplotlib.patches as ptch
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.ticker as ticker

geochemical_result='/home/ec2-user/environment/CO2_GASP_PROGRAM/temp/OUTPUT_DATA/geochemical_result'

def read_in(user_job):
	carb_co2_pre_eq = pd.read_csv(geochemical_result+'/'+str(user_job)+'/Carb_capt_user_job.sel',sep='\t',skipinitialspace=True,header=0) #present equilibrium
	#carb_co2_pre_eq = pd.read_csv(geochemical_result+'/'+user_job+'/Carb_capt_user_job.sel',sep='\t', skiprows=[i for j in (range(1, 11482), range(11483,34442,2)) for i in j],skipinitialspace=True,header=0) #present equilibrium
	initial_chem=carb_co2_pre_eq.iloc[:(int(len(carb_co2_pre_eq)/3))]
	#print(initial_chem.head(10))
	#print(initial_chem.tail(10))
	init_equi=carb_co2_pre_eq.iloc[(int(len(carb_co2_pre_eq)/3)):(int(len(carb_co2_pre_eq))-1):2]
	fin_equi=carb_co2_pre_eq.iloc[((int(len(carb_co2_pre_eq)/3))+1):int(len(carb_co2_pre_eq)):2]
	#print(init_equi.head(10))
	#print(init_equi.tail(10))
	#print(fin_equi.head(10))
	#print(fin_equi.tail(10))	s
	
	return carb_co2_pre_eq

def poro_converter():
	
	





def data_processing_1(carb,carb_co2,main_dolomite,order_dolomite,disorder_dolomite,sim_1,sim_2,sim_pre,sim_1_ref,sim_2_ref,dis_dolomite_no_co,ord_dolomite_no_co,main_dolomite_no_co,C02_no_mineral,low_temp_high_temp_no_min_sim_1,low_temp_high_temp_no_min_sim_2,initial,carb_co2_pre_eq,main_dolomite_pre_eq,order_dolomite_pre_eq,disorder_dolomite_pre_eq,sim_1_old,sim_2_old,smallusgs,medusgs):
	RI_vals = pd.read_csv(data_import.temp+'/DepthID_RI.csv',sep=',',header=0,usecols=list(range(3)))
	DepthID_VALUES=pd.read_csv(data_import.temp+'/DepthID_VALUES.csv',sep=',',header=0,usecols=list(range(1)))
	DepthID_VALS_v2=pd.read_csv(data_import.temp+'/DepthID_VALS_v2.csv',sep=',',header=0,usecols=list(range(8)))  #<- delete sylvarnena at line 2817 ahu1
	#print('heads')
	#print(RI_vals.head(10))
	#print(DepthID_VALUES.head(10))
	#print(DepthID_VALS_v2.head(10))
	RI_vals_list=[]
	for i in range(len(RI_vals)):
		RI_vals_list.append('d_Dolomite_%s'% RI_vals.iloc[i,0])
	#RI_vals=pd.concat([pd.DataFrame(RI_vals_list),RI_vals],axis=1)
	#print('RI_vals_1')
	#print(RI_vals.head(10))
	#print(DepthID_VALUES.head(10))
	#RI_vals=pd.merge(DepthID_VALUES,RI_vals,on=['DepthID'],how='left')
	#print('DepthID_VALS_v2')
	#print(DepthID_VALS_v2.head(10))
	#print('RI_vals_2')
	#print(RI_vals.head(10))
	#print(RI_vals.tail(10))
	#sys.exit()
	carb_v1 = carb[RI_vals_list]
	#carb_v1.merge(RI_vals,on=['soln'],how='outer',)
	carb_v1['soln'] = carb['soln']
	carb_v1['d_Dol_no_co2'] = carb_v1.replace(0, np.nan).bfill(axis=1).iloc[:, 0].fillna(0)
	carb_v1['d_Calcite_no_co2']=carb['d_Calcite']
	carb_v1['d_Calcite_vol_no_co2']= (carb_v1.d_Calcite_no_co2*100.09)/2.71
	carb_v1['d_Dol_vol_no_co2']=(carb_v1.d_Dol_no_co2*184.4)/2.85
	carb_v1['tot_min_no_co2']=carb_v1.d_Dol_vol_no_co2 + carb_v1.d_Calcite_vol_no_co2
	print(carb_v1.head(10))
	print(carb_v1.tail(10))
	print(len(DepthID_VALS_v2))
	print(len(carb_v1))
	carb_v1=pd.concat([DepthID_VALS_v2,carb_v1],axis=1)
	print(carb_v1.head(10))
	print(carb_v1.tail(10))
	print(len(carb_v1))
	#print(carb_v1.head(10))


	carb_co2_v1 = carb_co2[RI_vals_list]
	carb_co2_v1['soln'] = carb_co2['soln']
	carb_co2_v1['temp'] = carb_co2['temp']
	carb_co2_v1['d_Dol_mixed'] = carb_co2_v1.replace(0, np.nan).bfill(axis=1).iloc[:, 0].fillna(0)
	carb_co2_v1['d_CO2_mixed']=carb_co2['d_CO2(g)']
	carb_co2_v1['d_Calcite_mixed']=carb_co2['d_Calcite']
	carb_co2_v1['d_Calcite_vol_mixed']= (carb_co2_v1.d_Calcite_mixed*100.09)/2.71
	carb_co2_v1['d_Dol_vol_mixed']=(carb_co2_v1.d_Dol_mixed*184.4)/2.85
	carb_co2_v1['tot_min_mixed']=carb_co2_v1.d_Dol_vol_mixed + carb_co2_v1.d_Calcite_vol_mixed



	carb_co2_pre_eq_v1 = carb_co2_pre_eq[RI_vals_list]
	carb_co2_pre_eq_v1['soln'] = carb_co2_pre_eq['soln']-11480
	carb_co2_pre_eq_v1['temp'] = carb_co2_pre_eq['temp']
	carb_co2_pre_eq_v1['d_Dol_mixed_pre_eq'] = carb_co2_pre_eq_v1.replace(0, np.nan).bfill(axis=1).iloc[:, 0].fillna(0)
	carb_co2_pre_eq_v1['d_CO2_mixed_pre_eq']=carb_co2_pre_eq['d_CO2(g)']
	carb_co2_pre_eq_v1['d_Calcite_mixed_pre_eq']=carb_co2_pre_eq['d_Calcite']
	carb_co2_pre_eq_v1['d_Calcite_vol_mixed_pre_eq']= (carb_co2_pre_eq_v1.d_Calcite_mixed_pre_eq*100.09)/2.71
	carb_co2_pre_eq_v1['d_Dol_vol_mixed_pre_eq']=(carb_co2_pre_eq_v1.d_Dol_mixed_pre_eq*184.4)/2.85
	carb_co2_pre_eq_v1['tot_min_mixed_pre_eq']=carb_co2_pre_eq_v1.d_Dol_vol_mixed_pre_eq + carb_co2_pre_eq_v1.d_Calcite_vol_mixed_pre_eq

	main_dolomite['d_CO2_global']=main_dolomite['d_CO2(g)']
	main_dolomite['d_Dolomite_global']=main_dolomite['d_Dolomite_new']
	main_dolomite['d_Calcite_global']=main_dolomite['d_Calcite']
	main_dolomite['d_Calcite_vol_global']= (main_dolomite.d_Calcite_global*100.09)/2.71
	main_dolomite['d_Dol_vol_global']=(main_dolomite.d_Dolomite_global*184.4)/2.85
	main_dolomite['tot_min_global']=main_dolomite.d_Dol_vol_global + main_dolomite.d_Calcite_vol_global

	main_dolomite_no_co['d_Dolomite_global_no_co']=main_dolomite_no_co['d_Dolomite_new']
	main_dolomite_no_co['d_Calcite_global_no_co']=main_dolomite_no_co['d_Calcite']
	main_dolomite_no_co['d_Calcite_vol_global_no_co']= (main_dolomite_no_co.d_Calcite_global_no_co*100.09)/2.71
	main_dolomite_no_co['d_Dol_vol_global_no_co']=(main_dolomite_no_co.d_Dolomite_global_no_co*184.4)/2.85
	main_dolomite_no_co['tot_min_global_no_co']=main_dolomite_no_co.d_Dol_vol_global_no_co + main_dolomite_no_co.d_Calcite_vol_global_no_co

	main_dolomite_pre_eq['soln'] = main_dolomite_pre_eq['soln']-11480
	main_dolomite_pre_eq['d_CO2_global_pre_eq']=main_dolomite_pre_eq['d_CO2(g)']
	main_dolomite_pre_eq['d_Dolomite_global_pre_eq']=main_dolomite_pre_eq['d_Dolomite_new']
	main_dolomite_pre_eq['d_Calcite_global_pre_eq']=main_dolomite_pre_eq['d_Calcite']
	main_dolomite_pre_eq['d_Calcite_vol_global_pre_eq']= (main_dolomite_pre_eq.d_Calcite_global_pre_eq*100.09)/2.71
	main_dolomite_pre_eq['d_Dol_vol_global_pre_eq']=(main_dolomite_pre_eq.d_Dolomite_global_pre_eq*184.4)/2.85
	main_dolomite_pre_eq['tot_min_global_pre_eq']=main_dolomite_pre_eq.d_Dol_vol_global_pre_eq + main_dolomite_pre_eq.d_Calcite_vol_global_pre_eq

	order_dolomite['d_CO2_ord']=order_dolomite['d_CO2(g)']
	order_dolomite['d_Dolomite_ord']=order_dolomite['d_Dolomite(ordered)']
	order_dolomite['d_Calcite_ord']=order_dolomite['d_Calcite']
	order_dolomite['d_Calcite_vol_ord']= (order_dolomite.d_Calcite_ord*100.09)/2.71
	order_dolomite['d_Dol_vol_ord']=(order_dolomite.d_Dolomite_ord*184.4)/2.85
	order_dolomite['tot_min_order']=order_dolomite.d_Dol_vol_ord + order_dolomite.d_Calcite_vol_ord

	order_dolomite_pre_eq['soln'] = order_dolomite_pre_eq['soln']-11480
	order_dolomite_pre_eq['d_CO2_ord_pre_eq']=order_dolomite_pre_eq['d_CO2(g)']
	order_dolomite_pre_eq['d_Dolomite_ord_pre_eq']=order_dolomite_pre_eq['d_Dolomite(ordered)']
	order_dolomite_pre_eq['d_Calcite_ord_pre_eq']=order_dolomite_pre_eq['d_Calcite']
	order_dolomite_pre_eq['d_Calcite_vol_ord_pre_eq']= (order_dolomite_pre_eq.d_Calcite_ord_pre_eq*100.09)/2.71
	order_dolomite_pre_eq['d_Dol_vol_ord_pre_eq']=(order_dolomite_pre_eq.d_Dolomite_ord_pre_eq*184.4)/2.85
	order_dolomite_pre_eq['tot_min_order_pre_eq']=order_dolomite_pre_eq.d_Dol_vol_ord_pre_eq + order_dolomite_pre_eq.d_Calcite_vol_ord_pre_eq

	ord_dolomite_no_co['d_Dolomite_ord_no_co']=ord_dolomite_no_co['d_Dolomite(ordered)']
	ord_dolomite_no_co['d_Calcite_ord_no_co']=ord_dolomite_no_co['d_Calcite']
	ord_dolomite_no_co['d_Calcite_vol_ord_no_co']= (ord_dolomite_no_co.d_Calcite_ord_no_co*100.09)/2.71
	ord_dolomite_no_co['d_Dol_vol_ord_no_co']=(ord_dolomite_no_co.d_Dolomite_ord_no_co*184.4)/2.85
	ord_dolomite_no_co['tot_min_order_no_co']=ord_dolomite_no_co.d_Dol_vol_ord_no_co + ord_dolomite_no_co.d_Calcite_vol_ord_no_co

	disorder_dolomite['d_CO2_disord']=disorder_dolomite['d_CO2(g)']
	disorder_dolomite['d_Dolomite_disord']=disorder_dolomite['d_Dolomite(disordered)']
	disorder_dolomite['d_Calcite_disord']=disorder_dolomite['d_Calcite']
	disorder_dolomite['d_Calcite_vol_disord']= (disorder_dolomite.d_Calcite_disord*100.09)/2.71
	disorder_dolomite['d_Dol_vol_disord']=(disorder_dolomite.d_Dolomite_disord*184.4)/2.85
	disorder_dolomite['tot_min_disorder']=disorder_dolomite.d_Dol_vol_disord + disorder_dolomite.d_Calcite_vol_disord

	dis_dolomite_no_co['d_Dolomite_disord_no_co']=dis_dolomite_no_co['d_Dolomite(disordered)']
	dis_dolomite_no_co['d_Calcite_disord_no_co']=dis_dolomite_no_co['d_Calcite']
	dis_dolomite_no_co['d_Calcite_vol_disord_no_co']= (dis_dolomite_no_co.d_Calcite_disord_no_co*100.09)/2.71
	dis_dolomite_no_co['d_Dol_vol_disord_no_co']=(dis_dolomite_no_co.d_Dolomite_disord_no_co*184.4)/2.85
	dis_dolomite_no_co['tot_min_disorder_no_co']=dis_dolomite_no_co.d_Dol_vol_disord_no_co + dis_dolomite_no_co.d_Calcite_vol_disord_no_co

	disorder_dolomite_pre_eq['soln'] = disorder_dolomite_pre_eq['soln']-11480
	disorder_dolomite_pre_eq['d_CO2_disord_pre_eq']=disorder_dolomite_pre_eq['d_CO2(g)']
	disorder_dolomite_pre_eq['d_Dolomite_disord_pre_eq']=disorder_dolomite_pre_eq['d_Dolomite(disordered)']
	disorder_dolomite_pre_eq['d_Calcite_disord_pre_eq']=disorder_dolomite_pre_eq['d_Calcite']
	disorder_dolomite_pre_eq['d_Calcite_vol_disord_pre_eq']= (disorder_dolomite_pre_eq.d_Calcite_disord_pre_eq*100.09)/2.71
	disorder_dolomite_pre_eq['d_Dol_vol_disord_pre_eq']=(disorder_dolomite_pre_eq.d_Dolomite_disord_pre_eq*184.4)/2.85
	disorder_dolomite_pre_eq['tot_min_disorder_pre_eq']=disorder_dolomite_pre_eq.d_Dol_vol_disord_pre_eq + disorder_dolomite_pre_eq.d_Calcite_vol_disord_pre_eq


	sim_1_v1 = sim_1[RI_vals_list]
	sim_1_v1['soln'] = sim_1['soln']-11480
	sim_1_v1['d_Dol_mixed_sim_1'] = sim_1_v1.replace(0, np.nan).bfill(axis=1).iloc[:, 0].fillna(0)
	sim_1_v1['d_CO2_mixed_sim_1']=sim_1['d_CO2(g)']
	sim_1_v1['d_Calcite_mixed_sim_1']=sim_1['d_Calcite']
	sim_1_v1['d_Calcite_vol_mixed_sim_1']= (sim_1_v1.d_Calcite_mixed_sim_1*100.09)/2.71
	sim_1_v1['d_Dol_vol_mixed_sim_1']=(sim_1_v1.d_Dol_mixed_sim_1*184.4)/2.85
	sim_1_v1['tot_min_mixed_sim_1']=sim_1_v1.d_Dol_vol_mixed_sim_1 + sim_1_v1.d_Calcite_vol_mixed_sim_1


	sim_2_v1 = sim_2[RI_vals_list]
	sim_2_v1['soln'] = sim_2['soln']-22960   #old was just -11480 for this line
	sim_2_v1['d_Dol_mixed_sim_2'] = sim_2_v1.replace(0, np.nan).bfill(axis=1).iloc[:, 0].fillna(0)
	sim_2_v1['d_CO2_mixed_sim_2']=sim_2['d_CO2(g)']
	sim_2_v1['d_Calcite_mixed_sim_2']=sim_2['d_Calcite']
	sim_2_v1['d_Calcite_vol_mixed_sim_2']= (sim_2_v1.d_Calcite_mixed_sim_2*100.09)/2.71
	sim_2_v1['d_Dol_vol_mixed_sim_2']=(sim_2_v1.d_Dol_mixed_sim_2*184.4)/2.85
	sim_2_v1['tot_min_mixed_sim_2']=sim_2_v1.d_Dol_vol_mixed_sim_2 + sim_2_v1.d_Calcite_vol_mixed_sim_2

	sim_pre_v1 = sim_pre[RI_vals_list]
	sim_pre_v1['soln'] = sim_pre['soln']-22960   #old was just -11480 for this line
	sim_pre_v1['d_Dol_mixed_sim_pre'] = sim_pre_v1.replace(0, np.nan).bfill(axis=1).iloc[:, 0].fillna(0)
	sim_pre_v1['d_CO2_mixed_sim_pre']=sim_pre['d_CO2(g)']
	sim_pre_v1['d_Calcite_mixed_sim_pre']=sim_pre['d_Calcite']
	sim_pre_v1['d_Calcite_vol_mixed_sim_pre']= (sim_pre_v1.d_Calcite_mixed_sim_pre*100.09)/2.71
	sim_pre_v1['d_Dol_vol_mixed_sim_pre']=(sim_pre_v1.d_Dol_mixed_sim_pre*184.4)/2.85
	sim_pre_v1['tot_min_mixed_sim_pre']=sim_pre_v1.d_Dol_vol_mixed_sim_pre + sim_pre_v1.d_Calcite_vol_mixed_sim_pre



	sim_1_old_v1 = sim_1_old[RI_vals_list]
	sim_1_old_v1['soln'] = sim_1_old['soln']
	sim_1_old_v1['d_Dol_mixed_sim_1_old'] = sim_1_old_v1.replace(0, np.nan).bfill(axis=1).iloc[:, 0].fillna(0)
	sim_1_old_v1['d_CO2_mixed_sim_1_old']=sim_1_old['d_CO2(g)']
	sim_1_old_v1['d_Calcite_mixed_sim_1_old']=sim_1_old['d_Calcite']
	sim_1_old_v1['d_Calcite_vol_mixed_sim_1_old']= (sim_1_old_v1.d_Calcite_mixed_sim_1_old*100.09)/2.71
	sim_1_old_v1['d_Dol_vol_mixed_sim_1_old']=(sim_1_old_v1.d_Dol_mixed_sim_1_old*184.4)/2.85
	sim_1_old_v1['tot_min_mixed_sim_1_old']=sim_1_old_v1.d_Dol_vol_mixed_sim_1_old + sim_1_old_v1.d_Calcite_vol_mixed_sim_1_old


	sim_2_old_v1 = sim_2_old[RI_vals_list]
	sim_2_old_v1['soln'] = sim_2_old['soln']-11480   #old was just -11480 for this line
	sim_2_old_v1['d_Dol_mixed_sim_2_old'] = sim_2_old_v1.replace(0, np.nan).bfill(axis=1).iloc[:, 0].fillna(0)
	sim_2_old_v1['d_CO2_mixed_sim_2_old']=sim_2_old['d_CO2(g)']
	sim_2_old_v1['d_Calcite_mixed_sim_2_old']=sim_2_old['d_Calcite']
	sim_2_old_v1['d_Calcite_vol_mixed_sim_2_old']= (sim_2_old_v1.d_Calcite_mixed_sim_2_old*100.09)/2.71
	sim_2_old_v1['d_Dol_vol_mixed_sim_2_old']=(sim_2_old_v1.d_Dol_mixed_sim_2_old*184.4)/2.85
	sim_2_old_v1['tot_min_mixed_sim_2_old']=sim_2_old_v1.d_Dol_vol_mixed_sim_2_old + sim_2_old_v1.d_Calcite_vol_mixed_sim_2_old



	C02_no_mineral['d_CO2_no_mineral']= C02_no_mineral['d_CO2(g)']

	low_temp_high_temp_no_min_sim_1['d_CO2_no_mineral_lt_ht_sim_1']= low_temp_high_temp_no_min_sim_1['d_CO2(g)']
	low_temp_high_temp_no_min_sim_2['d_CO2_no_mineral_lt_ht_sim_2']= low_temp_high_temp_no_min_sim_2['d_CO2(g)']

	low_temp_high_temp_no_min_sim_2['soln']=low_temp_high_temp_no_min_sim_2['soln']-11480


	#sim_1_ref_v1 = sim_1_ref[RI_vals_list]
	#sim_1_ref_v1['soln'] = sim_1_ref['soln']
	#sim_1_ref_v1['d_Dol_mixed_sim_1_ref'] = sim_1_ref_v1.replace(0, np.nan).bfill(axis=1).iloc[:, 0].fillna(0)
	#sim_1_ref_v1['d_CO2_mixed_sim_1_ref']=sim_1_ref['d_CO2(g)']
	#sim_1_ref_v1['d_Calcite_mixed_sim_1_ref']=sim_1_ref['d_Calcite']
	#sim_1_ref_v1['d_Calcite_vol_mixed_sim_1_ref']= (sim_1_ref_v1.d_Calcite_mixed_sim_1_ref*100.09)/2.71
	#sim_1_ref_v1['d_Dol_vol_mixed_sim_1_ref']=(sim_1_ref_v1.d_Dol_mixed_sim_1_ref*184.4)/2.85
	#sim_1_ref_v1['tot_min_mixed_sim_1_ref']=sim_1_ref_v1.d_Dol_vol_mixed_sim_1_ref + sim_1_ref_v1.d_Calcite_vol_mixed_sim_1_ref

	#sim_2_ref_v1 = sim_2_ref[RI_vals_list]
	#sim_2_ref_v1['soln'] = sim_1_ref['soln']
	#sim_2_ref_v1['d_Dol_new_sim_2_ref'] = sim_2_ref['d_Dolomite_new']
	#sim_2_ref_v1['d_CO2_mixed_sim_2_ref']=sim_2_ref['d_CO2(g)']
	#sim_2_ref_v1['d_Calcite_mixed_sim_2_ref']=sim_2_ref['d_Calcite']
	#sim_2_ref_v1['d_Calcite_vol_mixed_sim_2_ref']= (sim_2_ref_v1.d_Calcite_mixed_sim_2_ref*100.09)/2.71
	#sim_2_ref_v1['d_Dol_vol_new_sim_2_ref']=(sim_2_ref_v1.d_Dol_new_sim_2_ref*184.4)/2.85
	#sim_2_ref_v1['tot_min_mixed_sim_2_ref']=sim_2_ref_v1.d_Dol_vol_new_sim_2_ref + sim_2_ref_v1.d_Calcite_vol_mixed_sim_2_ref

	#print(sim_2_v1.tot_min_mixed_sim_2.head(10))
	#print(sim_2_ref_v1.tot_min_mixed_sim_2_ref.head(10))


	#print(carb_v1.head(10))
	#print(carb_co2_v1.head(10))
	#print(order_dolomite.head(10))
	#print(main_dolomite.head(10))
	#print(disorder_dolomite.head(10))

	d_1=carb_v1[['soln','tot_min_no_co2','d_Calcite_no_co2','d_Dol_no_co2','d_Calcite_vol_no_co2','d_Dol_vol_no_co2','DepthID','RI','Log_KSP','RI_J21']]
	d_2=carb_co2_v1[['soln','d_Dol_mixed','d_CO2_mixed','d_Calcite_mixed','d_Calcite_vol_mixed','d_Dol_vol_mixed','tot_min_mixed','temp']]
	d_3=main_dolomite[['soln','d_CO2_global','d_Dolomite_global','d_Calcite_global','d_Calcite_vol_global','d_Dol_vol_global','tot_min_global']]
	d_4=order_dolomite[['soln','d_CO2_ord','d_Dolomite_ord','d_Calcite_ord','d_Calcite_vol_ord','d_Dol_vol_ord','tot_min_order']]
	d_5=disorder_dolomite[['soln','d_CO2_disord','d_Dolomite_disord','d_Calcite_disord','d_Calcite_vol_disord','d_Dol_vol_disord','tot_min_disorder']]
	d_6=sim_1_v1[['soln','d_Dol_mixed_sim_1','d_CO2_mixed_sim_1','d_Calcite_mixed_sim_1','d_Calcite_vol_mixed_sim_1','d_Dol_vol_mixed_sim_1','tot_min_mixed_sim_1']]
	d_7=sim_2_v1[['soln','d_Dol_mixed_sim_2','d_CO2_mixed_sim_2','d_Calcite_mixed_sim_2','d_Calcite_vol_mixed_sim_2','d_Dol_vol_mixed_sim_2','tot_min_mixed_sim_2']]
	d_8=main_dolomite_no_co[['soln','d_Dolomite_global_no_co','d_Calcite_global_no_co','d_Calcite_vol_global_no_co','d_Dol_vol_global_no_co','tot_min_global_no_co']]
	d_9=ord_dolomite_no_co[['soln','d_Dolomite_ord_no_co','d_Calcite_ord_no_co','d_Calcite_vol_ord_no_co','d_Dol_vol_ord_no_co','tot_min_order_no_co']]
	d_10=dis_dolomite_no_co[['soln','d_Dolomite_disord_no_co','d_Calcite_disord_no_co','d_Calcite_vol_disord_no_co','d_Dol_vol_disord_no_co','tot_min_disorder_no_co']]
	d_11=C02_no_mineral[['soln','d_CO2_no_mineral']]
	d_12=low_temp_high_temp_no_min_sim_1[['soln','d_CO2_no_mineral_lt_ht_sim_1']]
	d_13=low_temp_high_temp_no_min_sim_2[['soln','d_CO2_no_mineral_lt_ht_sim_2']]
	d_14=initial[['soln','mu']]
	d_15=carb_co2_pre_eq_v1[['soln','d_Dol_mixed_pre_eq','d_CO2_mixed_pre_eq','d_Calcite_mixed_pre_eq','d_Calcite_vol_mixed_pre_eq','d_Dol_vol_mixed_pre_eq','tot_min_mixed_pre_eq']]
	d_16=main_dolomite_pre_eq[['soln','d_CO2_global_pre_eq','d_Dolomite_global_pre_eq','d_Calcite_global_pre_eq','d_Calcite_vol_global_pre_eq','d_Dol_vol_global_pre_eq','tot_min_global_pre_eq']]
	d_17=order_dolomite_pre_eq[['soln','d_CO2_ord_pre_eq','d_Dolomite_ord_pre_eq','d_Calcite_ord_pre_eq','d_Calcite_vol_ord_pre_eq','d_Dol_vol_ord_pre_eq','tot_min_order_pre_eq']]
	d_18=disorder_dolomite_pre_eq[['soln','d_CO2_disord_pre_eq','d_Dolomite_disord_pre_eq','d_Calcite_disord_pre_eq','d_Calcite_vol_disord_pre_eq','d_Dol_vol_disord_pre_eq','tot_min_disorder_pre_eq']]
	d_19=sim_1_old_v1[['soln','d_Dol_mixed_sim_1_old','d_CO2_mixed_sim_1_old','d_Calcite_mixed_sim_1_old','d_Calcite_vol_mixed_sim_1_old','d_Dol_vol_mixed_sim_1_old','tot_min_mixed_sim_1_old']]
	d_20=sim_2_old_v1[['soln','d_Dol_mixed_sim_2_old','d_CO2_mixed_sim_2_old','d_Calcite_mixed_sim_2_old','d_Calcite_vol_mixed_sim_2_old','d_Dol_vol_mixed_sim_2_old','tot_min_mixed_sim_2_old']]

	d_21=sim_pre_v1[['soln','d_Dol_mixed_sim_pre','d_CO2_mixed_sim_pre','d_Calcite_mixed_sim_pre','d_Calcite_vol_mixed_sim_pre','d_Dol_vol_mixed_sim_pre','tot_min_mixed_sim_pre']]

	#d_8=sim_1_ref_v1[['soln','d_Dol_mixed_sim_1_ref','d_CO2_mixed_sim_1_ref','d_Calcite_mixed_sim_1_ref','d_Calcite_vol_mixed_sim_1_ref','d_Dol_vol_mixed_sim_1_ref','tot_min_mixed_sim_1_ref']]
	#d_9=sim_2_ref_v1[['soln','d_Dol_new_sim_2_ref','d_CO2_mixed_sim_2_ref','d_Calcite_mixed_sim_2_ref','d_Calcite_vol_mixed_sim_2_ref','d_Dol_vol_new_sim_2_ref','tot_min_mixed_sim_2_ref']]


	print(len(d_1))
	print(len(d_2))
	print(len(d_3))
	print(len(d_4))
	print(len(d_5))
	print(len(d_6))
	print(len(d_7))
	print(len(d_8))
	print(len(d_9))
	print(len(d_10))
	print(len(d_11))
	print(len(d_12))
	print(len(d_13))
	print(len(d_14))

	#print(d_1.head(10))
	#print(d_1.tail(10))
	#print(d_2.head(10))
	#print(d_2.tail(10))
	#print(d_14.head(10))
	#print(d_14.tail(10))

	data_frames = [d_1,d_2,d_3,d_4,d_5,d_6,d_7,d_8,d_9,d_10,d_11,d_12,d_13,d_14,d_15,d_16,d_17,d_18,d_19,d_20,d_21]
	massbal = reduce(lambda  left,right: pd.merge(left,right,on=['soln'],how='outer'), data_frames)
	print('massbal tails')
	print(massbal.tail(10))

	smallusgs = smallusgs.rename(columns={'ID': 'Number','LITHOLOGY':'Description'})
	massbal = massbal.rename(columns={'soln': 'Number'})
	medusgs['Number']=smallusgs.Number
	mass_bal_lith=medusgs.merge(massbal,on='Number')
	mass_bal_lith.to_csv(data_import.temp+'/pre_co2_sequestration.txt', header=True, index=False, mode='w', sep='\t')

	return mass_bal_lith
    #cell15["Calcite_abun_vol"]=(((cell15.Calcite*100.09)/2.71 )/cell15.min_vol_total)*100
    #cell15["Dolomite_abun_vol"]=(((cell15.Dolomite*184.4)/2.85)/cell15.min_vol_total)*100

def data_processing_2(mass_bal_lith):
	#print(smallusgs.head(10))
	#print('medusgs')
	#print(medusgs.head(10))
	#print(massbal)
	print(mass_bal_lith.head(10))
	mass_bal_lith['MIN_VOL_NEW']=mass_bal_lith.tot_min_mixed - mass_bal_lith.tot_min_no_co2
	mass_bal_lith['tot_sim_1_2']=mass_bal_lith.tot_min_mixed_sim_1 + mass_bal_lith.tot_min_mixed_sim_2
	mass_bal_lith['tot_sim_1_2_old']=mass_bal_lith.tot_min_mixed_sim_1_old + mass_bal_lith.tot_min_mixed_sim_2_old

	#mass_bal_lith['tot_sim_1_2_ref']=mass_bal_lith.tot_min_mixed_sim_1_ref + mass_bal_lith.tot_min_mixed_sim_2_ref
	mass_bal_lith['MIN_VOL_NEW_ORD']=mass_bal_lith.tot_min_order - mass_bal_lith.tot_min_order_no_co
	mass_bal_lith['MIN_VOL_NEW_DIS']=mass_bal_lith.tot_min_disorder - mass_bal_lith.tot_min_disorder_no_co
	mass_bal_lith['MIN_VOL_NEW_MAIN']=mass_bal_lith.tot_min_global - mass_bal_lith.tot_min_global_no_co

	mass_bal_lith['net_co2']=mass_bal_lith.d_CO2_mixed_sim_1 + mass_bal_lith.d_CO2_mixed_sim_2
	mass_bal_lith['net_co2_old']=mass_bal_lith.d_CO2_mixed_sim_1_old + mass_bal_lith.d_CO2_mixed_sim_2_old

	mass_bal_lith['min_trap']=(mass_bal_lith.d_Dol_mixed_sim_1*2)+(mass_bal_lith.d_Calcite_mixed_sim_1)+(mass_bal_lith.d_Dol_mixed_sim_2*2)+(mass_bal_lith.d_Calcite_mixed_sim_2)

	print('d_Calcite_vol_mixed_pre_eq average')
	print(mass_bal_lith['d_Calcite_vol_mixed_pre_eq'].describe())

	print('ord')
	print(len(mass_bal_lith.loc[mass_bal_lith['d_Dolomite_ord_no_co']>0]))
	print(len(mass_bal_lith.loc[mass_bal_lith['d_Calcite_ord_no_co']>0]))
	print(len(mass_bal_lith.loc[mass_bal_lith['d_Dolomite_ord_no_co']<0]))
	print(len(mass_bal_lith.loc[mass_bal_lith['d_Calcite_ord_no_co']<0]))

	print('dis')
	print(len(mass_bal_lith.loc[mass_bal_lith['d_Dolomite_disord_no_co']>0]))
	print(len(mass_bal_lith.loc[mass_bal_lith['d_Calcite_disord_no_co']>0]))
	print(len(mass_bal_lith.loc[mass_bal_lith['d_Dolomite_disord_no_co']<0]))
	print(len(mass_bal_lith.loc[mass_bal_lith['d_Calcite_disord_no_co']<0]))

	print('mixed')
	print(len(mass_bal_lith.loc[mass_bal_lith['d_Dol_no_co2']>0]))
	print(len(mass_bal_lith.loc[mass_bal_lith['d_Calcite_no_co2']>0]))
	print(len(mass_bal_lith.loc[mass_bal_lith['d_Dol_no_co2']<0]))
	print(len(mass_bal_lith.loc[mass_bal_lith['d_Calcite_no_co2']<0]))

	print(mass_bal_lith['d_Dol_vol_no_co2'].describe())
	print(mass_bal_lith['d_Calcite_vol_no_co2'].describe())

	print(mass_bal_lith['d_Dol_vol_disord_no_co'].describe())
	print(mass_bal_lith['d_Calcite_vol_disord_no_co'].describe())

	print(mass_bal_lith['d_Dol_vol_ord_no_co'].describe())
	print(mass_bal_lith['d_Calcite_vol_ord_no_co'].describe())


	print('min_vol_change')

	print(mass_bal_lith['tot_min_no_co2'].describe())
	print(mass_bal_lith['tot_min_order_no_co'].describe())
	print(mass_bal_lith['tot_min_disorder_no_co'].describe())
	print(mass_bal_lith['tot_min_mixed'].describe())
	print(mass_bal_lith['tot_min_global'].describe())
	print(mass_bal_lith['tot_min_global_no_co'].describe())





	mass_bal_lith['total_zero']=mass_bal_lith['net_co2'].abs()+mass_bal_lith['min_trap'].abs()



	mass_bal_lith['co_sol_ionic']=mass_bal_lith['d_CO2_mixed'] - mass_bal_lith['d_CO2_no_mineral']
	mass_bal_lith['co_sol_ionic_perc']=(mass_bal_lith['co_sol_ionic']/mass_bal_lith['d_CO2_mixed'])*100
	print(mass_bal_lith['co_sol_ionic_perc'].describe())
	print(mass_bal_lith['co_sol_ionic'].describe())
	#print(mass_bal_lith[['d_CO2_no_mineral','d_CO2_mixed','co_sol_ionic','co_sol_ionic_perc']].head(30))
	#print(mass_bal_lith.loc[(mass_bal_lith['co_sol_ionic_perc']>4)][['FIELD','co_sol_ionic_perc','d_CO2_mixed','d_CO2_no_mineral','d_CO2_mixed_sim_1','tot_sim_1_2','TDS']].head(30))
	print(len(mass_bal_lith.loc[(mass_bal_lith['co_sol_ionic_perc']>2)]))



	mass_bal_lith['co_sol_ionic_ord']=mass_bal_lith['d_CO2_ord'] - mass_bal_lith['d_CO2_no_mineral']
	mass_bal_lith['co_sol_ionic_perc_ord']=(mass_bal_lith['co_sol_ionic_ord']/mass_bal_lith['d_CO2_ord'])*100
	print(mass_bal_lith['co_sol_ionic_perc_ord'].describe())
	print(mass_bal_lith['co_sol_ionic_ord'].describe())
	#print(mass_bal_lith[['d_CO2_no_mineral','d_CO2_ord','co_sol_ionic_ord','co_sol_ionic_perc_ord']].head(30))


	mass_bal_lith['co_sol_ionic_disord']=mass_bal_lith['d_CO2_disord'] - mass_bal_lith['d_CO2_no_mineral']
	mass_bal_lith['co_sol_ionic_perc_disord']=(mass_bal_lith['co_sol_ionic_disord']/mass_bal_lith['d_CO2_disord'])*100
	print(mass_bal_lith['co_sol_ionic_perc_disord'].describe())
	print(mass_bal_lith['co_sol_ionic_disord'].describe())
	#print(mass_bal_lith[['d_CO2_no_mineral','d_CO2_disord','co_sol_ionic_disord','co_sol_ionic_perc_disord']].head(30))


	mass_bal_lith['co_sol_ionic_sim_1']=mass_bal_lith['d_CO2_mixed_sim_1'] - mass_bal_lith['d_CO2_no_mineral_lt_ht_sim_1']
	print(mass_bal_lith[['d_CO2_mixed_sim_1','d_CO2_no_mineral_lt_ht_sim_1','co_sol_ionic_sim_1']])
	mass_bal_lith['co_sol_ionic_sim_1_perc']=(mass_bal_lith['co_sol_ionic_sim_1']/mass_bal_lith['d_CO2_mixed_sim_1'])*100
	print(mass_bal_lith['co_sol_ionic_sim_1_perc'].describe())

	#mass_bal_lith['co_sol_ionic_sim_1']=mass_bal_lith['d_CO2_no_mineral_lt_ht_sim_1'] - mass_bal_lith['d_CO2_mixed_sim_1']
	#mass_bal_lith['co_sol_ionic_sim_1_perc']=(mass_bal_lith['co_sol_ionic_sim_1']/mass_bal_lith['d_CO2_mixed_sim_1'])*100
	#print(mass_bal_lith['co_sol_ionic_sim_1_perc'].describe())
#	print(mass_bal_lith['co_sol_ionic_sim_1'].describe())
	#print(mass_bal_lith[['d_CO2_no_mineral_lt_ht_sim_1','d_CO2_mixed_sim_1','co_sol_ionic_sim_1','co_sol_ionic_sim_1_perc']].head(30))
	print(len(mass_bal_lith.loc[(mass_bal_lith['co_sol_ionic_sim_1_perc']>2)]))



	mass_bal_lith['prop_min_trap']=(mass_bal_lith.min_trap/mass_bal_lith.total_zero)*100
	mass_bal_lith['prop_co_trap']=(mass_bal_lith.net_co2/mass_bal_lith.total_zero)*100
	mass_bal_lith['net_dolomite']=mass_bal_lith.d_Dol_vol_mixed_sim_1+mass_bal_lith.d_Dol_vol_mixed_sim_2
	mass_bal_lith['net_calcite']=mass_bal_lith.d_Calcite_vol_mixed_sim_1+mass_bal_lith.d_Calcite_vol_mixed_sim_2
	mass_bal_lith['dolomite_moles']=mass_bal_lith.d_Dol_mixed_sim_1+mass_bal_lith.d_Dol_mixed_sim_2
	mass_bal_lith['calcite_moles']=mass_bal_lith.d_Calcite_mixed_sim_1+mass_bal_lith.d_Calcite_mixed_sim_2

	mass_bal_lith['net_dolomite_CO2']=mass_bal_lith.d_Dol_mixed_sim_1*2+mass_bal_lith.d_Dol_mixed_sim_2*2
	mass_bal_lith['net_calcite_CO2']=mass_bal_lith.d_Calcite_mixed_sim_1+mass_bal_lith.d_Calcite_mixed_sim_2

	mass_bal_lith['net_calcite_dolomite']= mass_bal_lith['calcite_moles'].abs()/(mass_bal_lith['dolomite_moles'].abs())

	print(mass_bal_lith[['net_calcite_dolomite','dolomite_moles','calcite_moles']].head(10))

	#print(mass_bal_lith.loc[(mass_bal_lith['min_trap']>0)&(mass_bal_lith['net_co2']<0)][['total_zero','net_co2','min_trap','net_dolomite','net_calcite']].head(30))
	print(mass_bal_lith.loc[(mass_bal_lith['tot_sim_1_2']<0)&(mass_bal_lith['net_co2']<0)&(mass_bal_lith['min_trap']>0)][['net_dolomite','net_calcite']].head(30))
	print(len(mass_bal_lith.loc[(mass_bal_lith['tot_sim_1_2']<0)&(mass_bal_lith['net_co2']<0)&(mass_bal_lith['min_trap']>0)]))
	print(len(mass_bal_lith.loc[mass_bal_lith['min_trap']<0]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['min_trap']>0)&(mass_bal_lith['net_co2']>0)]))
	print(mass_bal_lith.loc[(mass_bal_lith['min_trap']>0)&(mass_bal_lith['net_co2']<0)][['prop_co_trap','prop_min_trap']].describe())

	print('caclite vs dolomite')
	print(len(mass_bal_lith.loc[(mass_bal_lith['tot_sim_1_2']<0)&(mass_bal_lith['net_co2']<0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['tot_sim_1_2']<0)&(mass_bal_lith['net_co2']<0)&(mass_bal_lith['net_calcite_dolomite']<2)]))

	print(mass_bal_lith.loc[(mass_bal_lith['min_trap']>0)&(mass_bal_lith['net_co2']<0)][['min_trap','net_co2','prop_co_trap','prop_min_trap']].head(20))

	print(mass_bal_lith[['total_zero','net_co2','min_trap']].head(30))
	#sys.exit()
	print('net co2 net min change')
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_co2']<0)&(mass_bal_lith['tot_sim_1_2']>0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_co2']<0)&(mass_bal_lith['tot_sim_1_2']>0)&(mass_bal_lith['net_calcite']>mass_bal_lith['net_dolomite'])]))
	print(mass_bal_lith.loc[(mass_bal_lith['net_co2']<0)&(mass_bal_lith['tot_sim_1_2']>0)&(mass_bal_lith['net_calcite']>mass_bal_lith['net_dolomite'])][['net_calcite_dolomite']].head(10))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']>0)&(mass_bal_lith['net_calcite']<0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']<0)&(mass_bal_lith['net_calcite']>0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']<0)&(mass_bal_lith['net_calcite']<0)]))



	print(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']>0)&(mass_bal_lith['net_calcite']<0)][['net_calcite_dolomite']].describe())


	print(len(mass_bal_lith.loc[(mass_bal_lith['net_calcite_dolomite']<2)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_calcite_dolomite']>2)]))

	print(mass_bal_lith['net_calcite_dolomite'].describe())
	print(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']>0)&(mass_bal_lith['net_calcite']<0)][['net_calcite_dolomite','net_dolomite','net_calcite']].head(10))
	print('net calcite dolomite positive change')
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']>0)&(mass_bal_lith['net_calcite']<0)&(mass_bal_lith['net_co2']<0)&(mass_bal_lith['tot_sim_1_2']<0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']>0)&(mass_bal_lith['net_calcite']<0)&(mass_bal_lith['net_co2']<0)&(mass_bal_lith['tot_sim_1_2']>0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']<0)&(mass_bal_lith['net_calcite']>0)&(mass_bal_lith['net_co2']<0)&(mass_bal_lith['tot_sim_1_2']>0)]))


	#sys.exit()

	print(mass_bal_lith.loc[(mass_bal_lith['net_co2']<0)&(mass_bal_lith['tot_sim_1_2']>0)][['net_dolomite','net_calcite']])


	print(len(mass_bal_lith.loc[(mass_bal_lith['net_dolomite_CO2']>0)&(mass_bal_lith['tot_sim_1_2']<0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']>0)&(mass_bal_lith['tot_sim_1_2']<0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['dolomite_moles']>0)&(mass_bal_lith['tot_sim_1_2']<0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']>0)&(mass_bal_lith['tot_sim_1_2']<0)&(mass_bal_lith['net_co2']<0)&(mass_bal_lith['min_trap']>0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']>0)&(mass_bal_lith['tot_sim_1_2']<0)&(mass_bal_lith['min_trap']>0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['tot_sim_1_2']<0)&(mass_bal_lith['min_trap']>0)]))
	print(mass_bal_lith.loc[(mass_bal_lith['tot_sim_1_2']<0)&(mass_bal_lith['net_co2']<0)&(mass_bal_lith['min_trap']>0)][['net_dolomite','net_calcite']].head(30))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']>0)&(mass_bal_lith['net_calcite']>0)&(mass_bal_lith['tot_sim_1_2']<0)]))



	print(mass_bal_lith['prop_min_trap'].describe())
	print(mass_bal_lith['prop_co_trap'].describe())

	print('min dissolution stage 1')
	print(len(mass_bal_lith.loc[(mass_bal_lith['tot_min_mixed_sim_1']<0)]))
	print(mass_bal_lith['d_Dol_vol_mixed_sim_1'].describe())
	print(mass_bal_lith['d_Calcite_vol_mixed_sim_1'].describe())

	print('min dissolution stage 2')
	print(len(mass_bal_lith.loc[(mass_bal_lith['tot_min_mixed_sim_2']>0)]))
	print(mass_bal_lith['d_Dol_vol_mixed_sim_2'].describe())
	print(mass_bal_lith['d_Calcite_vol_mixed_sim_2'].describe())




	#print(mass_bal_lith['MIN_VOL_NEW'].describe())
	print('no co vs co')
	print(mass_bal_lith['d_Dol_vol_mixed'].describe())
	print(mass_bal_lith['d_Calcite_vol_mixed'].describe())

	print(mass_bal_lith['d_Dol_vol_no_co2'].describe())
	print(mass_bal_lith['d_Calcite_vol_no_co2'].describe())

	print(mass_bal_lith['d_Dol_vol_global_no_co'].describe())
	print(mass_bal_lith['d_Calcite_vol_global_no_co'].describe())

	print(mass_bal_lith['d_Dol_vol_global'].describe())
	print(mass_bal_lith['d_Calcite_vol_global'].describe())
#
	print(mass_bal_lith['tot_min_no_co2'].describe())
	print(mass_bal_lith['tot_min_mixed'].describe())
	print(mass_bal_lith['tot_min_global'].describe())
	#print(mass_bal_lith['tot_min_order'].describe())
	#print(mass_bal_lith['tot_min_disorder'].describe())
	print(mass_bal_lith['tot_min_global_no_co'].describe())
	#print(mass_bal_lith['tot_min_order_no_co'].describe())
	#print(mass_bal_lith['tot_min_disorder_no_co'].describe())
#
	#print(mass_bal_lith['MIN_VOL_NEW_ORD'].describe())


	#mass_bal_lith['MIN_VOL_NEW_ORD_dol']=mass_bal_lith.d_Dol_vol_ord - mass_bal_lith.d_Dol_vol_ord_no_co
	#mass_bal_lith['MIN_VOL_NEW_DIS_dol']=mass_bal_lith.d_Dol_vol_disord - mass_bal_lith.d_Dol_vol_disord_no_co
	#mass_bal_lith['MIN_VOL_NEW_MAIN_dol']=mass_bal_lith.d_Dol_vol_global - mass_bal_lith.d_Dol_vol_global_no_co
#
	#mass_bal_lith['MIN_VOL_NEW_ORD_cal']=mass_bal_lith.d_Calcite_vol_ord - mass_bal_lith.d_Calcite_vol_ord_no_co
	#mass_bal_lith['MIN_VOL_NEW_DIS_cal']=mass_bal_lith.d_Calcite_vol_disord - mass_bal_lith.d_Calcite_vol_disord_no_co
	#mass_bal_lith['MIN_VOL_NEW_MAIN_cal']=mass_bal_lith.d_Calcite_global - mass_bal_lith.d_Calcite_global_no_co
#
	#print(mass_bal_lith['MIN_VOL_NEW'].describe())
	#print(mass_bal_lith['MIN_VOL_NEW_ORD'].describe())
	#print(mass_bal_lith['MIN_VOL_NEW_DIS'].describe())
	#print(mass_bal_lith['MIN_VOL_NEW_MAIN'].describe())
#
	#print(mass_bal_lith['MIN_VOL_NEW_ORD_dol'].describe())
	#print(mass_bal_lith['MIN_VOL_NEW_DIS_dol'].describe())
	#print(mass_bal_lith['MIN_VOL_NEW_MAIN_dol'].describe())
#
	#print(mass_bal_lith['MIN_VOL_NEW_ORD_cal'].describe())
	#print(mass_bal_lith['MIN_VOL_NEW_DIS_cal'].describe())
	#print(mass_bal_lith['MIN_VOL_NEW_MAIN_cal'].describe())




	mass_bal_lith['score']=np.nan
	#mass_bal_lith.loc[(mass_bal_lith.tot_min_mixed_sim_1_ref < 1)&(mass_bal_lith.tot_min_mixed_sim_2_ref<0),mass_bal_lith.score] = '2'
	#nesson['dif']=((nesson['tot_sim_1_2_ref']-nesson['tot_sim_1_2'])/nesson['tot_sim_1_2'])*100  #
	print(len(mass_bal_lith.loc[mass_bal_lith['tot_min_mixed_sim_2']>=0.5]))
	print(len(mass_bal_lith.loc[mass_bal_lith['tot_min_mixed_sim_2']>=0.4]))
	print(len(mass_bal_lith.loc[mass_bal_lith['tot_min_mixed_sim_2']<=0.4]))



	mass_bal_lith.loc[(mass_bal_lith['tot_min_mixed_sim_1']<0) & (mass_bal_lith['tot_min_mixed_sim_2']<0),'score'] = '0'
	mass_bal_lith.loc[(mass_bal_lith['tot_min_mixed_sim_1']<-1.5) & (mass_bal_lith['tot_min_mixed_sim_2']>0)&(mass_bal_lith['tot_min_mixed_sim_2']<=0.4),'score'] = '1'
	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-1.5)&(mass_bal_lith['tot_min_mixed_sim_1']<-1)) & (mass_bal_lith['tot_min_mixed_sim_2']>0)&(mass_bal_lith['tot_min_mixed_sim_2']<=0.4),'score'] = '2'
	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-1)&(mass_bal_lith['tot_min_mixed_sim_1']<-0.5)) & (mass_bal_lith['tot_min_mixed_sim_2']>0)&(mass_bal_lith['tot_min_mixed_sim_2']<=0.4),'score'] = '3'
	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-0.5)&(mass_bal_lith['tot_min_mixed_sim_1']<0)) & (mass_bal_lith['tot_min_mixed_sim_2']>0)&(mass_bal_lith['tot_min_mixed_sim_2']<=0.4),'score'] = '4'

	mass_bal_lith.loc[(mass_bal_lith['tot_min_mixed_sim_1']<-1.75) & (mass_bal_lith['tot_min_mixed_sim_2']>0.4),'score'] = '5'
	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-1.75)&(mass_bal_lith['tot_min_mixed_sim_1']<-1.5)) & (mass_bal_lith['tot_min_mixed_sim_2']>0.4),'score'] = '6'
	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-1.5)&(mass_bal_lith['tot_min_mixed_sim_1']<-1.25)) & (mass_bal_lith['tot_min_mixed_sim_2']>0.4),'score'] = '7'

	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-1.25)&(mass_bal_lith['tot_min_mixed_sim_1']<-1)) & (mass_bal_lith['tot_min_mixed_sim_2']>0.4),'score'] = '8'
	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-1)&(mass_bal_lith['tot_min_mixed_sim_1']<0)) & (mass_bal_lith['tot_min_mixed_sim_2']>0.4),'score'] = '9'

	mass_bal_lith.loc[mass_bal_lith['tot_min_mixed_sim_1']>=0,'score'] = '10'
	mass_bal_lith['score']=pd.to_numeric(mass_bal_lith['score'])

	print(len(mass_bal_lith.loc[(mass_bal_lith['score']==10)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']<0)&(mass_bal_lith['net_calcite']>0)&(mass_bal_lith['score']==10)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['d_Dol_vol_mixed_sim_1']<0)&(mass_bal_lith['d_Calcite_vol_mixed_sim_1']>0)&(mass_bal_lith['score']==10)]))




	print('class numbers 1')
	print(mass_bal_lith['score'].value_counts())
	print(mass_bal_lith[['score','net_co2']].groupby(['score']).agg('median'))
	print(mass_bal_lith[['net_co2']].describe())



	mass_bal_lith.loc[(mass_bal_lith['tot_min_mixed_sim_1_old']<0) & (mass_bal_lith['tot_min_mixed_sim_2_old']<0),'score_old'] = '0'
	mass_bal_lith.loc[(mass_bal_lith['tot_min_mixed_sim_1_old']<-1.5) & (mass_bal_lith['tot_min_mixed_sim_2_old']>0)&(mass_bal_lith['tot_min_mixed_sim_2_old']<=0.4),'score_old'] = '1'
	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1_old']>=-1.5)&(mass_bal_lith['tot_min_mixed_sim_1_old']<-1)) & (mass_bal_lith['tot_min_mixed_sim_2_old']>0)&(mass_bal_lith['tot_min_mixed_sim_2_old']<=0.4),'score_old'] = '2'
	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1_old']>=-1)&(mass_bal_lith['tot_min_mixed_sim_1_old']<-0.5)) & (mass_bal_lith['tot_min_mixed_sim_2_old']>0)&(mass_bal_lith['tot_min_mixed_sim_2_old']<=0.4),'score_old'] = '3'
	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1_old']>=-0.5)&(mass_bal_lith['tot_min_mixed_sim_1_old']<0)) & (mass_bal_lith['tot_min_mixed_sim_2_old']>0)&(mass_bal_lith['tot_min_mixed_sim_2_old']<=0.4),'score_old'] = '4'

	mass_bal_lith.loc[(mass_bal_lith['tot_min_mixed_sim_1_old']<-1.75) & (mass_bal_lith['tot_min_mixed_sim_2_old']>0.4),'score_old'] = '5'
	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1_old']>=-1.75)&(mass_bal_lith['tot_min_mixed_sim_1_old']<-1.5)) & (mass_bal_lith['tot_min_mixed_sim_2_old']>0.4),'score_old'] = '6'
	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1_old']>=-1.5)&(mass_bal_lith['tot_min_mixed_sim_1_old']<-1.25)) & (mass_bal_lith['tot_min_mixed_sim_2_old']>0.4),'score_old'] = '7'

	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1_old']>=-1.25)&(mass_bal_lith['tot_min_mixed_sim_1_old']<-1)) & (mass_bal_lith['tot_min_mixed_sim_2_old']>0.4),'score_old'] = '8'
	mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1_old']>=-1)&(mass_bal_lith['tot_min_mixed_sim_1_old']<0)) & (mass_bal_lith['tot_min_mixed_sim_2_old']>0.4),'score_old'] = '9'

	mass_bal_lith.loc[mass_bal_lith['tot_min_mixed_sim_1_old']>=0,'score_old'] = '10'
	mass_bal_lith['score_old']=pd.to_numeric(mass_bal_lith['score_old'])

	print(len(mass_bal_lith.loc[(mass_bal_lith['score_old']==10)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_dolomite']<0)&(mass_bal_lith['net_calcite']>0)&(mass_bal_lith['score_old']==10)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['d_Dol_vol_mixed_sim_1_old']<0)&(mass_bal_lith['d_Calcite_vol_mixed_sim_1_old']>0)&(mass_bal_lith['score_old']==10)]))

	mass_bal_lith['score']=mass_bal_lith['score_old']

	print('class numbers 2')

	print(mass_bal_lith[['score','temp']].groupby(['score']).agg('median'))


	print(mass_bal_lith['score_old'].value_counts())
	print(mass_bal_lith[['score_old','net_co2_old']].groupby(['score_old']).agg('median'))
	print(mass_bal_lith[['net_co2_old']].describe())

	print('score numbers')
	print(mass_bal_lith.loc[(mass_bal_lith['score_old']==10)]['score'].value_counts())





	#mass_bal_lith.loc[(mass_bal_lith['tot_min_mixed_sim_1']<0) & (mass_bal_lith['tot_min_mixed_sim_2']<0),'score'] = '0'
	#mass_bal_lith.loc[(mass_bal_lith['tot_min_mixed_sim_1']<-1.5) & (mass_bal_lith['tot_min_mixed_sim_2']>0)&(mass_bal_lith['tot_min_mixed_sim_2']<=0.5),'score'] = '1'
	#mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-1.5)&(mass_bal_lith['tot_min_mixed_sim_1']<-1)) & (mass_bal_lith['tot_min_mixed_sim_2']>0)&(mass_bal_lith['tot_min_mixed_sim_2']<=0.5),'score'] = '2'
	#mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-1)&(mass_bal_lith['tot_min_mixed_sim_1']<-0.5)) & (mass_bal_lith['tot_min_mixed_sim_2']>0)&(mass_bal_lith['tot_min_mixed_sim_2']<=0.5),'score'] = '3'
	#mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-0.5)&(mass_bal_lith['tot_min_mixed_sim_1']<0)) & (mass_bal_lith['tot_min_mixed_sim_2']>0)&(mass_bal_lith['tot_min_mixed_sim_2']<=0.5),'score'] = '4'

	#mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-4)&(mass_bal_lith['tot_min_mixed_sim_1']<-2)) & (mass_bal_lith['tot_min_mixed_sim_2']>0.5),'score'] = '5'
	#mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-2)&(mass_bal_lith['tot_min_mixed_sim_1']<-1.75)) & (mass_bal_lith['tot_min_mixed_sim_2']>0.5),'score'] = '6'
	#mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-1.75)&(mass_bal_lith['tot_min_mixed_sim_1']<-1.5)) & (mass_bal_lith['tot_min_mixed_sim_2']>0.5),'score'] = '7'

	#mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-1.5)&(mass_bal_lith['tot_min_mixed_sim_1']<-1)) & (mass_bal_lith['tot_min_mixed_sim_2']>0.5),'score'] = '8'
	#mass_bal_lith.loc[((mass_bal_lith['tot_min_mixed_sim_1']>=-1)&(mass_bal_lith['tot_min_mixed_sim_1']<0)) & (mass_bal_lith['tot_min_mixed_sim_2']>0.5),'score'] = '9'

	#mass_bal_lith.loc[mass_bal_lith['tot_min_mixed_sim_1']>=0,'score'] = '10'
	#mass_bal_lith['score']=pd.to_numeric(mass_bal_lith['score'])

	class_5=mass_bal_lith.loc[(mass_bal_lith['score']==5) ]
	class_5=class_5[['score','BASIN']].groupby(['BASIN']).agg('count')
	class_6=mass_bal_lith.loc[(mass_bal_lith['score']==6) ]
	class_6=class_6[['score','BASIN']].groupby(['BASIN']).agg('count')
	class_7=mass_bal_lith.loc[(mass_bal_lith['score']==7) ]
	class_7=class_7[['score','BASIN']].groupby(['BASIN']).agg('count')

	class_5_7=mass_bal_lith.loc[(mass_bal_lith['score']>=5)&(mass_bal_lith['score']<=7) ]
	class_5_7=class_5_7[['score','BASIN']].groupby(['BASIN']).agg('count').reset_index()
	class_5_7.columns=['BASIN','count']
	class_5_7=class_5_7.loc[class_5_7['count']>30]
	val_counts=pd.DataFrame(mass_bal_lith['BASIN'].value_counts().reset_index())
	val_counts.columns=['BASIN','count_total']
	class_5_7=class_5_7.merge(val_counts,on=['BASIN'])
	class_5_7['count_perc']=class_5_7['count']/class_5_7['count_total']
	print(class_5_7.sort_values('count_perc'))

	class_5_7=mass_bal_lith.loc[(mass_bal_lith['score']>=5)&(mass_bal_lith['score']<=7) ]
	class_5_7=class_5_7[['score','FORMATION']].groupby(['FORMATION']).agg('count').reset_index()
	class_5_7.columns=['FORMATION','count']
	class_5_7=class_5_7.loc[class_5_7['count']>30]
	val_counts=pd.DataFrame(mass_bal_lith['FORMATION'].value_counts().reset_index())
	val_counts.columns=['FORMATION','count_total']
	class_5_7=class_5_7.merge(val_counts,on=['FORMATION'])
	class_5_7['count_perc']=class_5_7['count']/class_5_7['count_total']
	print(class_5_7.sort_values('count_perc'))



	mass_bal_lith['Dolomite_perc']=(mass_bal_lith['d_Dol_vol_mixed'].abs()/(mass_bal_lith['d_Dol_vol_mixed'].abs()+mass_bal_lith['d_Calcite_vol_mixed'].abs()))*100
	mass_bal_lith['Dolomite_perc_sim_1']=(mass_bal_lith['d_Dol_vol_mixed_sim_1'].abs()/(mass_bal_lith['d_Dol_vol_mixed_sim_1'].abs()+mass_bal_lith['d_Calcite_vol_mixed_sim_1'].abs()))*100
	mass_bal_lith['Dolomite_perc_sim_2']=(mass_bal_lith['d_Dol_vol_mixed_sim_2'].abs()/(mass_bal_lith['d_Dol_vol_mixed_sim_2'].abs()+mass_bal_lith['d_Calcite_vol_mixed_sim_2'].abs()))*100
	mass_bal_lith['Dolomite_perc_sim_1_2']=((mass_bal_lith['d_Dol_vol_mixed_sim_1'].abs()+mass_bal_lith['d_Dol_vol_mixed_sim_2'].abs())/(mass_bal_lith['d_Dol_vol_mixed_sim_1'].abs()+mass_bal_lith['d_Dol_vol_mixed_sim_2'].abs()+mass_bal_lith['d_Calcite_vol_mixed_sim_2'].abs()+mass_bal_lith['d_Calcite_vol_mixed_sim_2'].abs()))*100

	#mass_bal_lith['Dolomite_perc_old']=(mass_bal_lith['d_Dol_vol_mixed_old'].abs()/(mass_bal_lith['d_Dol_vol_mixed_old'].abs()+mass_bal_lith['d_Calcite_vol_mixed_old'].abs()))*100
	mass_bal_lith['Dolomite_perc_sim_1_old']=(mass_bal_lith['d_Dol_vol_mixed_sim_1_old'].abs()/(mass_bal_lith['d_Dol_vol_mixed_sim_1_old'].abs()+mass_bal_lith['d_Calcite_vol_mixed_sim_1_old'].abs()))*100
	mass_bal_lith['Dolomite_perc_sim_2_old']=(mass_bal_lith['d_Dol_vol_mixed_sim_2_old'].abs()/(mass_bal_lith['d_Dol_vol_mixed_sim_2_old'].abs()+mass_bal_lith['d_Calcite_vol_mixed_sim_2_old'].abs()))*100
	mass_bal_lith['Dolomite_perc_sim_1_2_old']=((mass_bal_lith['d_Dol_vol_mixed_sim_1_old'].abs()+mass_bal_lith['d_Dol_vol_mixed_sim_2_old'].abs())/(mass_bal_lith['d_Dol_vol_mixed_sim_1_old'].abs()+mass_bal_lith['d_Dol_vol_mixed_sim_2_old'].abs()+mass_bal_lith['d_Calcite_vol_mixed_sim_2_old'].abs()+mass_bal_lith['d_Calcite_vol_mixed_sim_2_old'].abs()))*100




	print('perc_vol')
	print(mass_bal_lith['d_Dol_vol_mixed_sim_1'].describe())
	print(mass_bal_lith['d_Dol_vol_mixed_sim_2'].describe())
	print(mass_bal_lith['Dolomite_perc'].describe())
	print(mass_bal_lith['Dolomite_perc_sim_1'].describe())
	print(mass_bal_lith['Dolomite_perc_sim_2'].describe())
	print(mass_bal_lith['Dolomite_perc_sim_1_2'].describe())


	print(mass_bal_lith[['Dolomite_perc','d_Dol_vol_mixed','d_Calcite_vol_mixed']].head(20))

	print('score score')
	print(mass_bal_lith['tot_min_mixed_sim_1'].describe())
	print(mass_bal_lith['tot_min_mixed_sim_2'].describe())
	print(mass_bal_lith['score'].describe())
	print(mass_bal_lith['score'].value_counts())


	print('net volume change and net sequester')

	print(len(mass_bal_lith.loc[(mass_bal_lith['net_co2']<0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_co2']<0)&(mass_bal_lith['tot_sim_1_2']<0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['net_co2']<0)&(mass_bal_lith['tot_sim_1_2']>0)]))

	mass_bal_lith.to_csv(data_import.temp+'/co2_sequestration.txt', header=True, index=False, mode='w', sep='\t')

	return mass_bal_lith



def plotting_1(mass_bal_lith):

	xedges=np.arange(-4,4,0.2)
	yedges=np.arange(-4,4,0.2)


	#fig, ax = plt.subplots(figsize=(10,10))
	#X, Y = np.meshgrid(xedges, yedges)
	#ax.pcolormesh(X, Y, H)
	#ax.set_ylim([-4,4])
	#ax.set_xlim([-4,4])
	#plt.savefig(data_import.fig+'/Paper_2/frequency_plot.png',dpi=300)
#
	#PSS_dist=SPSS_dist.groupby([SPSS_dist.temp_phreeqc,SPSS_dist.Log_Ca_Mg]).count()
	#SPSS_dist=SPSS_dist.loc[:,['temp_phreeqc']]
	#SPSS_dist=SPSS_dist.unstack()
	#SPSS_dist = SPSS_dist.xs('temp_phreeqc', axis=1, drop_level=True)

	print('skew dolomite calcite')
	print(stats.skew(mass_bal_lith['d_Dol_vol_mixed']))
	print(stats.skew(mass_bal_lith['d_Calcite_vol_mixed']))
	print(mass_bal_lith['d_Dol_mixed'].describe())
	print(mass_bal_lith['d_Dol_no_co2'].describe())
	print(mass_bal_lith['d_Calcite_no_co2'].describe())


	print(stats.skew(mass_bal_lith['d_Dol_mixed']))
	print(stats.skew(mass_bal_lith['d_Calcite_mixed']))

	print(len(mass_bal_lith.loc[(mass_bal_lith['d_Dol_no_co2']<0)&(mass_bal_lith['d_Calcite_no_co2']>0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['d_Dol_no_co2']>0)&(mass_bal_lith['d_Calcite_no_co2']<0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['d_Dol_no_co2']<0)&(mass_bal_lith['d_Calcite_no_co2']<0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['d_Dol_no_co2']>0)&(mass_bal_lith['d_Calcite_no_co2']>0)]))


	print(len(mass_bal_lith.loc[(mass_bal_lith['d_Dol_mixed']<0)&(mass_bal_lith['d_Calcite_mixed']>0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['d_Dol_mixed']>0)&(mass_bal_lith['d_Calcite_mixed']<0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['d_Dol_mixed']<0)&(mass_bal_lith['d_Calcite_mixed']<0)]))
	print(len(mass_bal_lith.loc[(mass_bal_lith['d_Dol_mixed']>0)&(mass_bal_lith['d_Calcite_mixed']>0)]))



	H1, xedges1, yedges1 = np.histogram2d(mass_bal_lith['d_Dol_vol_ord'],mass_bal_lith['d_Dol_vol_ord_no_co'], bins=(xedges, yedges))
	H2, xedges2, yedges2 = np.histogram2d(mass_bal_lith['d_Calcite_vol_ord'],mass_bal_lith['d_Calcite_vol_ord_no_co'], bins=(xedges, yedges))
	H3, xedges3, yedges3 = np.histogram2d(mass_bal_lith['d_Dol_vol_disord'],mass_bal_lith['d_Dol_vol_disord_no_co'], bins=(xedges, yedges))
	H4, xedges4, yedges4 = np.histogram2d(mass_bal_lith['d_Calcite_vol_disord'],mass_bal_lith['d_Calcite_vol_disord_no_co'], bins=(xedges, yedges))
	H5, xedges5, yedges5 = np.histogram2d(mass_bal_lith['d_Dol_vol_global'],mass_bal_lith['d_Dol_vol_global_no_co'], bins=(xedges, yedges))
	H6, xedges6, yedges6 = np.histogram2d(mass_bal_lith['d_Calcite_vol_global'],mass_bal_lith['d_Calcite_vol_global_no_co'], bins=(xedges, yedges))
	H7, xedges7, yedges7 = np.histogram2d(mass_bal_lith['d_Dol_vol_mixed'],mass_bal_lith['d_Dol_vol_no_co2'], bins=(xedges, yedges))
	H8, xedges8, yedges8 = np.histogram2d(mass_bal_lith['d_Calcite_vol_mixed'],mass_bal_lith['d_Calcite_vol_no_co2'], bins=(xedges, yedges))


	H1a, xedges1a, yedges1a = np.histogram2d(mass_bal_lith['d_Dol_vol_ord_pre_eq'],mass_bal_lith['d_Dol_vol_ord'], bins=(xedges, yedges))
	H2a, xedges2a, yedges2a = np.histogram2d(mass_bal_lith['d_Calcite_vol_ord_pre_eq'],mass_bal_lith['d_Calcite_vol_ord'], bins=(xedges, yedges))
	H3a, xedges3a, yedges3a = np.histogram2d(mass_bal_lith['d_Dol_vol_disord_pre_eq'],mass_bal_lith['d_Dol_vol_disord'], bins=(xedges, yedges))
	H4a, xedges4a, yedges4a = np.histogram2d(mass_bal_lith['d_Calcite_vol_disord_pre_eq'],mass_bal_lith['d_Calcite_vol_disord'], bins=(xedges, yedges))
	H5a, xedges5a, yedges5a = np.histogram2d(mass_bal_lith['d_Dol_vol_global_pre_eq'],mass_bal_lith['d_Dol_vol_global'], bins=(xedges, yedges))
	H6a, xedges6a, yedges6a = np.histogram2d(mass_bal_lith['d_Calcite_vol_global_pre_eq'],mass_bal_lith['d_Calcite_vol_global'], bins=(xedges, yedges))
	H7a, xedges7a, yedges7a = np.histogram2d(mass_bal_lith['d_Dol_vol_mixed_pre_eq'],mass_bal_lith['d_Dol_vol_mixed'], bins=(xedges, yedges))
	H8a, xedges8a, yedges8a = np.histogram2d(mass_bal_lith['d_Calcite_vol_mixed_pre_eq'],mass_bal_lith['d_Calcite_vol_mixed'], bins=(xedges, yedges))

	print('d dol vol pre eq ')
	print(mass_bal_lith['d_Dol_vol_ord_pre_eq'].describe())
	print(mass_bal_lith['d_Dol_vol_disord_pre_eq'].describe())
	print(mass_bal_lith['d_Dol_vol_mixed_pre_eq'].describe())


	H1[H1==0]=np.nan
	H2[H2==0]=np.nan
	H3[H3==0]=np.nan
	H4[H4==0]=np.nan
	H5[H5==0]=np.nan
	H6[H6==0]=np.nan
	H7[H7==0]=np.nan
	H8[H8==0]=np.nan

	H1a[H1a==0]=np.nan
	H2a[H2a==0]=np.nan
	H3a[H3a==0]=np.nan
	H4a[H4a==0]=np.nan
	H5a[H5a==0]=np.nan
	H6a[H6a==0]=np.nan
	H7a[H7a==0]=np.nan
	H8a[H8a==0]=np.nan


	cbar_min = 0#np.min(SPSS_dist.Log_Ca_Mg)
	cbar_max = 300#np.max(SPSS_dist.Log_Ca_Mg)
	cbarlabels=[0,20,40,60,80,100,125,150,175,200,250,300]
	cbarlabels_1=['0','20','40','60','80','100','125','150','175','200','>250','']


	#levels = np.linspace(np.floor(cbar_min), np.ceil(cbar_max), 23) # to draw 35 levels
	norm = colors.BoundaryNorm([0,2,4,6,8,10,15,20,25,30,35,40,60,80,100,125,150,175,200,250,300], 250, clip=True)

	print(xedges1, yedges1)

	X, Y = np.meshgrid(xedges1, yedges1)
	kw = {'hspace':0.05,'wspace':0.2} #

	fig, ax = plt.subplots(nrows=4,ncols=3,sharex=True,sharey=False,figsize=(11,8),gridspec_kw=kw)
	cont1=ax[0][0].pcolormesh(X, Y, H1,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont2=ax[0][1].pcolormesh(X, Y, H2,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont3=ax[1][0].pcolormesh(X, Y, H3,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont4=ax[1][1].pcolormesh(X, Y, H4,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont5=ax[2][0].pcolormesh(X, Y, H5,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont6=ax[2][1].pcolormesh(X, Y, H6,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont7=ax[3][0].pcolormesh(X, Y, H7,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont8=ax[3][1].pcolormesh(X, Y, H8,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)

	cont1a=ax[0][2].pcolormesh(X, Y, H1a,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	#cont2a=ax[0][3].pcolormesh(X, Y, H2a,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont3a=ax[1][2].pcolormesh(X, Y, H3a,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	#cont4a=ax[1][3].pcolormesh(X, Y, H4a,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont5a=ax[2][2].pcolormesh(X, Y, H5a,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	#cont6a=ax[2][3].pcolormesh(X, Y, H6a,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont7a=ax[3][2].pcolormesh(X, Y, H7a,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	#cont8a=ax[3][3].pcolormesh(X, Y, H8a,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)


	#cbar=plt.colorbar(cont2,ax=ax[0][1],pad= 0.01,boundaries=np.linspace(0,300,300))
	#cbar.set_label('No. of Samples', fontsize=12,rotation=270,labelpad=12)
	#cbar.set_ticks(cbarlabels)
	#cbar.set_ticklabels(cbarlabels_1)



	#pos = ax[0][1].get_position()
	#pos2 = ax[1][1].get_position()
	#pos3 = ax[2][1].get_position()
	#pos4 = ax[3][1].get_position()
	#pos5 = ax[0][0].get_position()
	#pos6 = ax[1][0].get_position()
	#pos7 = ax[2][0].get_position()
	#pos8 = ax[3][0].get_position()
#
	#ax[1][1].set_position([pos.x0,pos2.y0,pos.width,pos2.height])
	#ax[2][1].set_position([pos.x0,pos3.y0,pos.width,pos3.height])
	#ax[3][1].set_position([pos.x0,pos4.y0,pos.width,pos4.height])
#
	#ax[0][0].set_position([pos5.x0,pos5.y0,pos.width,pos5.height])
	#ax[1][0].set_position([pos5.x0,pos6.y0,pos.width,pos6.height])
	#ax[2][0].set_position([pos5.x0,pos7.y0,pos.width,pos7.height])
	#ax[3][0].set_position([pos5.x0,pos8.y0,pos.width,pos8.height])


	ax[3][0].set_xlabel('Dolomite min. vol. Δ \n no CO$_{2}$ (cm$^{3}$/kgw)',fontsize=12)
	ax[3][1].set_xlabel('Calcite min. vol Δ \n no CO$_{2}$ (cm$^{3}$/kgw)',fontsize=12)
	ax[3][2].set_xlabel('Dolomite min. vol. Δ with CO$_{2}$ \n (no pre-pertubation) (cm$^{3}$/kgw)',fontsize=12)
	#ax[3][3].set_xlabel('Calcite min. vol Δ with CO$_{2}$ (cm$^{3}$/kgw)',fontsize=12)

	ax[0][0].set_ylabel('Dolomite min. vol. Δ with CO$_{2}$ (cm$^{3}$/kgw)',fontsize=12)
	ax[0][1].set_ylabel('Calcite min. vol Δ with CO$_{2}$ (cm$^{3}$/kgw)',fontsize=12)
	ax[0][2].set_ylabel('Dolomite min. vol. Δ with CO$_{2}$ (pre-pertubation) (cm$^{3}$/kgw)',fontsize=12)
	#ax[0][3].set_ylabel('Calcite min. vol Δ with CO$_{2}$ (pre-pertubation) (cm$^{3}$/kgw)',fontsize=12)
	ax[0][0].yaxis.set_label_coords(-0.11, -1.3)
	ax[0][1].yaxis.set_label_coords(-0.11, -1.3)
	ax[0][2].yaxis.set_label_coords(-0.11, -1.3)


	#ax[1][0].set_ylabel('Dolomite min. vol. Δ \n with CO$_{2}$  (cm$^{3}$/kgw)',fontsize=12)
	#ax[1][1].set_ylabel('Calcite min. vol Δ \n with CO$_{2}$  (cm$^{3}$/kgw)',fontsize=12)
	#ax[2][0].set_ylabel('Dolomite min. vol. Δ \n with CO$_{2}$  (cm$^{3}$/kgw)',fontsize=12)
	#ax[2][1].set_ylabel('Calcite min. vol Δ \n  with CO$_{2}$ (cm$^{3}$/kgw)',fontsize=12)
	#ax[3][0].set_ylabel('Dolomite min. vol. Δ \n with CO$_{2}$  (cm$^{3}$/kgw)',fontsize=12)
	#ax[3][1].set_ylabel('Calcite min. vol Δ \n  with CO$_{2}$ (cm$^{3}$/kgw)',fontsize=12)




	ax[0][0].xaxis.grid(True,zorder=0)
	ax[0][1].xaxis.grid(True,zorder=0)
	ax[1][0].xaxis.grid(True,zorder=0)
	ax[1][1].xaxis.grid(True,zorder=0)
	ax[2][0].xaxis.grid(True,zorder=0)
	ax[2][1].xaxis.grid(True,zorder=0)
	ax[3][0].xaxis.grid(True,zorder=0)
	ax[3][1].xaxis.grid(True,zorder=0)

	ax[0][0].yaxis.grid(True,zorder=0)
	ax[0][1].yaxis.grid(True,zorder=0)
	ax[1][0].yaxis.grid(True,zorder=0)
	ax[1][1].yaxis.grid(True,zorder=0)
	ax[2][0].yaxis.grid(True,zorder=0)
	ax[2][1].yaxis.grid(True,zorder=0)
	ax[3][0].yaxis.grid(True,zorder=0)
	ax[3][1].yaxis.grid(True,zorder=0)


	ax[0][2].xaxis.grid(True,zorder=0)
	#ax[0][3].xaxis.grid(True,zorder=0)
	ax[1][2].xaxis.grid(True,zorder=0)
	#ax[1][3].xaxis.grid(True,zorder=0)
	ax[2][2].xaxis.grid(True,zorder=0)
	#ax[2][3].xaxis.grid(True,zorder=0)
	ax[3][2].xaxis.grid(True,zorder=0)
	#ax[3][3].xaxis.grid(True,zorder=0)

	ax[0][2].yaxis.grid(True,zorder=0)
	#ax[0][3].yaxis.grid(True,zorder=0)
	ax[1][2].yaxis.grid(True,zorder=0)
	#ax[1][3].yaxis.grid(True,zorder=0)
	ax[2][2].yaxis.grid(True,zorder=0)
	#ax[2][3].yaxis.grid(True,zorder=0)
	ax[3][2].yaxis.grid(True,zorder=0)
	#ax[3][3].yaxis.grid(True,zorder=0)



	fig.tight_layout()
	plt.savefig(data_import.fig+'/Paper_2/frequency_plot_new_v2.png',dpi=300)
	plt.savefig(data_import.fig+'/Paper_2/frequency_plot_new_v2.tiff', format='TIFF',dpi=300,bbox_inches='tight')


	#xedges=np.arange(-3,1,0.005)
	#yedges=np.arange(-3,1,0.005)
	#H9[H9==0]=np.nan
	#H9, xedges9, yedges9 = np.histogram2d(mass_bal_lith['d_CO2_mixed'],mass_bal_lith['d_CO2_no_mineral'], bins=(xedges, yedges))
	#X, Y = np.meshgrid(xedges9, yedges9)
#
	#fig, ax = plt.subplots(figsize=(10,10))
	#cont1=ax.pcolormesh(X, Y, H9,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	#fig.tight_layout()
	#plt.savefig(data_import.fig+'/Paper_2/co2_vs_ionic.png',dpi=300)




	#yedges_2=np.arange(-3,2,0.05)
	#xedges_2=np.arange(-1,2.5,0.05)
	#H2, xedges2, yedges2 = np.histogram2d(mass_bal_lith['tot_min_mixed_sim_2'],mass_bal_lith['tot_min_mixed_sim_1'], bins=(xedges_2,yedges_2))
	#H2[H2==0]=np.nan
	#X2, Y2 = np.meshgrid(yedges2, xedges2)


	yedges=np.arange(0,13,0.2)
	xedges=np.arange(-2,1,0.05)
	H0, xedges0, yedges0 = np.histogram2d(mass_bal_lith['tot_min_mixed_pre_eq'],mass_bal_lith['mu'], bins=(xedges, yedges))
	H0[H0==0]=np.nan
	X0, Y0 = np.meshgrid(yedges0, xedges0)

	fig, ax = plt.subplots(figsize=(6.5,3))
	cont1=ax.pcolormesh(Y0, X0, H0,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	fig.tight_layout()
	ax.xaxis.grid(True,zorder=0)
	ax.yaxis.grid(True,zorder=0)
	cbar=plt.colorbar(cont1,ax=ax,pad= 0.01,boundaries=np.linspace(0,300,300))
	cbar.set_label('No. of Samples', fontsize=12,rotation=270,labelpad=12)
	cbar.set_ticks(cbarlabels)
	cbar.set_ticklabels(cbarlabels_1)
	ax.set_ylabel('Ionic strength (mol/kgw)',fontsize=12)
	ax.set_xlabel('Min. vol. Δ (cm$^{3}$/kgw)',fontsize=12,labelpad=3)#(Stage 1)

	plt.savefig(data_import.fig+'/Paper_2/ionic_vs_min_vol_change_pre_eq.png',dpi=300,bbox_inches='tight')
	plt.savefig(data_import.fig+'/Paper_2/ionic_vs_min_vol_change_pre_eq.tiff', format='TIFF',dpi=300,bbox_inches='tight')




	yedges=np.arange(0,13,0.2)
	xedges=np.arange(-3,0,0.05)
	H1, xedges1, yedges1 = np.histogram2d(mass_bal_lith['d_CO2_mixed_pre_eq'],mass_bal_lith['mu'], bins=(xedges, yedges))
	H1[H1==0]=np.nan
	X1, Y1 = np.meshgrid(yedges1, xedges1)

	yedges=np.arange(0,150,2.5)
	xedges=np.arange(-3,0,0.05)
	H2, xedges2, yedges2 = np.histogram2d(mass_bal_lith['d_CO2_mixed_pre_eq'],mass_bal_lith['temp'], bins=(xedges, yedges))
	H2[H2==0]=np.nan
	X2, Y2 = np.meshgrid(yedges2, xedges2)

	mass_bal_lith['Depth']=mass_bal_lith['Depth']*-1
	yedges=np.arange(-6,0,0.075)
	xedges=np.arange(-3,0,0.05)
	H3, xedges3, yedges3 = np.histogram2d(mass_bal_lith['d_CO2_mixed_pre_eq'],mass_bal_lith['Depth'], bins=(xedges, yedges))
	H3[H3==0]=np.nan
	X3, Y3 = np.meshgrid(yedges3, xedges3)


	kw = {'hspace':0.1,'wspace':0.1} #

	fig, ax = plt.subplots(nrows=3,sharex=True,figsize=(8,9),gridspec_kw=kw)

	cont1=ax[0].pcolormesh(Y1, X1, H1,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont2=ax[1].pcolormesh(Y2, X2, H2,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont3=ax[2].pcolormesh(Y3, X3, H3,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)

	ax[1].set_ylim([150,0])
	ax[2].set_xlim([-2,0])

	ax[0].set_ylabel('Ionic strength (mol/kgw)',fontsize=12)
	ax[1].set_ylabel('Temperature (°C)' ,fontsize=12)
	ax[2].set_ylabel('Depth (km)' ,fontsize=12)
	ax[2].set_xlabel('Δ CO$_{2}$ (mol/kgw)' ,fontsize=12)

	ax[0].xaxis.grid(True,zorder=0)
	ax[1].xaxis.grid(True,zorder=0)
	ax[2].xaxis.grid(True,zorder=0)

	ax[0].yaxis.grid(True,zorder=0)
	ax[1].yaxis.grid(True,zorder=0)
	ax[2].yaxis.grid(True,zorder=0)


	fig.tight_layout()
	plt.savefig(data_import.fig+'/Paper_2/co2_vs_ionic_pre_eq.tiff', format='TIFF',dpi=300,bbox_inches='tight')
	plt.savefig(data_import.fig+'/Paper_2/co2_vs_ionic_pre_eq.png',dpi=300,bbox_inches='tight')


	#fig, ax = plt.subplots(figsize=(10,10))
	#fig.tight_layout()
	#plt.savefig(data_import.fig+'/Paper_2/co2_vs_temp.png',dpi=300)
#
	##print(mass_bal_lith['Depth'].head(10))
#
	#fig, ax = plt.subplots(figsize=(10,10))
	#fig.tight_layout()
	#plt.savefig(data_import.fig+'/Paper_2/co2_vs_depth.png',dpi=300)





	#kw = {'height_ratios':[3,8],'hspace':0.025}
	#fig, ax = plt.subplots(nrows=4,ncols=2,sharex=True,sharey=False,figsize=(10,16))
#
	#mass_bal_lith.plot(kind='scatter',y='d_Dol_vol_ord',x='d_Dol_vol_ord_no_co',c='black',s=3,ax=ax[0][0],zorder=2,label='Ordered Dolomite',marker='^')
	#mass_bal_lith.plot(kind='scatter',y='d_Calcite_vol_ord',x='d_Calcite_vol_ord_no_co',c='black',s=3,ax=ax[0][1],zorder=2,label='Ordered Dolomite',marker='^')
	#mass_bal_lith.plot(kind='scatter',y='d_Dol_vol_disord',x='d_Dol_vol_disord_no_co',c='black',s=3,ax=ax[1][0],zorder=2,label='Disordered Dolomite',marker='^')
	#mass_bal_lith.plot(kind='scatter',y='d_Calcite_vol_disord',x='d_Calcite_vol_disord_no_co',c='black',s=3,ax=ax[1][1],zorder=2,label='Disordered Dolomite',marker='^')
	#mass_bal_lith.plot(kind='scatter',y='d_Dol_vol_global',x='d_Dol_vol_global_no_co',c='black',s=3,ax=ax[2][0],zorder=2,label='Model J23',marker='^')
	#mass_bal_lith.plot(kind='scatter',y='d_Calcite_vol_global',x='d_Calcite_vol_global_no_co',c='black',s=3,ax=ax[2][1],zorder=2,label='Model J23',marker='^')
	#mass_bal_lith.plot(kind='scatter',y='d_Dol_vol_mixed',x='d_Dol_vol_no_co2',c='black',s=3,ax=ax[3][0],zorder=2,label='Model J23 - Local Dolomite',marker='^')
	#mass_bal_lith.plot(kind='scatter',y='d_Calcite_vol_mixed',x='d_Calcite_vol_no_co2',c='black',s=3,ax=ax[3][1],zorder=2,label='Model J23 - Local Dolomite',marker='^')
#
	#ax[0][0].set_ylim([-4,4])
	#ax[1][0].set_ylim([-4,4])
	#ax[2][0].set_ylim([-4,4])
	#ax[3][0].set_ylim([-4,4])
	#ax[0][1].set_ylim([-4,4])
	#ax[1][1].set_ylim([-4,4])
	#ax[2][1].set_ylim([-4,4])
	#ax[3][1].set_ylim([-4,4])
	#ax[3][0].set_xlim([-4,4])
	#ax[3][1].set_xlim([-4,4])
	#ax[3][0].set_xlabel('Change dolomite volume - No CO$_{2}$ \n (cm$^{3}$/kgw)')
	#ax[3][1].set_xlabel('Change calcite volume - No CO$_{2}$ \n (cm$^{3}$/kgw)')
#
	#ax[0][0].set_ylabel('Change dolomite volume - with CO$_{2}$ \n (cm$^{3}$/kgw)')
	#ax[0][1].set_ylabel('Change calcite volume - with CO$_{2}$ \n (cm$^{3}$/kgw)')
	#ax[1][0].set_ylabel('Change dolomite volume - with CO$_{2}$ \n (cm$^{3}$/kgw)')
	#ax[1][1].set_ylabel('Change calcite volume - with CO$_{2}$ \n (cm$^{3}$/kgw)')
	#ax[2][0].set_ylabel('Change dolomite volume - with CO$_{2}$ \n (cm$^{3}$/kgw)')
	#ax[2][1].set_ylabel('Change calcite volume - with CO$_{2}$ \n (cm$^{3}$/kgw)')
	#ax[3][0].set_ylabel('Change dolomite volume - with CO$_{2}$ \n (cm$^{3}$/kgw)')
	#ax[3][1].set_ylabel('Change calcite volume - with CO$_{2}$ \n (cm$^{3}$/kgw)')
#
	#ax[0][0].xaxis.grid(True,zorder=0)
	#ax[0][1].xaxis.grid(True,zorder=0)
	#ax[1][0].xaxis.grid(True,zorder=0)
	#ax[1][1].xaxis.grid(True,zorder=0)
	#ax[2][0].xaxis.grid(True,zorder=0)
	#ax[2][1].xaxis.grid(True,zorder=0)
	#ax[3][0].xaxis.grid(True,zorder=0)
	#ax[3][1].xaxis.grid(True,zorder=0)
#
	#ax[0][0].yaxis.grid(True,zorder=0)
	#ax[0][1].yaxis.grid(True,zorder=0)
	#ax[1][0].yaxis.grid(True,zorder=0)
	#ax[1][1].yaxis.grid(True,zorder=0)
	#ax[2][0].yaxis.grid(True,zorder=0)
	#ax[2][1].yaxis.grid(True,zorder=0)
	#ax[3][0].yaxis.grid(True,zorder=0)
	#ax[3][1].yaxis.grid(True,zorder=0)
#
#
	#fig.tight_layout()
	#plt.savefig(data_import.fig+'/Paper_2/d_Cal_vs_d_dol.png',dpi=300)




def plotting_2(mass_bal_lith):

	#Tot min vol _ dol co2


	#old converted
	mass_bal_lith['tot_min_mixed_sim_1'] = mass_bal_lith['tot_min_mixed_sim_1_old']
	mass_bal_lith['tot_min_mixed_sim_2'] = mass_bal_lith['tot_min_mixed_sim_2_old']
	mass_bal_lith['d_CO2_mixed_sim_1'] = mass_bal_lith['d_CO2_mixed_sim_1_old']
	mass_bal_lith['d_CO2_mixed_sim_2'] = mass_bal_lith['d_CO2_mixed_sim_2_old']
	mass_bal_lith['Dolomite_perc_sim_1'] = mass_bal_lith['Dolomite_perc_sim_1_old']
	mass_bal_lith['Dolomite_perc_sim_2'] = mass_bal_lith['Dolomite_perc_sim_2_old']
	mass_bal_lith['net_co2'] = mass_bal_lith['net_co2_old']
	mass_bal_lith['tot_sim_1_2'] = mass_bal_lith['tot_sim_1_2_old']
	mass_bal_lith['score']=mass_bal_lith['score_old']


	mass_bal_lith['d_Calcite_vol_mixed_sim_1']=mass_bal_lith['d_Calcite_vol_mixed_sim_1_old']
	mass_bal_lith['d_Dol_vol_mixed_sim_1']=mass_bal_lith['d_Dol_vol_mixed_sim_1_old']
	mass_bal_lith['d_Calcite_vol_mixed_sim_2']=mass_bal_lith['d_Calcite_vol_mixed_sim_2_old']
	mass_bal_lith['d_Dol_vol_mixed_sim_2']=mass_bal_lith['d_Dol_vol_mixed_sim_2_old']
	mass_bal_lith['tot_min_mixed_sim_2']=mass_bal_lith['tot_min_mixed_sim_2_old']
	mass_bal_lith['tot_min_mixed_sim_1']=mass_bal_lith['tot_min_mixed_sim_1_old']







	xedges_7=np.arange(-5,5,0.05)
	yedges_7=np.arange(-5,5,0.05)
	H7, xedges7, yedges7 = np.histogram2d(mass_bal_lith['d_CO2_mixed_sim_1'],mass_bal_lith['tot_min_mixed_sim_1'], bins=(xedges_7,yedges_7))
	H7[H7==0]=np.nan
	X7, Y7 = np.meshgrid(yedges7, xedges7)

	xedges_8=np.arange(-5,5,0.05)
	yedges_8=np.arange(-5,5,0.05)
	H8, xedges8, yedges8 = np.histogram2d(mass_bal_lith['d_CO2_mixed_sim_2'],mass_bal_lith['tot_min_mixed_sim_2'], bins=(xedges_8,yedges_8))
	H8[H8==0]=np.nan
	X8, Y8 = np.meshgrid(yedges8, xedges8)

	xedges_5=np.arange(0,105,2.5)
	yedges_5=np.arange(-5,5,0.05)
	H5, xedges5, yedges5 = np.histogram2d(mass_bal_lith['Dolomite_perc_sim_1'],mass_bal_lith['tot_min_mixed_sim_1'], bins=(xedges_5,yedges_5))
	H5[H5==0]=np.nan
	X5, Y5 = np.meshgrid(yedges5, xedges5)

	xedges_6=np.arange(0,105,2.5)
	yedges_6=np.arange(-5,5,0.05)
	H6, xedges6, yedges6 = np.histogram2d(mass_bal_lith['Dolomite_perc_sim_2'],mass_bal_lith['tot_min_mixed_sim_2'], bins=(xedges_6,yedges_6))
	H6[H6==0]=np.nan
	X6, Y6 = np.meshgrid(yedges6, xedges6)

	xedges_10=np.arange(-3,2,0.05)
	yedges_10=np.arange(-2,2,0.05)
	H10, xedges10, yedges10 = np.histogram2d(mass_bal_lith['net_co2'],mass_bal_lith['tot_sim_1_2'], bins=(xedges_10,yedges_10))
	print(H10)
	H10[H10==0]=np.nan
	X10, Y10 = np.meshgrid(yedges10,xedges10)



	cbar_min = 0#np.min(SPSS_dist.Log_Ca_Mg)
	cbar_max = 300#np.max(SPSS_dist.Log_Ca_Mg)
	cbarlabels=[0,20,40,60,80,100,125,150,175,200,250,300]
	cbarlabels_1=['0','20','40','60','80','100','125','150','175','200','>250','']


	#levels = np.linspace(np.floor(cbar_min), np.ceil(cbar_max), 23) # to draw 35 levels
	norm = colors.BoundaryNorm([0,2,4,6,8,10,15,20,25,30,35,40,60,80,100,125,150,175,200,250,300], 250, clip=True)
	#norm = colors.BoundaryNorm([0,2,4,6,8,10,12,14,16,18,20,25,30,35,40,50,60,70,  80,90, 100,120,140,160,180,200], 200, clip=True)


	kw = {'width_ratios':[1,1,2],'hspace':0.07,'wspace':0.1} #
	fig, ax = plt.subplots(nrows=2,ncols=3,sharex='col',sharey='row',figsize=(10,5),gridspec_kw=kw)
	cont7=ax[1][0].pcolormesh(X7, Y7, H7,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont8=ax[1][1].pcolormesh(X8, Y8, H8,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont10=ax[1][2].pcolormesh(X10, Y10, H10,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)  #<- to figure A
	cont5=ax[0][0].pcolormesh(X5, Y5, H5,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont6=ax[0][1].pcolormesh(X6, Y6, H6,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)

	ax[1][0].set_ylim([-2,1])
	#ax[0][0].set_ylim([-2.1,0.5])
	ax[1][0].set_xlim([-2.3,2])
	#ax[0][1].set_ylim([-0.5,0.8])
	ax[1][1].set_xlim([-0.8,2])
	#ax[1][1].set_xlim([-1,3])
	ax[1][2].set_xlim([-2,1.8])

	ax[0][0].set_ylabel('Dolomite % of min. vol. Δ ',fontsize=12) #(Stage 1)
	#ax[1][1].set_ylabel('Dolomite % of min. vol. Δ ',fontsize=12)#(Stage 2)
	ax[1][0].set_ylabel('Δ CO$_{2}$ (mol/kgw)',fontsize=12)#(Stage 1)
	#ax[0][1].set_ylabel('Δ CO$_{2}$ (mol/kgw)',fontsize=12)#(Stage 2)
	ax[1][0].set_xlabel('Min. vol. Δ (cm$^{3}$/kgw)',fontsize=12,labelpad=3)#(Stage 1)
	ax[1][1].set_xlabel('Min. vol. Δ (cm$^{3}$/kgw)',fontsize=12,labelpad=3)#(Stage 2)
	ax[1][2].set_xlabel('Min. vol. Δ (cm$^{3}$/kgw)',fontsize=12,labelpad=3)

	#ax[0][0].set_xlabel('Total min. vol. Δ (cm$^{3}$/kgw)',fontsize=12)#(Stage 1)
	#ax[0][1].set_xlabel('Total min. vol. Δ (cm$^{3}$/kgw)',fontsize=12)#(Stage 2)
	ax[1][0].xaxis.grid(True,zorder=0)
	ax[1][1].xaxis.grid(True,zorder=0)
	ax[0][0].xaxis.grid(True,zorder=0)
	ax[0][1].xaxis.grid(True,zorder=0)
	ax[1][2].xaxis.grid(True,zorder=0)

	ax[1][0].yaxis.grid(True,zorder=0)
	ax[1][1].yaxis.grid(True,zorder=0)
	ax[0][0].yaxis.grid(True,zorder=0)
	ax[0][1].yaxis.grid(True,zorder=0)
	ax[1][2].yaxis.grid(True,zorder=0)
	ax[0][2].xaxis.set_label_position('top')

	fig.tight_layout()
	plt.savefig(data_import.fig+'/Paper_2/plot_a_dist.png',dpi=300)
	plt.savefig(data_import.fig+'/Paper_2/plot_a_dist.tiff', format='TIFF',dpi=300,bbox_inches='tight')


	xedges=np.arange(0,102.5,2.5)
	yedges=np.arange(0,102.5,2.5)
	H1, xedges1, yedges1 = np.histogram2d(mass_bal_lith['Dolomite_perc_sim_2'],mass_bal_lith['Dolomite_perc_sim_1'], bins=(xedges, yedges))
	H1[H1==0]=np.nan
	X, Y = np.meshgrid(xedges1, yedges1)

	kw = {'width_ratios':[1,1,2],'hspace':0.07,'wspace':0.1} #4
	fig, ax = plt.subplots(nrows=2,ncols=3,sharex=False,sharey='row',figsize=(10,5),gridspec_kw=kw)
	cont1=ax[0][2].pcolormesh(X, Y, H1,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	ax[0][2].set_yticks([0,20,40,60,80,100])
	ax[0][2].set_ylabel('Stage 2',fontsize=12)
	ax[0][2].set_xlabel('(Stage 1) Dolomite % of min. vol. Δ ',fontsize=12)
	ax[0][2].yaxis.grid(True,zorder=0)
	ax[0][2].xaxis.grid(True,zorder=0)
	ax[0][2].xaxis.set_label_position('top')
	ax[0][2].xaxis.tick_top()
	plt.savefig(data_import.fig+'/Paper_2/plot_b_dist.png',dpi=300)
	plt.savefig(data_import.fig+'/Paper_2/plot_b_dist.tiff', format='TIFF',dpi=300,bbox_inches='tight')




	xedges_13=np.arange(-3,3,0.05)
	yedges_13=np.arange(-3,3,0.05)
	H13, xedges13, yedges13 = np.histogram2d(mass_bal_lith['d_Calcite_vol_mixed_sim_1'],mass_bal_lith['d_Dol_vol_mixed_sim_1'], bins=(xedges_13,yedges_13))
	H13[H13==0]=np.nan
	X13, Y13 = np.meshgrid(yedges13, xedges13)

	xedges_14=np.arange(-2,2.5,0.05)
	yedges_14=np.arange(-3,2.5,0.05)
	H14, xedges14, yedges14 = np.histogram2d(mass_bal_lith['d_Calcite_vol_mixed_sim_2'],mass_bal_lith['d_Dol_vol_mixed_sim_2'], bins=(xedges_14,yedges_14))
	H14[H14==0]=np.nan
	X14, Y14 = np.meshgrid(yedges14, xedges14)

	yedges_2=np.arange(-2.5,2.1,0.05)
	xedges_2=np.arange(-0.7,1.7,0.05)
	H2, xedges2, yedges2 = np.histogram2d(mass_bal_lith['tot_min_mixed_sim_2'],mass_bal_lith['tot_min_mixed_sim_1'], bins=(xedges_2,yedges_2))
	H2[H2==0]=np.nan
	X2, Y2 = np.meshgrid(yedges2, xedges2)



	kw = {'width_ratios':[1,1,2],'hspace':0.1,'wspace':0.05} #4
	fig, ax = plt.subplots(nrows=1,ncols=3,sharex=False,sharey=True,figsize=(9,3.5),gridspec_kw=kw)
	cont13=ax[0].pcolormesh(X13, Y13, H13,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont14=ax[1].pcolormesh(X14, Y14, H14,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	cont2=ax[2].pcolormesh(X2, Y2, H2,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	ax[0].set_xlabel('Dolomite min. vol. Δ (cm$^{3}$/kgw)',fontsize=12)
	ax[1].set_xlabel('',fontsize=12)
	ax[0].set_ylabel('Calcite min. vol. Δ (cm$^{3}$/kgw)',fontsize=12)
	ax[2].set_ylabel('')
	ax[0].xaxis.set_label_coords(1.05, -0.1)
	ax[0].xaxis.grid(True,zorder=0)
	ax[1].xaxis.grid(True,zorder=0)
	ax[2].xaxis.grid(True,zorder=0)
	ax[0].yaxis.grid(True,zorder=0)
	ax[1].yaxis.grid(True,zorder=0)
	ax[2].yaxis.grid(True,zorder=0)

	plt.savefig(data_import.fig+'/Paper_2/plot_c_dist.png',dpi=300,bbox_inches='tight')
	plt.savefig(data_import.fig+'/Paper_2/plot_c_dist.tiff', format='TIFF',dpi=300,bbox_inches='tight')


	kw = {'width_ratios':[1,1,2],'hspace':0.13,'wspace':0.4} #4
	fig, ax = plt.subplots(nrows=1,ncols=3,sharex=False,sharey=False,figsize=(9,3.5),gridspec_kw=kw)
	cont2=ax[2].pcolormesh(X2, Y2, H2,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	ax[2].set_ylabel('(Stage 2) Min. vol. Δ (cm$^{3}$/kgw) ',fontsize=12)
	ax[2].set_xlabel('(Stage 1) Min. vol. Δ (cm$^{3}$/kgw) ',fontsize=12)

	cbar=plt.colorbar(cont2,ax=ax[2],pad= 0.01,boundaries=np.linspace(0,300,300))
	cbar.set_label('No. of Samples', fontsize=12,rotation=270,labelpad=10)
	cbar.set_ticks(cbarlabels)
	cbar.set_ticklabels(cbarlabels_1)
	plt.savefig(data_import.fig+'/Paper_2/plot_d_dist.png',dpi=300,bbox_inches='tight')
	plt.savefig(data_import.fig+'/Paper_2/plot_d_dist.tiff', format='TIFF',dpi=300,bbox_inches='tight')


	yedges_3=np.arange(0,105,2.5)
	xedges_3=np.arange(0,11,0.5)
	H3, xedges3, yedges3 = np.histogram2d(mass_bal_lith['score'],mass_bal_lith['Dolomite_perc_sim_1_2'], bins=(xedges_3,yedges_3))
	print(H3)
	H3[H3==0]=np.nan
	X3, Y3 = np.meshgrid(yedges3,xedges3)

	yedges_4=np.arange(-3,2.4,0.1)
	xedges_4=np.arange(0,11,0.5)
	H4, xedges4, yedges4 = np.histogram2d(mass_bal_lith['score'],mass_bal_lith['tot_sim_1_2'], bins=(xedges_4,yedges_4))
	H4[H4==0]=np.nan
	X4, Y4 = np.meshgrid(yedges4, xedges4)

	yedges_16=np.arange(-2.15,-1.70	,0.0075)
	xedges_16=np.arange(0,11,0.5)
	H16, xedges16, yedges16 = np.histogram2d(mass_bal_lith['score'],mass_bal_lith['RI_J21'], bins=(xedges_16,yedges_16))
	H16[H16==0]=np.nan
	X16, Y16 = np.meshgrid(yedges16, xedges16)


	yedges_9=np.arange(-2,0,0.1)
	xedges_9=np.arange(0,11,0.5)
	H9, xedges9, yedges9 = np.histogram2d(mass_bal_lith['score'],mass_bal_lith['net_co2'], bins=(xedges_9,yedges_9))
	print(H9)
	H9[H9==0]=np.nan
	X9, Y9 = np.meshgrid(yedges9,xedges9)




	bin_median, bin_edges, binnumber= stats.binned_statistic(mass_bal_lith['score'], mass_bal_lith['Dolomite_perc_sim_1_2'], statistic=np.nanmedian, bins=np.arange(0,12,1))
	bin_width = (bin_edges[1] - bin_edges[0])
	bin_centers = (bin_edges[1:] - bin_width/2)-0.25

	bins_dol_perc=pd.DataFrame({'bin_median':bin_median,'bin_centers':bin_centers})
	bin_median, bin_edges, binnumber= stats.binned_statistic(mass_bal_lith['score'], mass_bal_lith['tot_sim_1_2'], statistic=np.nanmedian, bins=np.arange(0,12,1))
	bins_tot_sim_1_2=pd.DataFrame({'bin_median':bin_median,'bin_centers':bin_centers})
	bin_median, bin_edges, binnumber= stats.binned_statistic(mass_bal_lith['score'], mass_bal_lith['RI_J21'], statistic=np.nanmedian, bins=np.arange(0,12,1))
	bin_RI_J21=pd.DataFrame({'bin_median':bin_median,'bin_centers':bin_centers})
	bin_median, bin_edges, binnumber= stats.binned_statistic(mass_bal_lith['score'], mass_bal_lith['net_co2'], statistic=np.nanmedian, bins=np.arange(0,12,1))
	bin_net_co2=pd.DataFrame({'bin_median':bin_median,'bin_centers':bin_centers})



	#PLOT MEDIAN VALUES

	kw = {'width_ratios':[1,1,1,1],'hspace':0.3,'wspace':0.05} #4
	fig, ax = plt.subplots(nrows=1,ncols=4,sharex=False,sharey=True,figsize=(10,4),gridspec_kw=kw)
	ax[0].pcolormesh(X3, Y3, H3,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	ax[1].pcolormesh(X4, Y4, H4,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	ax[2].pcolormesh(X9, Y9, H9,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	ax[3].pcolormesh(X16, Y16, H16,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
	ax0=ax[0].twiny()
	ax1=ax[1].twiny()
	ax2=ax[2].twiny()
	ax3=ax[3].twiny()

	bins_dol_perc.plot(x='bin_median',y='bin_centers',ax=ax0,label='',c='k',linestyle='dotted',marker='*')
	bins_tot_sim_1_2.plot(x='bin_median',y='bin_centers',ax=ax1,label='Median',c='k',linestyle='dotted',marker='*')
	bin_net_co2.plot(x='bin_median',y='bin_centers',ax=ax2,label='',c='k',linestyle='dotted',marker='*')
	bin_RI_J21.plot(x='bin_median',y='bin_centers',ax=ax3,label='',c='k',linestyle='dotted',marker='*')


	ax[0].set_ylim([0,105])
	ax[1].set_ylim([-3,2.5])
	ax[2].set_ylim([2,0.01])




	ax0.set_xlim(ax[0].get_xlim())
	ax1.set_xlim(ax[1].get_xlim())
	ax2.set_xlim(ax[2].get_xlim())
	ax3.set_xlim(ax[3].get_xlim())



	#ax0.set_yticks([])
	#ax1.set_yticks([])
	#ax2.set_yticks([])
	#ax3.set_yticks([])

	ax[0].tick_params(axis='y',which='minor',left=False, labelleft=False, top=False, labeltop=False,
                   right=False, labelright=True, bottom=False, labelbottom=False)
	ax[1].tick_params(axis='y',which='minor',left=False, labelleft=False, top=False, labeltop=False,
                   right=False, labelright=True, bottom=False, labelbottom=False)
	ax[2].tick_params(axis='y',which='minor',left=False, labelleft=False, top=False, labeltop=False,
                   right=False, labelright=True, bottom=False, labelbottom=False)
	ax[3].tick_params(axis='y',which='minor',left=False, labelleft=False, top=False, labeltop=False,
                   right=False, labelright=True, bottom=False, labelbottom=False)

	ax0.tick_params(axis='both',which='both',left=False, labelleft=False, top=False, labeltop=False,
                   right=False, labelright=False, bottom=False, labelbottom=False)
	ax1.tick_params(axis='both',which='both',left=False, labelleft=False, top=False, labeltop=False,
                   right=False, labelright=False, bottom=False, labelbottom=False)
	ax2.tick_params(axis='both',which='both',left=False, labelleft=False, top=False, labeltop=False,
                   right=False, labelright=False, bottom=False, labelbottom=False)
	ax3.tick_params(axis='both',which='both',left=False, labelleft=False, top=False, labeltop=False,
                   right=False, labelright=False, bottom=False, labelbottom=False)

	ax[0].set_xlabel('Dolomite % of \n min. vol. Δ' ,fontsize=12)
	ax[1].set_xlabel('Min. vol. Δ (cm$^{3}$/kgw)', fontsize=12)
	ax[2].set_xlabel('Δ CO$_{2}$ (mol/kgw)' ,fontsize=12)
	ax[3].set_xlabel('RI - model J21' ,fontsize=12)

	ax0.set_xlabel('')
	ax1.set_xlabel('')
	ax2.set_xlabel('')
	ax3.set_xlabel('')


	ax0.get_legend().remove()
	ax1.legend(loc=3, ncol=1, fancybox=True, framealpha=1, shadow=False, borderpad=0.1, fontsize=12,bbox_to_anchor = (0.34,0.76),labelspacing=0.02)
	ax2.get_legend().remove()
	ax3.get_legend().remove()


	ax[0].set_ylim([10.5,-0.5])
	ax[0].set_yticks([0.25,1.25,2.25,3.25,4.25,5.25,6.25,7.25,8.25,9.25,10.25])
	ax[0].set_yticklabels(['Class A','Class B','Class C','Class D','Class E','Class F','Class G','Class H','Class I','Class J','Class K'],rotation=35,ha="right",  fontsize=12, rotation_mode="anchor")
	ax[0].xaxis.grid(True,zorder=0)
	ax[1].xaxis.grid(True,zorder=0)
	ax[2].xaxis.grid(True,zorder=0)
	ax[3].xaxis.grid(True,zorder=0)



	plt.savefig(data_import.fig+'/Paper_2/plot_e_dist.png',dpi=300,bbox_inches='tight')
	plt.savefig(data_import.fig+'/Paper_2/plot_e_dist.tiff', format='TIFF',dpi=300,bbox_inches='tight')










#	sys.exit()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#	#bin_means, bin_edges, binnumber= stats.binned_statistic(mass_bal_lith[''], mass_bal_lith['net_co2'], statistic='median', bins=np.arange(-3,1,0.1))
#	#print(bin_means)
#	#print(bin_edges)
#
#
#	#print(bin_means)
#	#print(bin_edges)
#
#
#
#
#	print(bins)
#
#	xedges_11=np.arange(-2.05,-1.80,0.0025)
#	yedges_11=np.arange(-3,1,0.1)
#	H11, xedges11, yedges11 = np.histogram2d(mass_bal_lith['RI_J21'],mass_bal_lith['net_co2'], bins=(xedges_11,yedges_11))
#	print(H11)
#	H11[H11==0]=np.nan
#
#	X11, Y11 = np.meshgrid(yedges11,xedges11)
#
#	print(mass_bal_lith['net_dolomite'].describe())
#
#	xedges_12=np.arange(-1,1,0.02)
#	yedges_12=np.arange(-1,1,0.02)
#	H12, xedges12, yedges12 = np.histogram2d(mass_bal_lith['net_dolomite'],mass_bal_lith['net_calcite'], bins=(xedges_12,yedges_12))
#	H12[H12==0]=np.nan
#	X12, Y12 = np.meshgrid(yedges12, xedges12)
#
#
#
#
#
#	xedges_15=np.arange(-2.05,-1.80,0.0025)
#	yedges_15=np.arange(-2,2,0.05)
#	H15, xedges15, yedges15 = np.histogram2d(mass_bal_lith['RI_J21'],mass_bal_lith['tot_sim_1_2'], bins=(xedges_15,yedges_15))
#	H15[H15==0]=np.nan
#	X15, Y15 = np.meshgrid(yedges15, xedges15)
#
#
#
#
#	min_vol_change=pd.DataFrame({'moles_calcite':np.arange(-4,4,0.01),'moles_dolomite':np.arange(-4,4,0.01)})
#	min_vol_change['moles_calcite_equal']=min_vol_change['moles_dolomite']*1.75184
#	min_vol_change['calcite_vol_equal']=(min_vol_change['moles_calcite_equal']*100.09)/2.71
#	min_vol_change['dolomite_vol']=(min_vol_change['moles_dolomite']*184.4)/2.85
#
#
#
#
#	#xedges_5=np.arange(0,10,1)
#	#yedges_5=np.arange(0,100,5)
#	#H5, xedges5, yedges5 = np.histogram2d(mass_bal_lith['Dolomite_perc_sim_2'],mass_bal_lith['score'], bins=(xedges_5,yedges_5))
#	#H5[H5==0]=np.nan
#	#X5, Y5 = np.meshgrid(xedges5, yedges5)
#
#	print(np.nanmax(H1))
#	print(np.nanmax(H2))
#	print(np.nanmax(H3))
#	print(np.nanmax(H4))
#	print(np.nanmax(H5))
#	print(np.nanmax(H6))
#
#	cont12=ax[4][1].pcolormesh(X12, Y12, H12,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
#
#	min_vol_change.plot(x='calcite_vol_equal',y='dolomite_vol',ax=ax[4][1])
#
#	cont11=ax[5][1].pcolormesh(X11, Y11, H11,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
#
#
#	cont14=ax[7][0].pcolormesh(X15, Y15, H15,cmap='jet', vmin=cbar_min, vmax=cbar_max, norm=norm)
#
#
#
#	ax[0][1].set_xlim([-3,2])
#	ax[0][1].set_ylim([-0.5,2.5])
#
#	ax[4][1].set_xlim([-1,1])
#	ax[4][1].set_ylim([-1,1])
#
#
#
#
#
#	ax[1][0].set_xlim([0,11])
#	ax[1][1].set_xlim([0,11])
#
#	ax[1][0].set_xticks([0.25,1.25,2.25,3.25,4.25,5.25,6.25,7.25,8.25,9.25,10.25])
#	ax[1][0].set_xticklabels(['Class A','Class B','Class C','Class D','Class E','Class F','Class G','Class H','Class I','Class J','Class K'],rotation=35,ha="right",  rotation_mode="anchor")
#	ax[1][1].set_xticks([0.25,1.25,2.25,3.25,4.25,5.25,6.25,7.25,8.25,9.25,10.25])
#	ax[1][1].set_xticklabels(['Class A','Class B','Class C','Class D','Class E','Class F','Class G','Class H','Class I','Class J','Class K'],rotation=35,ha="right",  rotation_mode="anchor")
#
#	ax[1][0].set_yticks([0,20,40,60,80,100])
#	ax[1][1].set_yticks([0,20,40,60,80,100])
#	ax[2][0].set_yticks([0,20,40,60,80,100])
#	ax[2][1].set_yticks([0,20,40,60,80,100])
#
#	#cbar=plt.colorbar(cont1,ax=ax[0][1],pad= 0.01,boundaries=np.linspace(0,300,300))
#	#cbar.set_label('No. of Samples', fontsize=12,rotation=270,labelpad=12)
#	#cbar.set_ticks(cbarlabels)
#	#cbar.set_ticklabels(cbarlabels_1)
#
#	ax[1][0].set_ylabel('(Stage 1) Dolomite % of min. vol. Δ ',fontsize=12)
#	ax[1][1].set_ylabel('(Stage 2) Dolomite % of min. vol. Δ ',fontsize=12)
#
#	#ax[1][0].set_xlabel('Class',fontsize=12)
#	#ax[1][1].set_xlabel('Class',fontsize=12)
#
#
#
#	ax[1][0].yaxis.grid(True,zorder=0)
#	ax[1][1].yaxis.grid(True,zorder=0)
#	ax[4][1].yaxis.grid(True,zorder=0)
#
#	fig.tight_layout()
#	plt.savefig(data_import.fig+'/Paper_2/distribution_plot.png',dpi=300)
#
#
#	sys.exit()
#
#
#	fig, ax = plt.subplots(figsize=(10,10))
#
#	mass_bal_lith.plot(kind='scatter',y='Dolomite_perc_sim_1',x='Dolomite_perc_sim_2',c='black',s=19,ax=ax,zorder=2,label='All samples',marker='^')
#	ax.set_ylim([0,100])
#	ax.set_xlim([0,100])
#	fig.tight_layout()
#
#	plt.savefig(data_import.fig+'/Paper_2/Dolomite_perc_sim_1_2.png',dpi=300)
#
#
#	fig, ax = plt.subplots(figsize=(10,10))
#
#	mass_bal_lith.plot(kind='scatter',y='Dolomite_perc_sim_1',x='score',c='black',s=19,ax=ax,zorder=2,label='All samples',marker='^')
#	ax.set_ylim([0,100])
#	ax.set_xlim([-1,11])
#	fig.tight_layout()
#
#	plt.savefig(data_import.fig+'/Paper_2/Dolomite_perc_sim_1_score_all.png',dpi=300)
#
#	fig, ax = plt.subplots(figsize=(10,10))
#
#	mass_bal_lith.plot(kind='scatter',y='Dolomite_perc_sim_2',x='score',c='black',s=19,ax=ax,zorder=2,label='All samples',marker='^')
#	ax.set_xlim([-1,11])
#	fig.tight_layout()
#
#	plt.savefig(data_import.fig+'/Paper_2/Dolomite_perc_sim_2_score_all.png',dpi=300)
#
#
#	fig, ax = plt.subplots(figsize=(10,10))
#
#	mass_bal_lith.plot(kind='scatter',y='Dolomite_perc',x='tot_min_mixed_sim_1',c='black',s=19,ax=ax,zorder=2,label='All samples',marker='^')
#	ax.set_ylim([0,100])
#	ax.set_xlim([-5,5])
#	fig.tight_layout()
#
#	plt.savefig(data_import.fig+'/Paper_2/min_vol_dolomite.png',dpi=300)
#








def data_processing_3(mass_bal_lith):
	#question is best wya to present this data??
	#Williston_basin   Area - Madison thickness
	#North Tioga 47701986m2   - 560
	#Tioga 100237763m2   - 690
	#Beaver lodge 90871479m2   - 760
	#Capa 30193296            - 820
	#Charlson 66161969m2      - 860
	#Keene 15070583m2         - 860 #same as charlson as adjacent
	#Antelope 46189588m2      - 990
	#Blue Buttes 59244197m2   - 970
	#Perm basin
	#Yellowhouse 37261883m2
	#S Yellowhouse 9936334m2
	#Levelland 729706300m2
	#Slaughter 461965566m2
	#East Goldsmith 36185829m2
	#Foster 87469883m2
	#South Cowden 130383553m2
	#big area
	#centraL_PLAtform 16684324997m2
	#perm_shelf 35737788759
	#FORMATION
	#Grayburg 59
	#San Andres 352
	#Glorieta 117
	#Wolfcamp 59
	#Devonian 176
	#Ellenburger 293
	#Arkla
	#N_L_SALT_BASIN 20657586052m2
	#n_l_shelf      16289831675m2
	#Total area =   41682770156
	#FORMATION
	#Tuscaloosa = 305
	#Cotton valley = 1219
	#Smackover = 140



	#assume 20%  of volume is liquid and convert m3 to l
	#Willston - Volumes - Madison
	North_Tioga = 47701986 * 560 * 0.2 * 1000
	Tioga = 100237763 * 690 * 0.2 * 1000
	Beaver_lodge = 90871479 * 760  * 0.2 * 1000
	Capa = 30193296 * 820 * 0.2
	Charlson = 66161969 * 860  * 0.2
	Keene = 15070583 * 860 * 0.2  #same as charlson as adjacent
	Antelope = 46189588 * 990 * 0.2
	Blue_Buttes = 59244197 * 970  * 0.2

	#for i in list(mass_bal_lith.columns.values):
	#	print(i)

	#print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Tioga, North'])
	#print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Tioga, North'][['tot_min_mixed','d_Calcite_vol_mixed','d_Dol_vol_mixed','DepthID','RI','Log_KSP']])
	#print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Tioga, North'][['tot_min_global','d_Calcite_vol_global','d_Dol_vol_global','DepthID','RI','Log_KSP']])
	#print(mass_bal_lith.loc[mass_bal_lith.DepthID=='BLANK'][['tot_min_global','tot_min_mixed','d_Calcite_vol_global','d_Dol_vol_global','DepthID','RI','Log_KSP']])


	#print(mass_bal_lith.sort_values('MIN_VOL_NEW').tail(20)[['MIN_VOL_NEW','tot_min_no_co2','tot_min_mixed','d_Calcite_vol_mixed','d_Dol_vol_mixed','d_CO2_mixed']])
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Tioga, North'][['tot_min_no_co2','tot_min_mixed','MIN_VOL_NEW','tot_min_global','tot_min_order','tot_min_disorder','tot_min_mixed_sim_1','tot_min_mixed_sim_2']])
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Tioga, North'][['d_Calcite_vol_no_co2','d_Calcite_vol_mixed','d_Calcite_vol_global','d_Calcite_vol_ord','d_Calcite_vol_disord','d_Calcite_vol_mixed_sim_1','d_Calcite_vol_mixed_sim_2']])
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Tioga, North'][['d_Dol_vol_no_co2','d_Dol_vol_mixed','d_Dol_vol_global','d_Dol_vol_ord','d_Dol_vol_disord','d_Dol_vol_mixed_sim_1','d_Dol_vol_mixed_sim_2']])
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Tioga, North'][['d_CO2_mixed','d_CO2_global','d_CO2_ord','d_CO2_disord','d_CO2_mixed_sim_1','d_CO2_mixed_sim_2']])

	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Tioga, North'][['d_Calcite_mixed','d_Calcite_global','d_Calcite_ord','d_Calcite_disord']])
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Tioga, North'][['d_Dol_mixed','d_Dolomite_global','d_Dolomite_ord','d_Dolomite_disord']])

	sys.exit()


	print('Yellowhouse')
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Yellowhouse'][['tot_min_no_co2','tot_min_mixed','MIN_VOL_NEW','tot_min_global','tot_min_order','tot_min_disorder','tot_min_mixed_sim_1','tot_min_mixed_sim_2']])
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Yellowhouse'][['d_Calcite_vol_no_co2','d_Calcite_vol_mixed','d_Calcite_vol_global','d_Calcite_vol_ord','d_Calcite_vol_disord','d_Calcite_vol_mixed_sim_1','d_Calcite_vol_mixed_sim_2']])
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Yellowhouse'][['d_Dol_vol_no_co2','d_Dol_vol_mixed','d_Dol_vol_global','d_Dol_vol_ord','d_Dol_vol_disord','d_Dol_vol_mixed_sim_1','d_Dol_vol_mixed_sim_2']])
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Yellowhouse'][['d_CO2_mixed','d_CO2_global','d_CO2_ord','d_CO2_disord','d_CO2_mixed_sim_1','d_CO2_mixed_sim_2']])

	#Willston anticline
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Tioga, North'][['tot_min_mixed']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Beaver Lodge'][['tot_min_mixed']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Capa'][['tot_min_mixed']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Charlson'][['tot_min_mixed']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Keene'][['tot_min_mixed']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Antelope'][['tot_min_mixed']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Blue Buttes'][['tot_min_mixed']].mean())

	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Tioga, North'][['tot_sim_1_2']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Beaver Lodge'][['tot_sim_1_2']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Capa'][['tot_sim_1_2']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Charlson'][['tot_sim_1_2']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Keene'][['tot_sim_1_2']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Antelope'][['tot_sim_1_2']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Blue Buttes'][['tot_sim_1_2']].mean())

	print('permian')
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Yellowhouse'][['tot_min_no_co2','tot_min_mixed']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Levelland'][['tot_min_no_co2','tot_min_mixed']].mean())
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Slaughter'][['tot_min_no_co2','tot_min_mixed']].mean())

	sys.exit()

	print(mass_bal_lith.loc[(mass_bal_lith.d_CO2_mixed<0)&(mass_bal_lith.tot_min_mixed>0)&(mass_bal_lith.tot_min_no_co2<mass_bal_lith.tot_min_mixed)][['tot_min_no_co2','tot_min_mixed','d_Calcite_vol_mixed','d_Dol_vol_mixed','d_CO2_mixed']])
	print(mass_bal_lith.loc[mass_bal_lith.d_CO2_mixed==mass_bal_lith.d_CO2_mixed.min()][['tot_min_mixed','d_Calcite_vol_mixed','d_Dol_vol_mixed','d_CO2_mixed']])

	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Tioga, North'][['tot_min_no_co2','tot_min_mixed','tot_min_global','tot_min_order','tot_min_disorder']])

	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Tioga, North'][['d_CO2_mixed','d_CO2_global','d_CO2_ord','d_CO2_disord']])
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Yellowhouse'][['tot_min_no_co2','tot_min_mixed','tot_min_global','tot_min_order','tot_min_disorder']])
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Yellowhouse'][['tot_min_no_co2','d_Calcite_vol_no_co2','d_Dol_vol_no_co2']])
	print(mass_bal_lith.loc[mass_bal_lith.FIELD=='Yellowhouse'][['tot_min_mixed','d_Calcite_vol_mixed','d_Dol_vol_mixed','d_CO2_mixed','DepthID','RI','Log_KSP']])

	mass_bal_lith.loc[mass_bal_lith.FIELD_x=='Tioga']
	mass_bal_lith.loc[mass_bal_lith.FIELD_x=='Beaver Lodge']
	mass_bal_lith.loc[mass_bal_lith.FIELD_x=='Capa']
	mass_bal_lith.loc[mass_bal_lith.FIELD_x=='Charlson']
	mass_bal_lith.loc[mass_bal_lith.FIELD_x=='Keene']
	mass_bal_lith.loc[mass_bal_lith.FIELD_x=='Antelope']
	mass_bal_lith.loc[mass_bal_lith.FIELD_x=='Blue Buttes']

	#Arkla
	all_area_tuscaloosa =  41682770156 * 305  * 0.2
	all_area_cotton_valley =   41682770156 * 1219   * 0.2
	all_area_smackover =  41682770156 * 140 * 0.2

	#permian basin

def co2_vs_min(mass_bal_lith):

	#mass_bal_lith['d_Cal_Dol']=mass_bal_lith
	#
	#cols = ['Carbonate', 'Quartz', 'Matrix']
	#for col in cols:
    #	df[col[0]] = df[col] * 100 / df[cols].sum(axis=1)

	mass_bal_lith['MIN_VOL_NEW']=mass_bal_lith.tot_min_mixed - mass_bal_lith.tot_min_no_co2
	mass_bal_lith['DOL_VOL_NEW']=mass_bal_lith.d_Calcite_vol_mixed - mass_bal_lith.d_Calcite_vol_no_co2
	mass_bal_lith['CAL_VOL_NEW']=mass_bal_lith.d_Dol_vol_mixed - mass_bal_lith.d_Dol_vol_no_co2

	mass_bal_lith['MIN_VOL_NEW']=mass_bal_lith.tot_min_mixed - mass_bal_lith.tot_min_no_co2
	mass_bal_lith['DOL_VOL_NEW']=mass_bal_lith.d_Calcite_vol_mixed - mass_bal_lith.d_Calcite_vol_no_co2
	mass_bal_lith['CAL_VOL_NEW']=mass_bal_lith.d_Dol_vol_mixed - mass_bal_lith.d_Dol_vol_no_co2


	#comparison to baseline equilibration - co2 generally causes mineral dissolution
	fig,ax = plt.subplots(nrows=2,ncols=2,sharex=True,sharey=True,figsize=(10,10)) #gridspec_kw=kw
	mass_bal_lith.plot(ax=ax[0][0],kind='scatter',x='d_CO2_mixed',y='MIN_VOL_NEW') #
	mass_bal_lith.plot(ax=ax[0][1],kind='scatter',x='d_CO2_mixed',y='DOL_VOL_NEW') #
	mass_bal_lith.plot(ax=ax[1][0],kind='scatter',x='d_CO2_mixed',y='CAL_VOL_NEW') #
	mass_bal_lith.plot(ax=ax[1][1],kind='scatter',x='d_CO2_mixed',y='MIN_VOL_NEW') #

	ax[1][1].set_xlim([-0.2,0.2])


	plt.savefig('/Users/hamish/Documents/AWSprojects/fig/Paper_2/MIN_VOL_NEW.png')


	fig,ax = plt.subplots(nrows=2,ncols=2,sharex=True,sharey=True,figsize=(10,10)) #gridspec_kw=kw
	mass_bal_lith.plot(ax=ax[0][0],kind='scatter',x='d_CO2_mixed',y='tot_min_mixed') #
	mass_bal_lith.plot(ax=ax[0][1],kind='scatter',x='d_CO2_global',y='tot_min_global') #
	mass_bal_lith.plot(ax=ax[1][0],kind='scatter',x='d_CO2_ord',y='tot_min_order') #
	mass_bal_lith.plot(ax=ax[1][1],kind='scatter',x='d_CO2_disord',y='tot_min_disorder') #

	ax[1][1].set_xlim([-0.1,0.05])
	ax[1][1].set_ylim([-2.5,2.5])

	plt.savefig('/Users/hamish/Documents/AWSprojects/fig/Paper_2/CO2_min.png')

	fig,ax = plt.subplots(nrows=2,ncols=2,sharex=True,sharey=True,figsize=(10,10)) #gridspec_kw=kw
	mass_bal_lith.plot(ax=ax[0][0],kind='scatter',x='d_Calcite_vol_mixed',y='d_Dol_vol_mixed',c='red') #
	mass_bal_lith.plot(ax=ax[0][1],kind='scatter',x='d_Calcite_vol_global',y='d_Dol_vol_global',c='blue') #
	mass_bal_lith.plot(ax=ax[1][0],kind='scatter',x='d_Calcite_vol_ord',y='d_Dol_vol_ord',c='green') #
	mass_bal_lith.plot(ax=ax[1][1],kind='scatter',x='d_Calcite_vol_disord',y='d_Dol_vol_disord',c='black') #

	plt.savefig('/Users/hamish/Documents/AWSprojects/fig/Paper_2/dol_cal.png')






def main(smallusgs,medusgs,user_job):

	carb_co2_pre_eq = read_in(user_job)
	#mass_bal_lith=data_processing_1(carb,carb_co2,main_dolomite,order_dolomite,disorder_dolomite,sim_1,sim_2,sim_pre,sim_1_ref,sim_2_ref,dis_dolomite_no_co,ord_dolomite_no_co,main_dolomite_no_co,C02_no_mineral,low_temp_high_temp_no_min_sim_1,low_temp_high_temp_no_min_sim_2,initial,carb_co2_pre_eq,main_dolomite_pre_eq,order_dolomite_pre_eq,disorder_dolomite_pre_eq,sim_1_old,sim_2_old,smallusgs,medusgs)

	#mass_bal_lith=pd.read_csv(data_import.temp+'/pre_co2_sequestration.txt', header=0,  sep='\t') #pre_co2_sequestration_v2
	#mass_bal_lith=data_processing_2(mass_bal_lith)
	#mass_bal_lith=data_processing_3(mass_bal_lith)
	#plotting_1(mass_bal_lith)
	#plotting_2(mass_bal_lith)
	#co2_vs_min(mass_bal_lith)

	#calcite_sr_ca_mg(mgcalith)
if __name__ == "__main__":
	main()
