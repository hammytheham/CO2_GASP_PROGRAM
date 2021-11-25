import os
import numpy as np
import pandas as pd
import sys


def subsetting_pressure(medusgs):
	print('medusgs.head')
	print(medusgs.head(10))
	medusgs.to_csv('medusgs.csv')
	pw=(1+(42745*0.695e-6))*1000 #kg/m3

	medusgs['pressure']=(medusgs['Depth']*1000 * 9.81 * pw)/101325  #used to be 2700 for lithostatic pressure
	print(medusgs.columns.values)

	medusgs['Temp']=medusgs['TEMP']
	smallusgs=medusgs.loc[:,['TemperatureSMU','LITHOLOGY','PH','Temp',
	       'B', 'Ba',
	       'Br', 'CO2', 'CO3', 'HCO3', 'Ca', 'Cl',
	       'FeTot','FeIII','FeII','FeS',
	       'I', 'K', 'Li', 'Mg', 'Mn',
	       'Na',
	       'Pb', 'S', 'SO3', 'SO4', 'HS', 'H2S',
	       'Si', 'Zn','pressure']].copy()
	smallusgs['C(4)']= smallusgs.fillna(0).CO2 + smallusgs.fillna(0).CO3 + smallusgs.fillna(0).HCO3 #is hco3 correct?
	#look at S(6) is this correct and valid? acidity generating potential of suphide
	smallusgs['S(6)']= smallusgs.fillna(0).S + smallusgs.fillna(0).SO3 + smallusgs.fillna(0).SO4 + smallusgs.fillna(0).HS + smallusgs.fillna(0).H2S
	smallusgs['Fe']= smallusgs.fillna(0).FeTot + smallusgs.fillna(0).FeIII + smallusgs.fillna(0).FeII + smallusgs.fillna(0).FeS

	smallusgs.Temp[:] = 25  # include PHT IF AVAIL?
	smallusgs['ID']=0
	for i in range(len(smallusgs)):
	    smallusgs.loc[i,'ID']=int(i+1)
	smallusgs = smallusgs[['ID','LITHOLOGY','PH','Temp',
	       'B', 'Ba','C(4)',
	       'Ca', 'Cl','Fe',
	       'I', 'K', 'Li', 'Mg', 'Na',
	       'S(6)', 'Si','pressure']]
	smallusgs=smallusgs.rename(columns={'PH': 'pH'})
	smallusgs=smallusgs.fillna(0)[:]
	#print(smallusgs.head(10))
	#smallusgs = smallusgs.rename(columns={'ID': 'Number','LITHOLOGY':'Description'}) #for modelliong purposes - may have depreciated
	return smallusgs

def experi_pressure(smallusgs,medusgs):
	experi1 = pd.DataFrame(medusgs.TemperatureSMU).copy()
	experi1 = experi1.rename(columns={'TemperatureSMU': 'Temperature'})
	#experi['Sol']=smallusgs.ID
	experi1['ID']=smallusgs.ID
	experi1['pressure']=smallusgs.pressure
	print(experi1.head(10))
	tempnchem=pd.merge(smallusgs,experi1)
	#tempnchem.to_csv(data_import.temp+'/tempnchem_new_gradient_pressure.txt', header=True, index=False, mode='w', sep='\t')
	return tempnchem,experi1


def main(medusgs):
	smallusgs=subsetting_pressure(medusgs)
	tempnchem,experi1 = experi_pressure(smallusgs,medusgs)
	return smallusgs,tempnchem,experi1

if __name__ == "__main__":
	main()
