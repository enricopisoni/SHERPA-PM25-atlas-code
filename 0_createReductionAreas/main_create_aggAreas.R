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
  for (item in 1:nrow(cities)) {
    print(paste0('Processing ',lev, ' ',cities$cityname[[item]]))
    
    #country
    cou <- paste0(cities$country[[item]])
    shpfilLv0 <- paste0('./shapes/fua/FUA_2013_WGS84_Lv0.shp')
    shpLv0 <- st_read(shpfilLv0)
    shpTmpCou <- shpLv0 %>% filter(str_detect(NUTS_Lv0, cou))
    if (nrow(shpTmpCou)>0) {
      r_out_cou <- rasterize(shpTmpCou, grid, getCover=TRUE)
      r_out_cou <- r_out_cou * 100
    }
    
    #international file
    international <- r_out_cou
    values(international) <- 100
    international <- international - r_out_cou
    #save result
    nf <- paste0('output/aggAreas/',cou,'_International.nc')
    if (file.exists(nf)==0) {
      dimX <- ncdim_def( "longitude", "deg", unique(coordinates(grid)[,1]) )
      dimY <- ncdim_def( "latitude", "deg", sort(unique(coordinates(grid)[,2])))
      AREA <- ncvar_def('AREA', units="perc", list(dimX,dimY) )
      nc <- nc_create(nf, list(AREA) )
      ncvar_put(nc, AREA, values(flip(international,"y")) ) 
      nc_close(nc)  
      print(paste0('Processed International ',cou))
    }
    
    #city
    city_city <- paste0(cities$cityname[[item]],'_city')
    shpTmpCity <- shp %>% filter(str_detect(NAME_ASCI, city_city))
    if (nrow(shpTmpCity)>0) {
      r_out_city <- rasterize(shpTmpCity, grid, getCover=TRUE)
      r_out_city1 <- r_out_city * 100
      r_out_cou <- r_out_cou - r_out_city1  
    }
    
    #comm
    city_city <- paste0(cities$cityname[[item]],'_comm')
    shpTmpCity <- shp %>% filter(str_detect(NAME_ASCI, city_city))
    if (nrow(shpTmpCity)>0) {
      r_out_city <- rasterize(shpTmpCity, grid, getCover=TRUE)
      r_out_city2 <- r_out_city * 100
      r_out_cou <- r_out_cou - r_out_city2  
    }
    
    #national file
    nf <- paste0('output/aggAreas/',cities$cityname[[item]],'_National.nc')
    dimX <- ncdim_def( "longitude", "deg", unique(coordinates(grid)[,1]) )
    dimY <- ncdim_def( "latitude", "deg", sort(unique(coordinates(grid)[,2])))
    AREA <- ncvar_def('AREA', units="perc", list(dimX,dimY) )
    nc <- nc_create(nf, list(AREA) )
    ncvar_put(nc, AREA, values(flip(r_out_cou,"y")) ) 
    nc_close(nc)  
    print(paste0('Processed national ',cities$cityname[[item]]))
    
  }
}

