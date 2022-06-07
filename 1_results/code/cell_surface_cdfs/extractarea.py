# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 16:02:16 2022

@author: pisonen
"""
import xarray as xr

nc = xr.open_dataset('sce0.nc')

ncArea = nc['Area_Grid_km2']

ncArea.to_netcdf('sce0_Area_Grid_km2.nc')
    