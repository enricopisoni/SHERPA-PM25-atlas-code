'''
Created on 27 June 2017

ONE SCRIPT TO RUN THEM ALL
- EMEP and CHIMERE based sherpa
- NO2 and PM2.5
- aggregated and disaggregated areas
- all snaps or per snap
- all precursors or per precursorc

Each run calls module 6 (modified with full output)
- target cell is the centre of the 'city' area
concentration changes to emission reductions in
- the city
- the commuting zone (without city)
- background per country
are calculated
user_reduction_list
@author: degraba
'''
# import sys
import os
from datetime import date

from module6_fua import module6 
import timeit

# paths to input data
root = 'D:/WORK/projects/37_ISGlobal/20220504_AtlasCode/FINAL_103_tryAtlasBartCode_emepV434_camsV42/1_results/code/'
#city_list_file = root + 'city_list_fua150_orig.txt'
city_list_file = root + 'city_list_fua150_orig.txt'

# INPUT configuration
# -------------------

# use aggregated areas (city, comm, national, international) or all areas
use_aggregated = True
if use_aggregated == True:
    area_aggregation_tag = 'aggAreas'
    agg_reduc_area_path = ''
else:
    area_aggregation_tag = 'allAreas' # for the 257 areas 

# read file with city_lats and city_lons
# cityname    nuts0    codeid    lat    lon
fcity = open(city_list_file, 'r')
fcity.readline()     # read header
city_dict = {}
while True:
    line = fcity.readline().rstrip()
    if len(line) == 0:
        break
    [cityname, lat, lon, codeid, country_code] = line.split(';')
    city_dict[cityname] = {'codeid': codeid, 'lat': float(lat), 'lon': float(lon), 'country_code': country_code}
n_cities = len(city_dict)


# which reductions to apply: all, perPrecursor, perSNAP, perSNAPandPrecursor
user_reduction_folder = root + 'reduction_input_files/'
# user_reduction_subfolder = 'allSNAP_allPrec'
# user_reduction_subfolder = 'allSNAP_perPrec'
# user_reduction_subfolder = 'perSNAP_allPrec'
user_reduction_subfolder = 'perGNFR_perPrec'

# list of snap sectors (reduction of all precursors together)
snap_tag = user_reduction_subfolder.split('_')[0]
precursor_tag = user_reduction_subfolder.split('_')[1]

user_reduction_list = os.listdir(user_reduction_folder + user_reduction_subfolder)

# read model information
model_file = root + 'run_configuration/model_file.txt'
fmod = open(model_file, 'r')
line = fmod.readline().rstrip()      # read header
model_dict = {}

while True:
    line = fmod.readline().rstrip()
    if len(line) == 0:
        break
    [model_name, ctm, pollutant, emission_cdf, concentration_cdf, source_receptor_cdf, cell_surface_cdf] = line.split('\t')
    model_dict[model_name] = {}
    model_dict[model_name]['ctm'] = ctm
    model_dict[model_name]['pollutant'] = pollutant
    model_dict[model_name]['emission_cdf'] = emission_cdf
    model_dict[model_name]['concentration_cdf'] = concentration_cdf
    model_dict[model_name]['source_receptor_cdf'] = source_receptor_cdf
    model_dict[model_name]['cell_surface_cdf'] = cell_surface_cdf
fmod.close()

print(model_dict)

# OUTPUT configuration
# --------------------

date_tag = date.today().strftime('%Y%m%d')
#results_path = root + 'results/%s_%s_%s_%s/' % (date_tag, snap_tag, precursor_tag, area_aggregation_tag)
#20210208EP change name dir , too long
results_path = root + 'results/%s/' % (date_tag)
if not(os.path.exists(results_path)):
    os.makedirs(results_path) 
    print('Results directory %s created.' % (results_path))   

results_file_format = '%s_%s_%s_%s_%s_%s.txt' # to be replaced with date_tag, model, pollutant, snap_tag, precursor_tag and area_aggregation_tag

