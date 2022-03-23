from flask import Flask, render_template, redirect, request, url_for, session
import boto3
from config import S3_KEY, S3_SECRET, S3_BUCKET
from data_input import Data_input,Data_input_geochem, Index_page,Constant_page, Index_page, Download,PhreeqcOptions,volume_to_mole
import sys
from data_import import boto3_download_results, boto3_upload_csv
#Geochemical code
import data_import
import data_import_2
from carbon_capture import main as carbon_capture_MAIN
from CO2_density_state import main as CO2_density_state_MAIN
from dolomite_constant import main as dolomite_constant_MAIN
from co2_gasp_run_options import *     #import the option file from within the same folder
from redis import Redis
from rq import Queue
from rq.job import Job
from worker import conn
import time
from random import randint
import json
import os
from simple_job import main as simple_Main
from file_paths import co2_results, geochemical_result, directory
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY']=S3_SECRET
#s3_resource = boto3.resource("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)

app.config['EXPLAIN_TEMPLATE_LOADING'] = True
#app.config['FLASKS3_BUCKET_NAME'] = 'co-2-gasp-bucket'

q = Queue(connection=conn)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dolomite_constant',methods=['GET','POST'])
def home_constant():
    data=Constant_page()
    if request.method == 'POST':
        result=request.form.to_dict()
        print(result)
        #print(data.user_file)        print(request.files)
        file_to_upload = request.files['user_file']
        filename=secure_filename(file_to_upload.filename)
        boto3_upload_csv('temp/INPUT_DATA/input_water_chem_data/'+filename)
        user_data=pd.read_csv(file_to_upload,sep='\t')
        print(user_data.head(10))
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        job = q.enqueue(dolomite_constant_MAIN, args=(rawusgs, grad, sur,user_data,result['US_DATA'], result['NEW_TEMP'], user_job),job_timeout=50000) #)# )
        session['job_id']=job.id
    return render_template("/index_dolomite_constant.html",form=data)

    #    url=boto3_download_results('temp/OUTPUT_DATA/co2_results/'+'co2_results_'+session['user_job']+'.zip')
#
    #    
    #s3://co-2-gasp-bucket/temp/INPUT_DATA/input_water_chem_data/

    #if data.is_submitted():
    #    result=request.form.to_dict()
    #    print(result)
    

@app.route('/index_co2_modelling',methods=['GET','POST'])
def home_co2():
    data=Index_page()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        if result['modelling_option']=='Free state/Geothermal':
            session['modelling_option']='geothermal'
            return redirect('/sim1')
        if result['modelling_option']=='Geochemical':
            session['modelling_option']='geochemical'
            return redirect('/horizontal')
    return render_template("index_co2_modelling.html",form=data)


