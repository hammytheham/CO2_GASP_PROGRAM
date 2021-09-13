from flask import Flask, render_template
import boto3
from config import S3_KEY, S3_SECRET, S3_BUCKET

app = Flask(__name__)

#s3_resource = boto3.resource("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)


app.config['EXPLAIN_TEMPLATE_LOADING'] = True
#app.config['FLASKS3_BUCKET_NAME'] = 'co-2-gasp-bucket'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    s3_resource = boto3.resource("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)
    return render_template("about.html")

#adding defunct text ading more texrt
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080,debug=True)