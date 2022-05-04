'''
Created on Jul 14, 2015

define some global variables

@author: degraba
'''

# variabels for testing
# absolute emission per cell and macro sector
path_emission_cdf_test = 'input/20151116_SR_no2_pm10_pm25/BC_emi_PM25_Y.nc'
# netcdf with cells where reductions have to be applied (value between 0 and 1)
# path_area_cdf_test = 'input/EMI_RED_NUTS3_ITALY.nc'
path_area_cdf_test = 'input/London_region.nc'
# reductions per precursor and macro sector
path_reduction_txt_test = 'input/user_reduction_snap7.txt'
path_reduction50all_txt_test = 'input/user_reduction_all50.txt'
# reductions per precursor and macro sector for module 3a and 3b
path_reduction_mod3a1P_txt_test = 'input/potency_reduction_module3a1P.txt'
path_reduction_mod3a2P_txt_test = 'input/potency_reduction_module3a2P.txt'
path_reduction_mod3b_txt_test = 'input/potency_reduction_module3b.txt'
# netcdf with model parameters per cell
path_model_cdf_test = 'input/20151116_SR_no2_pm10_pm25/SR_PM25_Y.nc' 
# folder where output will be put
path_result_cdf_test = 'output/'
# progress log is used when module 1 is called by another module
path_nuts0_cdf_test = 'input/EMI_RED_ATLAS_NUTS0.nc'
path_nuts1_cdf_test = 'input/EMI_RED_ATLAS_NUTS1.nc'
path_nuts2_cdf_test = 'input/EMI_RED_ATLAS_NUTS2.nc'
path_nuts3_cdf_test = 'input/EMI_RED_ATLAS_NUTS3.nc'

path_base_conc_cdf_test = 'input/20151116_SR_no2_pm10_pm25/BC_conc_PM25_Y.nc'


# list of precursors
# order important, it's the order in the alpha and omega arrays
# precursor_lst = ['NOx', 'NMVOC', 'NH3', 'PM25', 'SOx']  

# order important, it's the order in the alpha and omega arrays
sector_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]   #  

# fixed reduction percentage for potency calculation
alpha_potency = float(50)