pitzer_mineral_map= {'Akermanite (Ca2MgSi2O7)': 'Akermanite','Anhydrite (CaSO4)': 'Anhydrite',
'Anthophyllite (Mg7Si8O22(OH)2)': 'Anthophyllite','Antigorite (Mg48Si34O85(OH)62)': 'Antigorite',
'Aragonite (CaCO3)': 'Aragonite','Arcanite (K2SO4)': 'Arcanite','Artinite (Mg2CO3(OH)2:3H2O)': 'Artinite',
'Barite (BaSO4)': 'Barite','Bischofite (MgCl2:6H2O)': 'Bischofite','Bloedite (Na2Mg(SO4)2:4H2O)': 'Bloedite',
'Brucite (Mg(OH)2)': 'Brucite','Burkeite (Na6CO3(SO4)2)': 'Burkeite','Calcite (CaCO3)': 'Calcite',
'Carnallite (KMgCl3:6H2O)': 'Carnallite','Celestite (SrSO4)': 'Celestite','Chalcedony (SiO2)': 'Chalcedony',
'Chrysotile (Mg3Si2O5(OH)4)': 'Chrysotile','Diopside (CaMgSi2O6)': 'Diopside','Dolomite (CaMg(CO3)2)': 'Dolomite',
'Enstatite (MgSiO3)': 'Enstatite','Epsomite (MgSO4:7H2O)': 'Epsomite','Forsterite (Mg2SiO4)': 'Forsterite',
'Gaylussite (CaNa2(CO3)2:5H2O)': 'Gaylussite','Glaserite (NaK3(SO4)2)': 'Glaserite',
'Glauberite (Na2Ca(SO4)2)': 'Glauberite','Goergeyite (K2Ca5(SO4)6H2O)': 'Goergeyite','Gypsum (CaSO4:2H2O)': 'Gypsum',
'Halite (NaCl)': 'Halite','Hexahydrite (MgSO4:6H2O)': 'Hexahydrite','Huntite (CaMg3(CO3)4)': 'Huntite',
'Kainite (KMgClSO4:3H2O)': 'Kainite','Kalicinite (KHCO3)': 'Kalicinite','Kieserite (MgSO4:H2O)': 'Kieserite',
'Labile_S (Na4Ca(SO4)3:2H2O)': 'Labile_S','Leonhardite (MgSO4:4H2O)': 'Leonhardite',
'Leonite (K2Mg(SO4)2:4H2O)': 'Leonite','Magnesite (MgCO3)': 'Magnesite','MgCl2_2H2O (MgCl2:2H2O)': 'MgCl2_2H2O',
'MgCl2_4H2O (MgCl2:4H2O)': 'MgCl2_4H2O','Mirabilite (Na2SO4:10H2O )': 'Mirabilite',
'Misenite (K8H6(SO4)7)': 'Misenite','Nahcolite (NaHCO3)': 'Nahcolite','Natron (Na2CO3:10H2O)': 'Natron',
'Nesquehonite (MgCO3:3H2O)': 'Nesquehonite','Pentahydrite (MgSO4:5H2O)': 'Pentahydrite',
'Pirssonite (Na2Ca(CO3)2:2H2O)': 'Pirssonite','Polyhalite (K2MgCa2(SO4)4:2H2O) ': 'Polyhalite',
'Portlandite (Ca(OH)2)': 'Portlandite','Quartz (SiO2)': 'Quartz','Schoenite (K2Mg(SO4)2:6H2O)': 'Schoenite',
'Sepiolite(d) (Mg2Si3O7.5OH:3H2O)': 'Sepiolite(d)','Sepiolite (Mg2Si3O7.5OH:3H2O)': 'Sepiolite',
'SiO2(a) (SiO2) ': 'SiO2(a)','Sylvite (KCl)': 'Sylvite','Syngenite (K2Ca(SO4)2:H2O)': 'Syngenite',
'Talc (Mg3Si4O10(OH)2)': 'Talc','Thenardite (Na2SO4)': 'Thenardite','Trona (Na3H(CO3)2:2H2O)': 'Trona',
'Borax (Na2(B4O5(OH)4):8H2O)': 'Borax','Boric_acid,s (B(OH)3)': 'Boric_acid,s',
'KB5O8:4H2O (KB5O8:4H2O)': 'KB5O8:4H2O','K2B4O7:4H2O (K2B4O7:4H2O)': 'K2B4O7:4H2O',
'NaBO2:4H2O (NaBO2:4H2O)': 'NaBO2:4H2O','NaB5O8:5H2O (NaB5O8:5H2O)': 'NaB5O8:5H2O',
'Teepleite':'Na2B(OH)4Cl'}

mineral_keys=['mineral_select_1','mineral_select_2','mineral_select_3','mineral_select_4']
#,'mineral_select_5','mineral_select_6','mineral_select_7','mineral_select_8','mineral_select_9','mineral_select_10',
#'mineral_select_11']
volume_keys=['volume_1','volume_2','volume_3','volume_4']
#,'moles_5','moles_6','moles_7','moles_8','moles_9','moles_10','moles_11']

moles_keys=['moles_1','moles_2','moles_3','moles_4']
#,'moles_5','moles_6','moles_7','moles_8','moles_9','moles_10','moles_11']



mineral_keys_secondary=['sec_mineral_select_1','sec_mineral_select_2','sec_mineral_select_3','sec_mineral_select_4']
moles_keys_secondary=['sec_moles_1','sec_moles_2','sec_moles_3','sec_moles_4']


