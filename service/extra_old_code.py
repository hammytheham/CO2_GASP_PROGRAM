#data='INPUT_DATA'
#directory='/Users/hamish/github/co2_gasp'
#geotherm_result = 'INPUT_DATA/geothermal_result_files'
#MODIS_results = 'INPUT_DATA/MODIS_result_files'
#geochem_result = 'INPUT_DATA/geochemical_result_files'

#from data_import
#this method is now mostly defunct....probably...can use S3 like local filesystem....mostly....
#def boto3_file_read(file):
#    print(file)
#    s3_client = boto3.client('s3')
#    response=s3_client.get_object(Bucket='co-2-gasp-bucket',Key=file)
#    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
#    if status == 200:
#        return response.get('Body')
#    else:
#       print ('Error retrieving file:',file)

#old docker
FROM public.ecr.aws/lts/ubuntu:latest
#FROM public.ecr.aws/ubuntu/redis:latest
RUN echo Updating existing packages, installing and upgrading python and pip.

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
RUN apt-get install build-essential -y
RUN apt-get install g++ -y
RUN apt-get install gcc -y
#RUN apt-get install redis -y
RUN apt-get install gdal-bin -y
RUN which gcc 
RUN echo $PATH
RUN echo 'Hellow'


#WORKDIR /PHREEQC/phreeqc_files/examples
#COPY /PHREEQC/phreeqc_files/database/phreeqc.dat /PHREEQC/phreeqc_files/examples/
#RUN ../bin/phreeqc ex1 ex1.out phreeqc.dat 


FROM osgeo/gdal:ubuntu-small-latest
FROM continuumio/miniconda3
WORKDIR /app
## Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml
#Make RUN commands use the new environment:
RUN echo "conda activate myenv" >> ~/.bashrc
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Demonstrate the environment is activated:
RUN echo "Make sure flask is installed AND NEW STUFFF:"
RUN python -c "import flask"
RUN python -c "import flask_wtf"
RUN python -c "import wtforms"


RUN echo Copy service directory

COPY ./PHREEQC /PHREEQC
COPY ./service /service
COPY ./temp_files /temp_files
COPY ./INPUT_DATA /INPUT_DATA


#RUN redis-server
#RUN gdal
#RUN ls *


##COPY /co2gaspService/server.py ./
##COPY /co2gaspService/entrypoint.sh ./
#
WORKDIR /service
#
#
##RUN ["chmod", "+x","./entrypoint.sh"]
#RUN ["chmod", "+x","gdal_command_1.sh"]
#RUN ["chmod", "+x","gdal_command_2.sh"]
#RUN ["chmod", "+x","gdal_command_3.sh"]
#RUN ["chmod", "+x","gdal_command_4.sh"]
#RUN ["chmod", "+x","aws_sync_co2_results.sh"]
#RUN ["chmod", "+x","aws_sync_geochem_results.sh"]
#RUN ["chmod", "+x","bash_phreeqc.sh"]
#
#
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "myenv", "python","server.py"]
<b>1.2 Project Background</b><br>


Additional development work has been carried to utilize the core methodology for the purposes of carbon capture and storage. The choice to develop a website recongises that a web app represents a high level of user accessibility and reproducibility. We aim to develop/release an API/python program more geared towards computationally inclined users depending on feedback. <br>
</p>
<p>
<b>1.2 Methodology/Groundtruthing</b><br>
The methodology comprises three core databases that have been coupled together.<br>
<b>USGS Produced Water database (Blondes et al. 2016)</b> 
This database comprises 

</p>



We realised that the 
</p>


<p>CO2-GASP (CO2, geochemcial assessment of seqeustration potential) is desgined to enable users to quickly evaluate and simulate CO2 sequestration at a range of scales. CO2-GASP was primarily developed by Hamish Robertson, with Fiona Whitaker, Cathy Holis and Hilary Corlett providing additional review. <br>

Full documentation is avalible as a downloadable PDF here: <br>

Relevant papers: <br>

</p>