import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

co2_results='/Users/hamish/github/co2_gasp/co2_results'

def plot_3_columns(D_T):


	kw = {'width_ratios':[1.5,2,2],'hspace':0.01}

	fig, ax = plt.subplots(ncols=3,figsize=(6,5),gridspec_kw=kw,sharey=True)#,gridspec_kw=kw

	D_T_PLOT=D_T.plot(x='temp_cel',y='Depth',ax=ax[0],color='grey') # label='Temperature (°C)'
	D_T_PLOT.fill_betweenx(D_T['Depth'],D_T['temp_min'],D_T['temp_max'],alpha=0.1,color='grey')

	D_T_PLOT_2=D_T.plot(x='co2_den',y='Depth',ax=ax[1],c='grey')
	D_T_PLOT_2.fill_betweenx(D_T['Depth'],D_T['co2_den_min'],D_T['co2_den_max'],alpha=0.3,color='grey')

	D_T_PLOT_3=D_T.plot(x='co2_state',y='Depth',ax=ax[2],c='grey')
	D_T_PLOT_3.fill_betweenx(D_T['Depth'],D_T['co2_state_min'],D_T['co2_state_max'],alpha=0.3,color='grey')

	ax[0].get_legend().remove()
	ax[1].get_legend().remove()
	ax[2].get_legend().remove()

	ax[0].yaxis.grid(True,zorder=0)
	ax[1].yaxis.grid(True,zorder=0)
	ax[2].yaxis.grid(True,zorder=0)

	ax[2].set_xlim([-0.5,5.5])
	ax[2].set_xticks([0,1,2,3,4,5])
	ax[2].set_xticklabels(['Liquid','Sc. fluid','Sc. gas','Sc. liquid','Gas', 'Two phase'],rotation=45,ha="right",  fontsize=11, rotation_mode="anchor")
	ax[0].set_ylabel('Depth (m)')
	ax[0].set_xlabel('Temperature (°C)')
	ax[1].set_xlabel('Δ CO$_{2}$ (mol/kgw)')
	ax[2].set_xlabel('')

	ax[0].text(30,-1500,'%.1f + %.1f °C/km'%(D_T['Sur'][0],D_T['Grad'][0]),size=11,rotation=-70)

	fig.tight_layout()
	plt.savefig(co2_results+'/D_T_plot.tiff',format='TIFF',dpi=300,bbox_inches='tight')


def main(D_T):
	plot_3_columns(D_T)


if __name__ == '__main__':
	main()
