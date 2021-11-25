import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from file_paths import geochemical_result

def plot_2d_slice(merge_out,user_job):
	merge_out=merge_out[(merge_out.tonne_co2 > 0)]

	merge_out['Depth']=merge_out['Depth']*-1
	merge_out['change_vol_pc']=merge_out['change_vol_pc']*100
	fig, ax1 = plt.subplots(figsize=(6,5))
	merge_out.plot(kind='scatter',x='change_vol_pc',y='Depth',ax=ax1)
	ax1.set_ylabel('Depth (km)')
	ax1.set_xlabel('Volume change from original (%)')
	fig.tight_layout()
	plt.savefig(geochemical_result+'/'+user_job+'/change_vol_pc.png',format='png',dpi=200,bbox_inches='tight')

	merge_out['tonne_co2_mil']=merge_out['tonne_co2']/1000000
	merge_out['tonne_co2_euros_mil']=merge_out['tonne_co2_euros']/1000000

	print(merge_out['tonne_co2_mil'].head(20))
	print(merge_out['tonne_co2_euros_mil'].head(20))

	fig, ax2 = plt.subplots(figsize=(6,5))
	merge_out.plot(kind='scatter',x='tonne_co2_euros_mil',y='Depth',ax=ax2)
	ax2.set_ylabel('Depth (km)')
	ax2.set_xlabel('Value of total storable CO₂ (million $)')
	fig.tight_layout()
	plt.savefig(geochemical_result+'/'+user_job+'/value_of_storable_co2.png',format='png',dpi=200,bbox_inches='tight')

	fig, ax3 = plt.subplots(figsize=(6,5))
	merge_out.plot(kind='scatter',x='tonne_co2_mil',y='Depth',ax=ax3)
	ax3.set_ylabel('Depth (km)')
	ax3.set_xlabel('Total storable CO₂ (million tonnes)')
	fig.tight_layout()
	plt.savefig(geochemical_result+'/'+user_job+'/volume_of_storable_co2.png',format='png',dpi=200,bbox_inches='tight')



def main(merge_out,user_job):
	plot_2d_slice(merge_out,user_job)


if __name__ == '__main__':
	main()
