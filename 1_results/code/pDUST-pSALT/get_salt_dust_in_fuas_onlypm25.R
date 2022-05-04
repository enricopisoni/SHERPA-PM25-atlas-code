# ------------------------------------------------
# Look up Salt and Dust concentrations in the FUAs
# ------------------------------------------------

rm(list = ls())
library(raster)

wd <- "D:/WORK/projects/37_ISGlobal/20220504_AtlasCode/FINAL_103_tryAtlasBartCode_emepV434_camsV42/1_results/code/pDUST-pSALT/"
setwd(wd)

chimere.natural.pm.path <- "D:/WORK/projects/37_ISGlobal/20220504_AtlasCode/FINAL_103_tryAtlasBartCode_emepV434_camsV42/1_results/code/pDUST-pSALT/"
city.file <- "D:/WORK/projects/37_ISGlobal/20220504_AtlasCode/FINAL_103_tryAtlasBartCode_emepV434_camsV42/1_results/code/city_list_fua150_orig.txt"
city.df <- read.table(city.file, header = TRUE, sep = ';', quote = "")
# path to basecase concentrations
chimere.basecase.conc.path <- "D:/WORK/projects/37_ISGlobal/20220504_AtlasCode/FINAL_103_tryAtlasBartCode_emepV434_camsV42/1_results/code/20210325_SRR/2_base_concentrations/"

pm.type <- 'DUST'
pm.size <- '25'
res.df <- data.frame()
for (pm.size in c('25')) {
  
  # read file with basecase pm concentrations
  pm.base.file <- paste0(chimere.basecase.conc.path, "BCconc_emepV434_camsV42_SURF_ug_PM", pm.size, "_rh50.nc")
  pm.base.raster <- raster(pm.base.file)
  
  for (pm.type in c('SALT', 'DUST')) {
    
    # read the file with natural salt/dust concentrations
    pm.natural.file <- paste0(chimere.natural.pm.path, 'p', pm.type, '-', pm.size, '_emepV434_camsV42.nc')
    pm.natural.raster <- raster(pm.natural.file)

    # loop over all the cities
    # city <- "Sevilla"
    for (city in city.df$cityname) {
      
      # data frame with city coordinates
      city.coord <- city.df[city.df$cityname == city, c('lon', 'lat')]
      
      # get base case PM2.5/10 concentration
      pm.base <- extract(pm.base.raster, city.coord, method = 'simple')
      
      # get natural PM2.5/10 concentration
      pm.natural<- extract(pm.natural.raster, city.coord, method = 'simple')
      
      # add results to data.frame
      res.city.df <- data.frame(model = 'sherpa_camsV42',
                                pollutant = paste0('PM', pm.size),
                                target = city, 
                                source = 'Nature',
                                snap = pm.type,
                                precursor = 'PPM',
                                potential = pm.natural,
                                relative_potential = pm.natural / pm.base * 100,
                                potency = NA,
                                target_basecase_conc = pm.base,
                                delta_conc = pm.natural / 2,
                                DE = NA)
      res.df <- rbind(res.df, res.city.df)
    }
  }
}

# write table with results
write.table(res.df, 'emepV434_camsV42_Salt_Dust_FUA151.txt', sep = ';', row.names = FALSE, quote = FALSE)