def return_key(val):
    for key, value in pitzer_mineral_map.items():
        if key==val:
            return value
    return('Key Not Found')



@app.route('/sim2',methods=['GET','POST'])
def sim2():#
    data=PhreeqcOptions()
    if data.is_submitted():
        result=request.form.to_dict()
        keys=[result[x] for x in mineral_keys]
        keys=[x for x in keys if x]
        a=[]
        for i in keys:
            if i == 'Dolomite':
                a.append('Dolomite_new')
            else:
                a.append(return_key(i))
        print(a)
        values=[result[x] for x in moles_keys]
        values=[x for x in values if x]
        geochem_minerals=dict(zip(a,values))

        keys=[result[x] for x in mineral_keys_secondary]
        keys=[x for x in keys if x]
        b=[]
        for i in keys:
            if i == 'Dolomite':
                b.append('Dolomite_new')
            else:
                b.append(return_key(i))
        print(b)
        values_b=[result[x] for x in moles_keys_secondary]
        values_b=[x for x in values_b if x]
        geochem_minerals_secondary=dict(zip(b,values_b))
        user_job=str(randint(100000000, 999999999))
        session['user_job']=user_job
        #co2_US_county,co2_US_state,co2_lon_lat
        job = q.enqueue(carbon_capture_MAIN, args=(rawusgs, grad, sur,user_job,geochem_minerals,geochem_minerals_secondary,
        session['area'],session['co2_US_state'],session['co2_US_county'],session['co2_lon_lat'],
        result['radius'],result['height'],result['porosity'],str(session),result),job_timeout=500)
        session['job_id']=job.id
        return redirect('/co2_result_download')
    return render_template("geochem_selections.html",form=data)

@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/Introduction_header')
def serve_1():
    return render_template('introduction_1.html')

@app.route('/Methodology_heading')
def serve_2():
    return render_template('methodology_2.html')

@app.route('/Background_methodology_heading')
def serve_3():
    return render_template('methodology_background_1.html')

@app.route('/USGS_Produced_Water_Database')
def serve_4():
    return render_template('produced_water.html')

@app.route('/Heatflow_data')
def serve_5():
    return render_template('heatflow.html')

@app.route('/MODIS_data')
def serve_6():
    return render_template('modis.html')

@app.route('/Robertson_et_al')
def serve_7():
    return render_template('robertson_2021.html')

@app.route('/User_method')
def serve_8():
    return render_template('user_methods.html')

@app.route('/free_state')
def serve_9():
    return render_template('free_state.html')

@app.route('/geochemical_modelling')
def serve_10():
    return render_template('geochem_modelling.html')

@app.route('/Results_heading')
def serve_11():
    return render_template('free_state_results_1.html')

@app.route('/geochemical_modelling_results')
def serve_12():
    return render_template('geochem_modelling_results.html')

@app.route('/reference_heading')
def serve_13():
    return render_template('references.html')


@app.route('/sim1',methods=['GET','POST'])
def sim1():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        if result['co2_profile']=='Horizontal':
            return redirect('/horizontal')
        if result['co2_profile']=='Vertical':
            return redirect('/vertical')
        print(result)
    return render_template('horizontal_vertical.html',form=data)

@app.route('/horizontal',methods=['GET','POST'])
def horizontal_top():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        session['area']=result['mapping_select']
        print(session['modelling_option'])
        if session['modelling_option']=='geothermal' and session['area']=='All US':
            return redirect('/horizontal_all_us')
        if session['modelling_option']=='geochemical' and session['area']=='All US':
            session['co2_US_state']=None
            session['co2_US_county']=None
            session['co2_lon_lat']=None
            return redirect('/sim2')
        if session['modelling_option']=='geothermal' and session['area']=='US state':
            return redirect('/horizontal_state')
        if session['modelling_option']=='geochemical' and session['area']=='US state':
            return redirect('/horizontal_state_geochemical')
        if session['modelling_option']=='geothermal' and session['area']=='US county':
            return redirect('/horizontal_county')
        if session['modelling_option']=='geochemical' and session['area']=='US county':
            return redirect('/horizontal_county_geochemical')
        if session['modelling_option']=='geothermal' and session['area']=='Custom mapping':
            return redirect('/horizontal_custom')
        if session['modelling_option']=='geochemical' and session['area']=='Custom mapping':
           return redirect('/horizontal_custom_geochemical')
    return render_template('horizontal.html',form=data)

