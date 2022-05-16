rm(list=ls())

library(raster)
library(sf)
library(dplyr)
library(ncdf4)
setwd('D:/WORK/projects/1_urbIam/1_CODE_MATLAB/SHERPA/PYTHON-SHERPA-CODE/SHERPA-GIT-CITNET-simulationCode/input_EDGAR_EMEP/createRedArea')

#select here which country to reduce
# SelectedEntity <- 'France'
# shpfil <- paste0('./shapes/fua/FUA_2013_WGS84_Lv0.shp') #for country
SelectedEntity <- 'London_FUA'
shpfil <- paste0('./shapes/fua/FUA_2013_WGS84_Lv2.shp') #for city

#load concentration basecase camsemep - use it as default grid
grid <- raster('../createBCemiGNFR/input/emiss/sce0.nc', varname='SOMO35')
values(grid) <- 0

#load shape fua
shp <- st_read(shpfil)
print(paste0('Loading ',shpfil))

#loop shp -  process all geographical entities in the shp
r_out <- list()
for (city in shp$NAME_ASCI) {
  print(city)
  if (city == SelectedEntity) {
    print(paste0('Processing ',city))
    shpTmp <- shp %>% filter(NAME_ASCI == city)
    r_out[city] <- rasterize(shpTmp, grid, getCover=TRUE)
  }
}

#create and export final stack
nf <- paste0('./output/emiRedOn_',SelectedEntity,'.nc')
f_final <- brick(r_out)*100

#write final netcdf
dimX <- ncdim_def( "longitude", "deg", unique(coordinates(grid)[,1]) )
dimY <- ncdim_def( "latitude", "deg", sort(unique(coordinates(grid)[,2])))
AREA <- ncvar_def('AREA', units="perc", list(dimX,dimY) )

nc <- nc_create(nf, list(AREA) )
ncvar_put(nc, AREA, values(flip(f_final,"y")) ) 

nc_close(nc)  

#writeRaster(f_final, nf, varname='AREA', zname='NUTS',overwrite=TRUE)
  


