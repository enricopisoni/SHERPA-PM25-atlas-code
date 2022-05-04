20220504
code and infos at:
https://github.com/enricopisoni/SHERPA-PM25-atlas-code

20201013
I redid all the process using the SHERPA CHIMERE SRR, used for 2015 atlas:
a) 1_results/code/python/atlas_run_em_all.py: produces all anthropogenic results
b) 1_results/code/pDUST-pSALT/get_salt_dust_in_fuas.R: produces natural results
c) I merge the 2 files resulting from the previous step ('results150fuas')
d) I copy 'results150fuas' in 2_createFigures/atlas2/results150fuas.xlsx
e) I run 2_createFiguresR code to get graphs (this replaces the previous python code)

***

a) SHERPA_PM25_Atlas/python/atlas_run_em_all.py
Use as input BaseEmissions[Mg/km2], BaseConcentrations, SRR, cellSurfaceCDF[km2], reductionTxtFiles, fuaArea.
Note on FuaAreas: values between 0 and 100:
*CITY_Nationals (country at 100, without city)
*COU_International (all at 100 without country)
*CITY_City (city)
*CITY_Comm (commuting zone without city)

b) SHERPA_PM25_Atlas/pDUST-pSALT/get_salt_dust_in_fuas.R
Use as input the basecase, and a file containing natural PM (salt and dust in PM2.5)....gives as output to be attached to the result of the 'atlas_run_em_all.py'
***