@app.route('/horizontal_all_us',methods=['GET','POST'])
def all_us_horizontal():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        co2_profile='Horizontal'
        area='All US'
        co2_US_state=None
        co2_US_county=None
        co2_lon_lat=None
        min_vert_depth=None
        max_vert_depth=None
        user_job=str(randint(10000000, 99999999))
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile, result['co2_depth'],
        result['land_correct'],min_vert_depth,max_vert_depth, co2_US_state, co2_US_county,co2_lon_lat,area,
        result['climate'],user_job,str(session),result),job_timeout=500)
        session['job_id']=job.id
        return redirect('/co2_result_download')
    return render_template('all_us_horizontal.html',form=data)


@app.route('/horizontal_state',methods=['GET','POST'])
def state_horizontal():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        #print(type(result['co2_depth']))
        co2_profile='Horizontal'
        area='US state'
        co2_US_county=None
        co2_lon_lat=None
        min_vert_depth=None
        max_vert_depth=None
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile,
        result['co2_depth'],min_vert_depth,max_vert_depth,result['land_correct'],result['US_state_select'],
        co2_US_county,co2_lon_lat,area,result['climate'],user_job,str(session),result),job_timeout=500)
        session['job_id']=job.id
        return redirect('/co2_result_download')
    return render_template('state_horizontal.html',form=data)

@app.route('/horizontal_state_geochemical',methods=['GET','POST'])
def state_horizontal_geochemical():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        #print(type(result['co2_depth']))
        co2_profile='Horizontal'
        area='US state'
        co2_US_county=None
        co2_lon_lat=None
        min_vert_depth=None
        max_vert_depth=None
        session['co2_US_state']=result['US_state_select']
        session['co2_US_county']=co2_US_county
        session['co2_lon_lat']=co2_lon_lat
        return redirect('/sim2')
    return render_template('state_horizontal_geochem.html',form=data)




@app.route('/horizontal_county',methods=['GET','POST'])
def county_horizontal():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        co2_profile='Horizontal'
        area='US county'
        co2_lon_lat=None
        min_vert_depth=None
        max_vert_depth=None
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile,
        result['co2_depth'],min_vert_depth,max_vert_depth,result['land_correct'],result['US_state_select'],
        result['US_county'],co2_lon_lat,area,result['climate'],user_job,str(session),result),job_timeout=500)
        session['job_id']=job.id
        return redirect('/co2_result_download')
    return render_template('county_horizontal.html',form=data)

@app.route('/horizontal_county_geochemical',methods=['GET','POST'])
def county_horizontal_geochemical():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        co2_profile='Horizontal'
        area='US county'
        co2_lon_lat=None
        min_vert_depth=None
        max_vert_depth=None
        session['co2_US_state']=result['US_state_select']
        session['co2_US_county']=result['US_county']
        session['co2_lon_lat']=co2_lon_lat
        return redirect('/sim2')
    return render_template('county_horizontal_geochemical.html',form=data)


@app.route('/horizontal_custom',methods=['GET','POST'])
def custom_horizontal():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        co2_profile='Horizontal'
        area='Custom mapping'
        co2_US_state=None
        co2_US_county=None
        min_vert_depth=None
        max_vert_depth=None
        co2_lon_lat={'Lon':[int(x) for x in result['lon_bounding'].split(",")], 'Lat':[int(x) for x in result['lat_bounding'].split(",")]}
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        os.mkdir(co2_results+'/'+user_job)
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile,
        result['co2_depth'],min_vert_depth,max_vert_depth,result['land_correct'],
        co2_US_state,co2_US_county,co2_lon_lat,area,result['climate'],user_job,str(session),result),job_timeout=500)
        session['job_id']=job.id
        return redirect('/co2_result_download')
    return render_template('custom_horizontal.html',form=data)

