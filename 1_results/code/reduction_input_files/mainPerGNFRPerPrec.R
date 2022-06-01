library(tidyverse)
rm(list=ls())

df1 <- data.frame('POLL'=c('NOx','NMVOC','NH3','PPM25','SOx'))
df2 <- matrix(rep(0,5*13), nrow=5, ncol=13)

df <- cbind(df1,df2)
colnames(df) <- c('POLL', paste0('GNFR', 1:13))

for (i in 1:5) {
  for (j in 1:13) {
    newdf <- df
    newdf[i,j+1]<- 50
    nf <- paste0('./perGNFR_perPrec/user_reduction_', names(df)[j+1], '_', df$POLL[i], '.txt')
    write_tsv(newdf, nf)    
  }
}



