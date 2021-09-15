from flask import Flask, render_template, redirect, request, url_for
import boto3
from config import S3_KEY, S3_SECRET, S3_BUCKET
from data_input import Data_input, Index_page

app = Flask(__name__)
app.config['SECRET_KEY']=S3_SECRET
#s3_resource = boto3.resource("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)

app.config['EXPLAIN_TEMPLATE_LOADING'] = True
#app.config['FLASKS3_BUCKET_NAME'] = 'co-2-gasp-bucket'

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
            return redirect('/about')
    return render_template("index.html",form=data)

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
def horizontal():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
        
    return render_template('horizontal.html',form=data)

@app.route('/vertical',methods=['GET','POST'])
def vertical():
    data=Data_input()
    if data.is_submitted():
        result=request.form.to_dict()
        print(result)
    return render_template('vertical.html',form=data)
  
    

#adding defunct text ading more texrt
    
if __name__ == '__main__':
    print('hello')
    print(S3_KEY)
    print(S3_BUCKET)
    app.run(host="0.0.0.0", port=8080,debug=True)