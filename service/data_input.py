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

class PhreeqcOptions(FlaskForm):
    'For geochemical modelling'
    minerals=['','Akermanite (Ca2MgSi2O7)','Anhydrite (CaSO4)','Anthophyllite (Mg7Si8O22(OH)2)','Antigorite (Mg48Si34O85(OH)62)',
    'Aragonite (CaCO3)','Arcanite (K2SO4)','Artinite (Mg2CO3(OH)2:3H2O)','Barite (BaSO4)','Bischofite (MgCl2:6H2O)',
    'Bloedite (Na2Mg(SO4)2:4H2O)','Brucite (Mg(OH)2)','Burkeite (Na6CO3(SO4)2)','Calcite (CaCO3)','Carnallite (KMgCl3:6H2O)',
    'Celestite (SrSO4)','Chalcedony (SiO2)','Chrysotile (Mg3Si2O5(OH)4)','Diopside (CaMgSi2O6)','Dolomite (CaMg(CO3)2)',
    'Enstatite (MgSiO3)','Epsomite (MgSO4:7H2O)','Forsterite (Mg2SiO4)','Gaylussite (CaNa2(CO3)2:5H2O)','Glaserite (NaK3(SO4)2)',
    'Glauberite (Na2Ca(SO4)2)','Goergeyite (K2Ca5(SO4)6H2O)','Gypsum (CaSO4:2H2O)','Halite (NaCl)','Hexahydrite (MgSO4:6H2O)',
    'Huntite (CaMg3(CO3)4)','Kainite (KMgClSO4:3H2O)','Kalicinite (KHCO3)','Kieserite (MgSO4:H2O)','Labile_S (Na4Ca(SO4)3:2H2O)',
    'Leonhardite (MgSO4:4H2O)','Leonite (K2Mg(SO4)2:4H2O)','Magnesite (MgCO3)','MgCl2_2H2O (MgCl2:2H2O)','MgCl2_4H2O (MgCl2:4H2O)',
    'Mirabilite (Na2SO4:10H2O )','Misenite (K8H6(SO4)7)','Nahcolite (NaHCO3)','Natron (Na2CO3:10H2O)','Nesquehonite (MgCO3:3H2O)',
    'Pentahydrite (MgSO4:5H2O)','Pirssonite (Na2Ca(CO3)2:2H2O)','Polyhalite (K2MgCa2(SO4)4:2H2O) ','Portlandite (Ca(OH)2)',
    'Quartz (SiO2)','Schoenite (K2Mg(SO4)2:6H2O)','Sepiolite(d) (Mg2Si3O7.5OH:3H2O)','Sepiolite (Mg2Si3O7.5OH:3H2O)','SiO2(a) (SiO2) ',
    'Sylvite (KCl)','Syngenite (K2Ca(SO4)2:H2O)','Talc (Mg3Si4O10(OH)2)','Thenardite (Na2SO4)','Trona (Na3H(CO3)2:2H2O)',
    'Borax (Na2(B4O5(OH)4):8H2O)','Boric_acid,s (B(OH)3)','KB5O8:4H2O (KB5O8:4H2O)','K2B4O7:4H2O (K2B4O7:4H2O)','NaBO2:4H2O (NaBO2:4H2O)',
    'NaB5O8:5H2O (NaB5O8:5H2O)']
    mineral_select_1=SelectField('Select Mineral 1', choices=minerals)
    moles_1=StringField('Enter moles of select mineral 1')

    mineral_select_2=SelectField('Select Mineral 2', choices=minerals)
    moles_2=StringField('Enter moles of select mineral 2')

    mineral_select_3=SelectField('Select Mineral 3', choices=minerals)
    moles_3=StringField('Enter moles of select mineral 3')

    mineral_select_4=SelectField('Select Mineral 4', choices=minerals)
    moles_4=StringField('Enter moles of select mineral 4')
    
    mineral_select_5=SelectField('Select Mineral 5', choices=minerals)
    moles_5=StringField('Enter moles of select mineral 5')    

    mineral_select_6=SelectField('Select Mineral 6', choices=minerals)
    moles_6=StringField('Enter moles of select mineral 6')

    mineral_select_7=SelectField('Select Mineral 7', choices=minerals)
    moles_7=StringField('Enter moles of select mineral 7')

    mineral_select_8=SelectField('Select Mineral 8', choices=minerals)
    moles_8=StringField('Enter moles of select mineral 8')
    
    mineral_select_9=SelectField('Select Mineral 9', choices=minerals)
    moles_9=StringField('Enter moles of select mineral 9')

    mineral_select_10=SelectField('Select Mineral 10', choices=minerals)
    moles_10=StringField('Enter moles of select mineral 10')
    
    mineral_select_11=SelectField('Select Mineral 11', choices=minerals)
    moles_11=StringField('Enter moles of select mineral 11')

    mineral_select_12=SelectField('Select Mineral 12', choices=minerals)
    moles_12=StringField('Enter moles of select mineral 12')
    
    submit=SubmitField('Submit parameters')
