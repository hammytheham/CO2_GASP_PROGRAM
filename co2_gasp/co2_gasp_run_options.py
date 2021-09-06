#user config options
#Initial database size and lithology classification system
lithology_simple = True #Change lithology characterisation to 1 word simpliefied classification - default True database size =
lithology_small = False  # Change lithology characterisation to 1 word simpliefied classification and cull samples with no lithology - default false - database size =
lithology_all = False #Just a geochemical filter in place original USGS lithology description  - default false
lithology_no_geochem= False # Geochemical filter removed

#CO2 gradients
CO2_thermal_only = True #This option only determines free state CO2
water_density = True # To modify at a later date to use local water density values - currently is True which uses default
water_density_value = []

co2_profile ='Horizontal' #'Vertical generates a 2-D Vertical slice of CO2 density and pressure at a location 'Horizontal' - generates a flat 2D profile
co2_all_US_mapping=False
co2_state_mapping=False
co2_county_mapping=False
co2_custom_mapping = True
co2_US_state=['Texas'] #see menu for options
co2_US_county=['Lee']#'King','Midland','Martin']

co2_lon_lat = {'Lon':[-101,-101,-98,-98],'Lat':[30,32,32,30]} #co-ordinates  zipped in order marking the bouding box, unlimited number for Polygon #whole US - [(-128.600464,24.374619),(-128.600464,50.406767),(-60.748901,50.406767),(-60.748901,24.374619)]

co2_depth = [250] # m

land_sur_correct=[2] #apply a land surface correction for climate change modelling
min_max_vert_depth=[1,3000] #m - note do not set to zero as it wont work, minimum is 1 m


#code_validation options - most by default false as repetitive
geo_interp_T_F = False #run interpolation - default false
MODIS_process_T_F = False  #run download of MODIS data and subsequent processing - default is false
