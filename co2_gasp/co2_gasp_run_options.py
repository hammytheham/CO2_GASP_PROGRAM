#user config options
#Initial database size and lithology classification system
lithology_simple = True #Change lithology characterisation to 1 word simpliefied classification - default True database size =
lithology_small = False  # Change lithology characterisation to 1 word simpliefied classification and cull samples with no lithology - default false - database size =
lithology_all = False #Just a geochemical filter in place original USGS lithology description  - default false
lithology_no_geochem= False # Geochemical filter removed

#CO2 gradients
CO2_only = True #This option only determines free state CO2
water_density = True # To modify at a later date to use local water density values - currently is True which uses default
water_density_value = []
co2_profile ='Vertical' #'Vertical generates a 2-D Vertical slice of CO2 density and pressure at a location 'Horizontal' - generates a flat 2D profile
co2_lon_lat = [-19,-20,32,35] #for use with the vertical option
co2_depth = [600] #
co2_depth_bounding = []
co2_US_state=[44] #see menu for options
land_sur_correct=[2] #apply a land surface correction for climate change modelling 



#code_validation options - most by default false as repetitive
geo_interp_T_F = False #run interpolation - default false
MODIS_process_T_F = False  #run download of MODIS data and subsequent processing - default is false