@app.route('/horizontal_custom_geochemical',methods=['GET','POST'])
def custom_horizontal_geochemical():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        co2_profile='Horizontal'
        area='Custom mapping'
        co2_US_state=None
        co2_US_county=None
        min_vert_depth=None
        max_vert_depth=None
        co2_lon_lat={'Lon':[int(x) for x in result['lon_bounding'].split(",")], 'Lat':[int(x) for x in result['lat_bounding'].split(",")]}
        session['co2_US_state']=result['US_state_select']
        session['co2_US_county']=co2_US_county
        session['co2_lon_lat']=co2_lon_lat
        return redirect('/sim2')
    return render_template('custom_horizontal_geochemical.html',form=data)



@app.route('/co2_result_download',methods=['GET','POST'])
def download():
    print(session['job_id'])
    job=Job.fetch(session['job_id'],connection=conn)
    if session['modelling_option']=='geothermal':
        if job.is_finished:
            print('hurrah')
            url=boto3_download_results('temp/OUTPUT_DATA/co2_results/'+'co2_results_'+session['user_job']+'.zip')
            return redirect(url)
        else:
            print('nay')
            time.sleep(30)
            return redirect('/co2_result_download')
    if session['modelling_option']=='geochemical':
        if job.is_finished:
            print('hurrah')
            url=boto3_download_results('temp/OUTPUT_DATA/geochemical_result/'+'geochem_result_'+session['user_job']+'.zip')
            return redirect(url)
        else:
            print('nay')
            time.sleep(30)
            return redirect('/co2_result_download')




@app.route('/vertical',methods=['GET','POST'])
def vertical():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        if result['mapping_select']=='All US':
            return redirect('/vertical_US')
        if result['mapping_select']=='US state':
            return redirect('/vertical_state')
        if result['mapping_select']=='US county':
            return redirect('/vertical_county')
        if result['mapping_select']=='Custom mapping':
            return redirect('/vertical_custom')
        print(result)
    return render_template('vertical.html',form=data)


@app.route('/vertical_US',methods=['GET','POST'])
def vertical_US():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        co2_profile='Vertical'
        area='All US'
        co2_US_state=None
        co2_US_county=None
        co2_lon_lat=None
        min_vert_depth=None
        max_vert_depth=None
        user_job=str(randint(10000000, 99999999))
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile, result['co2_depth'],
        result['land_correct'],min_vert_depth,max_vert_depth, co2_US_state, co2_US_county,co2_lon_lat,area,
        result['climate'],user_job,str(session),result),job_timeout=500)
        session['job_id']=job.id
        return redirect('/co2_result_download')
    return render_template('all_us_vertical.html',form=data)

@app.route('/vertical_state',methods=['GET','POST'])
def state_vertical():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        co2_profile='Vertical'
        area='US state'
        co2_lon_lat=None
        co2_US_county=None
        co2_depth=300 #not used
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile,
        co2_depth,result['min_vert_depth'],result['max_vert_depth'],result['land_correct'],
        result['US_state_select'],co2_US_county,co2_lon_lat,area,result['climate'],user_job,str(session),result),job_timeout=500)
        session['job_id']=job.id
        return redirect('/co2_result_download')
    return render_template('state_vertical.html',form=data)


@app.route('/vertical_county',methods=['GET','POST'])
def county_vertical():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        co2_profile='Vertical'
        area='US county'
        co2_lon_lat=None
        co2_depth=300 #not used
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile,
        co2_depth,result['min_vert_depth'],result['max_vert_depth'],result['land_correct'],
        result['US_state_select'],result['US_county'],co2_lon_lat,area,result['climate'],user_job,str(session),result),job_timeout=500)
        session['job_id']=job.id
        return redirect('/co2_result_download')
    return render_template('county_vertical.html',form=data)

