library(raster)

rss <- raster('../cell_surface_cdfs/sce0.nc', varname='SURF_ug_SEASALT_F')

rd1 <- raster('../cell_surface_cdfs/sce0.nc', varname='SURF_ug_DUST_NAT_F')
rd2 <- raster('../cell_surface_cdfs/sce0.nc', varname='SURF_ug_DUST_SAH_F')
rd3 <- raster('../cell_surface_cdfs/sce0.nc', varname='SURF_ug_DUST_WB_F')
rdd <- rd1+rd2+rd3

names(rss) <- 'pSALT-25'
writeRaster(rss, 'pSALT-25_emepV434_camsV42_01_005.nc')

names(rdd) <- 'pDUST-25'
writeRaster(rdd, 'pDUST-25_emepV434_camsV42_01_005.nc')