# loop over all models
for model_name in model_dict.keys():
    
    # pollutant
    pollutant_tag = model_dict[model_name]['pollutant']
    # define the emission cdf
    path_emission_cdf = model_dict[model_name]['emission_cdf']
    # define base case concentration cdf
    path_base_conc_cdf = model_dict[model_name]['concentration_cdf']
    # define source receptor model cdf
    path_model_cdf = model_dict[model_name]['source_receptor_cdf']
    # cell surface netcdf
    path_cell_surface_cdf = model_dict[model_name]['cell_surface_cdf']
    
    # and the reduction areas
    reduc_area_agg_path = root + 'fua_area_cdfs/aggAreas_%s/' % (model_dict[model_name]['ctm'])
    reduc_area_all_path = root + 'fua_area_cdfs/allAreas_%s/' % (model_dict[model_name]['ctm'])

    # check if the output file already exists to resume a calculation
    completed_runs = []
    results_file_name = results_path + results_file_format % (date_tag, model_name, pollutant_tag, snap_tag, precursor_tag, area_aggregation_tag)
    if os.path.exists(results_file_name):
        
        # open the file in read only
        fallres = open(results_file_name, 'r')
        # read first 6 lines
        for i in range(6):
            line = fallres.readline().rstrip()
        while len(line) > 0:
            res_lst = line.split(';')
            target_city = res_lst[2]
            source_area = res_lst[3]
            snap = str(res_lst[4])
            precursor = str(res_lst[5])
            completed_runs.append((target_city, source_area, snap, precursor))
            line = fallres.readline().rstrip()
        fallres.close()
        
    else:
        # open a new file to store all results and write the header
        fallres = open(results_file_name, 'w')
        fallres.write('Source apportionment for %d cities\n' % (n_cities))
        fallres.write('commit BD handover version 23 March 2020\n')
        fallres.write('emissions cdf = %s\n' % (path_emission_cdf))
        fallres.write('concentrations cdf = %s\n' % (path_base_conc_cdf))
        fallres.write('model folder = %s\n' % (path_model_cdf))
        header_format = 11 * '%s;' + '%s\n' 
        fallres.write(header_format % ('model', 'pollutant', 'target', 'source', 'snap', 'precursor', 'potential',\
                                       'relative_potential', 'potency', 'target_conc_basecase', 'delta_conc', 'DE'))
        fallres.close()
        
    for target_city in city_dict.keys(): 

        # for the grouped snaps
        # path_reduction_txt = 'D:/SHERPA/FUA/user_reduction_snap_precursor/' + snap
                
        target_country = city_dict[target_city]['country_code']
        
        # make a dictionary of source areas, name as key, path as value
        source_area_dict = {}
        if use_aggregated == True:
            source_area_dict[target_city + '_City'] = reduc_area_all_path + target_city + '_City.nc'
            if not(target_city in ['Liverpool', 'Riga']):        # these 2 don't have a commuting zone..
                source_area_dict[target_city + '_Comm'] = reduc_area_all_path + target_city + '_Comm.nc'
            source_area_dict[target_city + '_National'] = reduc_area_agg_path + target_city + '_National.nc'
            source_area_dict[target_country + '_International'] = reduc_area_agg_path + target_country + '_International.nc'
        else:
            # get the list of areas from the content of a folder
            source_area_list = os.listdir(reduc_area_all_path)
            # remove extension '.nc' from area name
            for i in range(len(source_area_list)):
                source_area_dict[source_area_list[i].replace('.nc', '')] = reduc_area_all_path + source_area_list[i]
        
        for source_area in source_area_dict.keys():
            
            # retrieve source area type (the part after the underscore)
            source_area_type = source_area.split('_')[1]

            # loop over all combinations of snap, target cities and source areas 
            for user_reduction_file in user_reduction_list:
                # extract SNAP sector and precursor
                snap_prec = user_reduction_file.replace('user_reduction_GNFR', '')
                snap_prec = snap_prec.replace('.txt', '')
                snap = snap_prec.split('_')[0]
                precursor = snap_prec.split('_')[1] 
                
                # in case of NO2 only calculate for precursor NOx
                if pollutant_tag != 'NO2' or (pollutant_tag == 'NO2' and precursor == 'NOx'):
                
                    # check if the city, source_area, snap combination is already calculated
                    start = timeit.timeit()
                    run_tuple = (target_city, source_area, snap, precursor)
                    done_or_not_done = run_tuple in completed_runs
                    end = timeit.timeit()
                    print('Time to check if done = %fs' % (end - start))
    
                    if done_or_not_done:
                        print('Already calculated pollutant: %s, snap: %s, precursor: %s, target: %s, source: %s' % (pollutant_tag, snap, precursor, target_city, source_area))
                    else:
                        print('Calculating model: %s, pollutant: %s, snap: %s, precursor: %s, target: %s, source: %s' % (model_name, pollutant_tag, snap, precursor, target_city, source_area))
                        
                        # example file format: user_reduction_snap1.txt
                        path_reduction_txt = user_reduction_folder + user_reduction_subfolder + '/' + user_reduction_file
    
                        fua_area_cdf =  source_area_dict[source_area]
                        print(fua_area_cdf)
                        target_cell_lat = city_dict[target_city]['lat']
                        target_cell_lon = city_dict[target_city]['lon']
                        path_result_cdf = results_path + target_city + '/'
                        if not os.path.exists(path_result_cdf):
                            os.makedirs(path_result_cdf)
                        
                        # call module 6
                        m6_dict = module6(path_emission_cdf, fua_area_cdf, target_cell_lat, target_cell_lon, path_reduction_txt, path_base_conc_cdf, path_model_cdf, path_cell_surface_cdf, path_result_cdf)
                                            
                        # open the result dictionary and write results to one file
                        fallres = open(results_file_name, 'a')
                        for source_area_in_dict in m6_dict.keys():
                            res_area = m6_dict[source_area_in_dict]
                            for pollutant in m6_dict[source_area_in_dict].keys():
                                res_area_pol = res_area[pollutant]
                                line_format = 6 * '%s;' + 5 * '%e;' + '%e\n'
                                fallres.write(line_format % (model_name, pollutant, target_city, source_area, snap, precursor, res_area_pol['potential'],\
                                                             res_area_pol['relative_potential'], res_area_pol['potency'], res_area_pol['target_conc_basecase'], res_area_pol['delta_conc'], res_area_pol['DE']))
                        fallres.close()
                                            
                        # add to completed runs
                        completed_runs.append(run_tuple)
    
                        # delete nc output and rename potency output
                        os.rename(path_result_cdf + 'radius_result.txt', path_result_cdf + model_name + '_' + pollutant_tag + '_' + target_city + '_' + source_area + '_' + snap + '_' + precursor + '.txt' )
                        # os.remove(path_result_cdf)
               
            
    # close the results file    
    fallres.close()        
    
 

if __name__ == '__main__':
    pass