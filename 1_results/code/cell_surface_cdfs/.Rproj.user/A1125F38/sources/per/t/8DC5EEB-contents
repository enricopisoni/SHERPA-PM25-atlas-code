rm(list=ls())

library(raster)
library(ncdf4)

polvec <- c('Area_Grid_km2')

for (pol in polvec) {
  polr <- raster('./sce0.nc', varname = pol)
  unit <- polr@data@unit
  print(paste(pol, unit))
  names(polr) <- 'surface'
  
  dimX <- ncdim_def( "longitude", "deg", unique(coordinates(polr)[,1]) )
  dimY <- ncdim_def( "latitude", "deg", sort(unique(coordinates(polr)[,2])))
  CONC <- ncvar_def('surface', units=unit, list(dimX,dimY) )
  nf <- './edgaremep_cell_surface.nc'
  nc <- nc_create(nf, list(CONC) )
  ncvar_put(nc, CONC, values(flip(polr,"y")) ) 
  
  nc_close(nc)  
}


