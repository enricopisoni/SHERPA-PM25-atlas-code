rm(list=ls())

library(raster)
library(sf)
library(dplyr)
library(ncdf4)
library(tidyverse)

#load concentration basecase camsemep - use it as default grid
grid <- raster('input/sce0.nc')
values(grid) <- 0

#load shape nuts0
#for (lev in c('Lv0', 'Lv1', 'Lv2', 'Lv3')) {
for (lev in c('Lv3')) {
  print(lev)
  
  shpfil <- paste0('./shapes/fua/FUA_2013_WGS84_',lev,'.shp')
  shp <- st_read(shpfil)
  print(paste0('Loading ',shpfil))
  
  cities <- read_delim('input/city_list_fua150_orig.txt', delim=';')
  
  #loop shp -  process all geographical entities in the shp
  #r_out <- list()
  for (city in cities$cityname) {
    print(paste0('Processing ',lev, ' ',city))
    
    #city
    city_city <- paste0(city,'_city')
    shpTmpCity <- shp %>% filter(str_detect(NAME_ASCI, city_city))
    if (nrow(shpTmpCity)>0) {
      r_out_city <- rasterize(shpTmpCity, grid, getCover=TRUE)
      r_out_city <- r_out_city * 100
      nf <- paste0('output/allAreas/',city,'_City.nc')
      dimX <- ncdim_def( "longitude", "deg", unique(coordinates(grid)[,1]) )
      dimY <- ncdim_def( "latitude", "deg", sort(unique(coordinates(grid)[,2])))
      AREA <- ncvar_def('AREA', units="perc", list(dimX,dimY) )
      nc <- nc_create(nf, list(AREA) )
      ncvar_put(nc, AREA, values(flip(r_out_city,"y")) ) 
      nc_close(nc)  
      print(paste0('Processed city ',lev, ' ',city))
    }
    
    #comm
    city_city <- paste0(city,'_comm')
    shpTmpCity <- shp %>% filter(str_detect(NAME_ASCI, city_city))
      if (nrow(shpTmpCity)>0) {
      r_out_city <- rasterize(shpTmpCity, grid, getCover=TRUE)
      r_out_city <- r_out_city * 100
      nf <- paste0('output/allAreas/',city,'_Comm.nc')
      dimX <- ncdim_def( "longitude", "deg", unique(coordinates(grid)[,1]) )
      dimY <- ncdim_def( "latitude", "deg", sort(unique(coordinates(grid)[,2])))
      AREA <- ncvar_def('AREA', units="perc", list(dimX,dimY) )
      nc <- nc_create(nf, list(AREA) )
      ncvar_put(nc, AREA, values(flip(r_out_city,"y")) ) 
      nc_close(nc)  
      print(paste0('Processed comm ',lev, ' ',city))
    }
  }
}

