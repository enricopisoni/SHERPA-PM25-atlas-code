## New branch 'atlas_01_005_deg'

A new branch has been created, to use the new SRR at 0.1x0.05. At the moment the code is configured to work with the usual 150 of the Atlas.

- '0_createReductionAreas': running here the 2 scripts, you can create all the combination of 'masks' (reductions at city, country level...) needed to run the Atlas py code
- '1_results': here now I included
    - '20220601_01_005': new files containing SRR, basecase emissions, basecase concentrations
    - 'cell_surface_cdfs': cell surface
    - 'fua_area_cdfs': to be updated with the new masks, to be created using the R code at '0_createReductionAreas'
    - 'pDUST-pSALT': dust and salt fields
    - 'reduction_input_files': containing all the 'text' reduction files
    - 'run_configuration': containing all the path to be used by the python code
    
## PM2.5 Atlas code

This repository contains the code to produce the results for the PM2.5 Atlas, 2021 version.

Basic steps:

* Create source allocation results:
  * 0_createReductionAreas: the code here can be used to create netcdf defining the reduction areas (city, commuting zone, country, international). 
    * The 'main_create_allAreas.R' code creates netcdf for city and commuting zones, 
    * The 'main_create_aggAreas.R' code creates national and international netcdf masks 
  * 1_results/code/python/atlas_run_em_all.py: it produces all anthropogenic results (please see .doc file with further explainations, in the '1_results' directory)
  * 1_results/code/pDUST-pSALT/get_salt_dust_in_fuas.R: it produces natural results
  * Then you need to merge the 2 files resulting from the 2 previous steps (i.e. see the created file 'results150fuas.xlsx')
* You need to copy 'results150fuas' in 2_createFiguresR/results150fuas.xlsx
* You run 2_createFiguresR R code to get graphs (this replaces the previous python code)

Additional notes on previous steps:
* SHERPA_PM25_Atlas/python/atlas_run_em_all.py
  * Use as input BaseEmissions[Mg/km2], BaseConcentrations, SRR, cellSurfaceCDF[km2], reductionTxtFiles, fuaArea.
  * Note on FuaAreas: values between 0 and 100:
    * CITY_Nationals (country at 100, without city)
    * COU_International (all at 100 without country)
    * CITY_City (city)
    * CITY_Comm (commuting zone without city)

* SHERPA_PM25_Atlas/pDUST-pSALT/get_salt_dust_in_fuas.R
  * Use as input the basecase, and a file containing natural PM (salt and dust in PM2.5)...
  * gives as output a file to be attached to the result of the 'atlas_run_em_all.py'

## Suggested steps for the work
1. Test the code to produce the current atlas results on 150 cities, at 0.1x0.1 deg
2. Adapt the code to work already on all required polygons 
3. Redo step 1 and 2 replacing the SRR with the new ones, i.e. using the 0.1x0.05 or 0.02x0.01 SRRs


