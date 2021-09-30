from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField

class Download(FlaskForm):
    submit=SubmitField('Download files')


class Index_page(FlaskForm):
    modelling_option_choices=['Option 1', 'Option 2']
    modelling_option=RadioField(choices=modelling_option_choices)
    submit=SubmitField('Submit parameters')


class Data_input_geochem(FlaskForm):
    modelling_option_choices=['Option 1', 'Option 2']
    modelling_option=RadioField(choices=modelling_option_choices)
    submit=SubmitField('Submit parameters')

class Data_input(FlaskForm):
    'For co2 density/state and geothermal gradient'
    #co2_profile=StringField
    SelectDatabaseChoices=['lithology_simple','lithology_small','lithology_all','lithology_no_geochem']
    database_select=RadioField('Database Filter',choices=SelectDatabaseChoices)
    
    SelectField_choices=['Horizontal','Vertical']
    co2_profile=RadioField('CO2 Profile',choices=SelectField_choices)
    
    SelectMapping_choices=['co2_all_US_mapping','co2_state_mapping','co2_county_mapping','co2_custom_mapping']
    mapping_select=RadioField('Mapping Choices',choices=SelectMapping_choices)
    
    us_state=['Alabama','Arizona','Arkansas','California','Colorado'
,'Connecticut','Delaware','Florida','Georgia','Idaho','Illinois','Indiana',
'Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts',
'Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada',
'New Hampshire','New Jersey','New Mexico','New York','North Carolina',
'North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island',
'South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont',
'Virginia','Washington','West Virginia','Wisconsin','Wyoming']
    US_state_select=SelectField('Select State', choices=us_state)
    
    US_county=StringField('Enter county(ies)')
    
    co2_depth=StringField('CO2 target depth')

    land_correct=StringField('Landsurface correction')

    min_vert_depth=StringField('Minimum vertical depth (m) -- y-axis minimum')
    
    max_vert_depth=StringField('Maximum vertical depth (m) -- y-axis maximum')

    lat_bounding=StringField('Latitude coordinates of corners of bounding box. Comma seperated values (e.g 30,32,32,30)')

    lon_bounding=StringField('Longitude coordinates of bounding box. Comma seperated values (e.g -101,-101,-98,-98)')

    climate=StringField('')

    Selectclimate_choices=[True,False]
    climate=RadioField('Plot land surface correction?',choices=Selectclimate_choices)
   
    submit=SubmitField('Submit parameters')


    