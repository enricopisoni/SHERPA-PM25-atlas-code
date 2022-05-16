rm(list=ls())

library(raster)
library(sf)
library(dplyr)
library(ncdf4)

#load concentration basecase camsemep - use it as default grid
grid <- raster('../../cell_surface_cdfs/sce0.nc')
values(grid) <- 0

#load shape nuts0
#for (lev in c('Lv0', 'Lv1', 'Lv2', 'Lv3')) {
for (lev in c('Lv3')) {
  print(lev)
  
  shpfil <- paste0('./shapes/fua/FUA_2013_WGS84_',lev,'.shp')
  shp <- st_read(shpfil)
  print(paste0('Loading ',shpfil))
  
  #loop shp -  process all geographical entities in the shp
  r_out <- list()
  for (cou in shp$NUTS_ID) {
    print(paste0('Processing ',lev, ' ',cou))
    shpTmp <- shp %>% filter(NUTS_ID == cou)
    r_out[cou] <- rasterize(shpTmp, grid, getCover=TRUE)
  }
  
  #create and export final stack
  nf <- paste0('./output/EMI_RED_ATLAS_FUA_',lev,'_EdgarEmep.nc')
  f_final <- brick(r_out) * 100
  #vecCou <-paste(as.vector(shp$NUTS_ID),collapse="-")
  
  #write final netcdf
  dimX <- ncdim_def( "longitude", "deg", unique(coordinates(grid)[,1]) )
  dimY <- ncdim_def( "latitude", "deg", sort(unique(coordinates(grid)[,2])))
  dimZ <- ncdim_def( "NUTS", "ID", 1:length(shp$NUTS_ID))
  
  AREA <- ncvar_def('AREA', units="perc", list(dimX,dimY,dimZ) )
  
  nc <- nc_create(nf, list(AREA) )
  
  ncvar_put(nc, AREA, values(flip(f_final,"y")) ) 
  ncatt_put( nc, 0, 'NUTS', paste(as.vector(shp$NUTS_ID),collapse="-"))
             
  nc_close(nc)  
  
  
  #writeRaster(f_final, nf, varname='AREA', zname='NUTS', zunit=vecCou,
   #           overwrite=TRUE)
  
}