@app.route('/vertical_custom',methods=['GET','POST'])
def custom_vertical():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        co2_profile='Vertical'
        area='Custom mapping'
        co2_US_state=None
        co2_US_county=None
        co2_depth=300 #not used
        co2_lon_lat={'Lon':[int(x) for x in result['lon_bounding'].split(",")], 'Lat':[int(x) for x in result['lat_bounding'].split(",")]}
        print(co2_lon_lat)
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile,
        co2_depth,result['min_vert_depth'],result['max_vert_depth'],result['land_correct'],
        co2_US_state,co2_US_county,co2_lon_lat,area,result['climate'],user_job,str(session),result),job_timeout=500)
        session['job_id']=job.id
        return redirect('/co2_result_download')
    return render_template('custom_vertical.html',form=data)

@app.route('/molar_volume_conversion',methods=['GET','POST'])
def mol_vol():
    data=volume_to_mole()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        mineral_density = eval(open(directory+'Mineral_dictionary_density.txt').read())
        mineral_mr = eval(open(directory+'Mineral_dictionary_mr.txt').read())
        mineral_density={k.replace('d_', '') : v for k, v in mineral_density.items()}
        mineral_mr={k.replace('d_', '') : v for k, v in mineral_mr.items()}
        keys=[result[x] for x in mineral_keys]
        keys=[x for x in keys if x]
        a=[]
        for i in keys:
            if i == 'Dolomite':
                a.append('Dolomite_new')
            else:
                a.append(return_key(i))
        print(a)
        values=[result[x] for x in moles_keys]
        values=[float(x) for x in values if x]
        geochem_minerals=pd.DataFrame([(dict(zip(a,values)))]).transpose()
        geochem_minerals.rename(columns={geochem_minerals.columns[0]: 'Vol. prop (%)'}, inplace=True)
        geochem_minerals['Moles in 100cm3']=np.nan
        for row in geochem_minerals.index.values:
            geochem_minerals['Moles in 100cm3'][row]=(geochem_minerals['Vol. prop (%)'][row]*float(mineral_density[row]))/float(mineral_mr[row])
        table_d=geochem_minerals.to_html()
        return render_template('display.html',table=table_d)
    return render_template('molar_volume_conversion.html',form=data)


@app.route('/ajs_modelling',methods=['GET','POST'])
def ajs_model():
    data=volume_to_mole()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        mineral_density = eval(open(directory+'Mineral_dictionary_density.txt').read())
        mineral_mr = eval(open(directory+'Mineral_dictionary_mr.txt').read())
        mineral_density={k.replace('d_', '') : v for k, v in mineral_density.items()}
        mineral_mr={k.replace('d_', '') : v for k, v in mineral_mr.items()}
        keys=[result[x] for x in mineral_keys]
        keys=[x for x in keys if x]
        a=[]
        for i in keys:
            if i == 'Dolomite':
                a.append('Dolomite_new')
            else:
                a.append(return_key(i))
        print(a)
        values=[result[x] for x in moles_keys]
        values=[float(x) for x in values if x]
        geochem_minerals=pd.DataFrame([(dict(zip(a,values)))]).transpose()
        geochem_minerals.rename(columns={geochem_minerals.columns[0]: 'Vol. prop (%)'}, inplace=True)
        geochem_minerals['Moles in 100cm3']=np.nan
        for row in geochem_minerals.index.values:
            geochem_minerals['Moles in 100cm3'][row]=(geochem_minerals['Vol. prop (%)'][row]*float(mineral_density[row]))/float(mineral_mr[row])
        table_d=geochem_minerals.to_html()
        return render_template('display.html',table=table_d)
    return render_template('molar_volume_conversion.html',form=data)


if __name__ == '__main__':
    #path = os.getcwd()
    #print('current path')
    #print(path)
    #files = os.listdir(os.curdir)
    #print(files)
    rawusgs, grad, sur, medusgs = data_import.main()
    app.run(host="0.0.0.0", port=8080,debug=True)

    #print('hello')
    #print(S3_KEY)
    #print(S3_BUCKET)
    #print(co2_gasp)
