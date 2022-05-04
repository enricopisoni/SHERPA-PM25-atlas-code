## PM2.5 Atlas code

This repository contains the code to produce the results for the PM2.5 Atlas, 2021 version.

Basic steps
1. 1_results/code/python/atlas_run_em_all.py: it produces all anthropogenic results (please see .doc file with further explainations, in the '1_results' directory)
2. 1_results/code/pDUST-pSALT/get_salt_dust_in_fuas.R: it produces natural results
3. Need to merge the 2 files resulting from the 2 previous steps (i.e. see the created file 'results150fuas.xlsx')
4. Need to copy 'results150fuas' in 2_createFiguresR/results150fuas.xlsx
5. run 2_createFiguresR R code to get graphs (this replaces the previous python code)

Additional notes on previous steps:
1. SHERPA_PM25_Atlas/python/atlas_run_em_all.py
  * Use as input BaseEmissions[Mg/km2], BaseConcentrations, SRR, cellSurfaceCDF[km2], reductionTxtFiles, fuaArea.
  * Note on FuaAreas: values between 0 and 100:
    * CITY_Nationals (country at 100, without city)
    * COU_International (all at 100 without country)
    * CITY_City (city)
    * CITY_Comm (commuting zone without city)

2. SHERPA_PM25_Atlas/pDUST-pSALT/get_salt_dust_in_fuas.R
  * Use as input the basecase, and a file containing natural PM (salt and dust in PM2.5)...
  * gives as output a file to be attached to the result of the 'atlas_run_em_all.py'

## Suggested steps for the work
1. Test the code to produce the current atlas results on 150 cities, at 0.1x0.1 deg
2. Adapt the code to work already on all required polygons 
3. Redo step 1 and 2 replacing the SRR with the new ones, i.e. using the 0.1x0.05 or 0.02x0.01 SRRs


