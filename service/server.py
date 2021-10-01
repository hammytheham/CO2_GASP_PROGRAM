from flask import Flask, render_template, redirect, request, url_for, session
import boto3
from config import S3_KEY, S3_SECRET, S3_BUCKET
from data_input import Data_input,Data_input_geochem, Index_page, Download
import sys
from data_import import boto3_download_results
#Geochemical code
import data_import
import data_import_2
import carbon_capture
from CO2_density_state import main as CO2_density_state_MAIN
from co2_gasp_run_options import *     #import the option file from within the same folder
from redis import Redis
from rq import Queue
from rq.job import Job
from worker import conn
import time
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY']=S3_SECRET
#s3_resource = boto3.resource("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)

app.config['EXPLAIN_TEMPLATE_LOADING'] = True
#app.config['FLASKS3_BUCKET_NAME'] = 'co-2-gasp-bucket'

q = Queue(connection=conn)

@app.route('/',methods=['GET','POST'])
def home():
    data=Index_page()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        if result['modelling_option']=='Option 1':
            print('hello')
            return redirect('/sim1')
        if result['modelling_option']=='Option 2':
            return redirect('/sim2')
    return render_template("index.html",form=data)


#@app.route('/sim2')
#def sim2():#
#    data=Data_input_geochem()
#    if data.is_submitted():
#        result=request.form.to_dict()
#        if result[]='':



@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/about')
def about():
    return render_template("about.html")

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
        if result['mapping_select']=='co2_all_US_mapping':
            return redirect('/horizontal_all_us')
        if result['mapping_select']=='co2_state_mapping':
            return redirect('/horizontal_state')
        if result['mapping_select']=='co2_county_mapping':
            return redirect('/horizontal_county')
        if result['mapping_select']=='co2_custom_mapping':
            return redirect('/horizontal_custom')
    return render_template('horizontal.html',form=data)

@app.route('/horizontal_all_us',methods=['GET','POST'])
def all_us_horizontal():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        co2_profile='Horizontal'
        area='co2_all_US_mapping'
        co2_US_state=None
        co2_US_county=None
        co2_lon_lat=None
        min_vert_depth=None
        max_vert_depth=None
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile, result['co2_depth'],
        result['land_correct'],min_vert_depth,max_vert_depth, co2_US_state, co2_US_county,co2_lon_lat,area,result['climate'],user_job))
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
        area='co2_state_mapping'
        co2_US_county=None
        co2_lon_lat=None
        min_vert_depth=None
        max_vert_depth=None
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile,
        result['co2_depth'],min_vert_depth,max_vert_depth,result['land_correct'],result['US_state_select'],co2_US_county,co2_lon_lat,area,result['climate'],user_job))
        session['job_id']=job.id
        return redirect('/co2_result_download')
    return render_template('state_horizontal.html',form=data)





@app.route('/horizontal_county',methods=['GET','POST'])
def county_horizontal():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        co2_profile='Horizontal'
        area='co2_county_mapping'
        co2_lon_lat=None
        min_vert_depth=None
        max_vert_depth=None
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile,
        result['co2_depth'],min_vert_depth,max_vert_depth,result['land_correct'],result['US_state_select'],result['US_county'],co2_lon_lat,area,result['climate'],user_job))
        session['job_id']=job.id
        return redirect('/co2_result_download')
    return render_template('county_horizontal.html',form=data)


@app.route('/horizontal_custom',methods=['GET','POST'])
def custom_horizontal():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        co2_profile='Horizontal'
        area='co2_custom_mapping'
        co2_US_state=None
        co2_US_county=None
        min_vert_depth=None
        max_vert_depth=None
        co2_lon_lat={'Lon':[int(x) for x in result['lon_bounding'].split(",")], 'Lat':[int(x) for x in result['lat_bounding'].split(",")]}
        print(co2_lon_lat)
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile,
        result['co2_depth'],min_vert_depth,max_vert_depth,result['land_correct'],co2_US_state,co2_US_county,co2_lon_lat,area,result['climate'],user_job))
        session['job_id']=job.id
        return redirect('/co2_result_download')
    return render_template('custom_horizontal.html',form=data)



@app.route('/co2_result_download',methods=['GET','POST'])
def download():
    print(session['job_id'])
    job=Job.fetch(session['job_id'],connection=conn)
    if job.is_finished:
        print('hurrah')
        url=boto3_download_results('temp/OUTPUT_DATA/co2_results/'+'co2_results_'+session['user_job']+'.zip')
        return redirect(url)
    else:
        print('nay')
        time.sleep(15)
        return redirect('/co2_result_download')

@app.route('/vertical',methods=['GET','POST'])
def vertical():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        if result['mapping_select']=='co2_state_mapping':
            return redirect('/vertical_state')
        if result['mapping_select']=='co2_county_mapping':
            return redirect('/vertical_county')
        if result['mapping_select']=='co2_custom_mapping':
            return redirect('/vertical_custom')
        print(result)
    return render_template('vertical.html',form=data)



@app.route('/vertical_state',methods=['GET','POST'])
def state_vertical():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        co2_profile='Vertical'
        area='co2_state_mapping'
        co2_lon_lat=None
        co2_US_county=None
        co2_depth=300 #not used
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile,
        co2_depth,result['min_vert_depth'],result['max_vert_depth'],result['land_correct'],result['US_state_select'],co2_US_county,co2_lon_lat,area,result['climate'],user_job))
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
        area='co2_county_mapping'
        co2_lon_lat=None
        co2_depth=300 #not used
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile,
        co2_depth,result['min_vert_depth'],result['max_vert_depth'],result['land_correct'],result['US_state_select'],result['US_county'],co2_lon_lat,area,result['climate'],user_job))
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
        area='co2_custom_mapping'
        co2_US_state=None
        co2_US_county=None
        co2_depth=300 #not used
        co2_lon_lat={'Lon':[int(x) for x in result['lon_bounding'].split(",")], 'Lat':[int(x) for x in result['lat_bounding'].split(",")]}
        print(co2_lon_lat)
        user_job=str(randint(10000000, 99999999))
        session['user_job']=user_job
        job = q.enqueue(CO2_density_state_MAIN, args=(grad, sur, co2_profile,
        co2_depth,result['min_vert_depth'],result['max_vert_depth'],result['land_correct'],co2_US_state,co2_US_county,co2_lon_lat,area,result['climate'],user_job))
        session['job_id']=job.id
        return redirect('/co2_result_download')
    return render_template('custom_vertical.html',form=data)




#adding defunct text ading more texrt

if __name__ == '__main__':
    rawusgs, grad, sur, medusgs = data_import.main()
    user_job=str(1010111)
    carbon_capture.main(rawusgs, grad, sur,user_job)
    app.run(host="0.0.0.0", port=8080,debug=True)

    #print('hello')
    #print(S3_KEY)
    #print(S3_BUCKET)
    #print(co2_gasp)
