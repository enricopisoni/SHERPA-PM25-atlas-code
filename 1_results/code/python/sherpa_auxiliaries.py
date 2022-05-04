'''
Created on Jul 14, 2015

auxiliary functions for SHERPA
@author: degraba
'''

from netCDF4 import Dataset
from numpy import zeros, power, sqrt, array


# create a dictionary with emission reductions per precursor and nuts
#--------------------------------------------------------------------

# file format:
# POLL    MS1    MS2    MS3    MS4    MS5    MS6    MS7    MS8    MS9    MS10
# NOx    0    0    0    0    0    100    0    0    0    0
# NMVOC    0    0    0    0    0    100    0    0    0    0
# NH3    0    0    0    0    0    100    0    0    0    0
# PM25    0    0    0    0    0    100    0    0    0    0
# SOx    0    0    0    0    0    100    0    0    0    0

def create_emission_reduction_dict(path_reduction_txt):
    # read emission reductions per precursor and macro sector
    f = open(path_reduction_txt, 'r')
    emission_reduction_dict = {}
    f.readline()
    while True:
        line = f.readline().rstrip()
        if len(line) == 0:
            break
        value_lst = line.split('\t')
        # sub dictionary per precursor
        precursor = value_lst[0]
        emission_reduction_dict[precursor] = {}
        for snap in range(1, 13):
            emission_reduction_dict[precursor][snap] = float(value_lst[snap]) / 100.0
    f.close()
    
    return emission_reduction_dict

# function making a list of the precursors that are reduced
def create_reduced_precursor_lst(emission_reduction_dict):
    reduced_precursor_lst = []
    for precursor in emission_reduction_dict.keys():
        sum_reductions = 0
        for snap in emission_reduction_dict[precursor].keys():
            sum_reductions += emission_reduction_dict[precursor][snap]
        if sum_reductions > 0:
            reduced_precursor_lst.append(precursor)
    return reduced_precursor_lst


# create a dictionary with emissions per precursor, macrosector and postion (lat, lon)
#-------------------------------------------------------------------------------------
def create_emission_dict(path_emission_cdf, precursor_lst):
    # open the emission netcdf
    rootgrp = Dataset(path_emission_cdf, 'r')
    
    emission_dict = {}
    emission_dict['units'] = {}
    for precursor in precursor_lst:
        emission_dict[precursor] = rootgrp.variables[precursor][:, :, :]
        emission_dict['units'][precursor] = rootgrp.variables[precursor].units
    
    # get snap, longitude and latitude arrays from emission file
    snap_array = range(1, 13)
    lon_array = rootgrp.variables['longitude'][:]
    lat_array = rootgrp.variables['latitude'][:]
    emission_dict['Nsnaps'] = snap_array
    emission_dict['lon_array'] = lon_array
    emission_dict['lat_array'] = lat_array
    
    # close the emission file
    rootgrp.close()
    
    return emission_dict


# make a window with cell distances to the central cell
# -----------------------------------------------------
def create_window(radius):
    # the window contains the distance between each cell and the centre of the window
    # the distance is expressed in cells
    n_lon_win = 2 * radius + 1
    n_lat_win = 2 * radius + 1
     
    window = zeros((n_lat_win, n_lon_win))
    i_centre = radius  
    j_centre = radius  
    for iw in range(n_lon_win):
        for jw in range(n_lon_win):
            cell_dist = sqrt((float(iw - i_centre)) ** 2 + (float(jw - j_centre)) ** 2) 
            window[iw, jw] = 1 / (1 + cell_dist) 
     
    return window

# convert to progress log file to a dictionary
def read_progress_log(progresslog):
    progress_dict = {}
    f_prog = open(progresslog, 'r')
    line = f_prog.readline().rstrip()
    [start, divisor] = line.split('\t')
    progress_dict['start'] = float(start)
    progress_dict['divisor'] = float(divisor) 
    progress_dict['netcdf_output'] = False 

    return progress_dict

# write progress log file
def write_progress_log(progress_log_filename, start, divisor):
    # write progress log file
    f_prog = open(progress_log_filename, 'w')
    f_prog.write('%f\t%f' % (start, divisor))
    f_prog.close()

# define a function that applies the NO2 fraction correlation
def fno2_corr(nox_array):
    # this is the correlation used in GRAL
    fno2_array = 30 / (nox_array + 35) + 0.18
    return fno2_array


# function that converts a delta_conc(NOx) into a delta_conc(NO2)
def deltaNOx_to_deltaNO2(delta_conc_nox, base_conc_nox, base_conc_no2):
    # read the NO2 concentration (should be inside the NO2eq/NOx file)
    base_fno2 = base_conc_no2 / base_conc_nox 
    base_fno2_rel_error = fno2_corr(base_conc_nox) / base_fno2
    
    # calculate NO2 fraction and the absolute NO2 concentration
    # delta_conc = -(scen_conc_nox - base_conc_nox)
    scen_conc_nox = base_conc_nox - delta_conc_nox
    # the NO2 fraction given by the correlation has to be corrected with the NO2 fraction of each cell
    # from the baseline scenario. Otherwise delta_NO2's will be created when the NO2 fraction is different for the 
    # correlation and the basecase model results.
    scen_fno2 = array(fno2_corr(scen_conc_nox) / base_fno2_rel_error)
    # correlation can lead to NO2 fractions above 1, avoid this
    scen_fno2[scen_fno2 > 1] = 1
    scen_conc_no2 = scen_conc_nox * scen_fno2
    # recalculate delta_conc
    delta_conc_no2 = base_conc_no2 - scen_conc_no2
    
#     # add diagnostic variables in the case of NOx
#     delta_conc_nox_var = rootgrp.createVariable('delta_conc_nox', 'f4', ('latitude', 'longitude',))
#     delta_conc_nox_var.units = 'ug/m3'
#     delta_conc_nox_var[:] = delta_conc_nox
    
    return delta_conc_no2

    
if __name__ == '__main__':
    
    # check the window function
    radius = 200
    testwindow = create_window(radius)
    window_file = open('C:/temp/source_recptor_window.txt', 'w')
    for i in range(2 * radius + 1):
        for j in range(2 * radius + 1):
            window_file.write('%e\t' % testwindow[i,j])
        window_file.write('\n')
    window_file.close()
    pass


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    