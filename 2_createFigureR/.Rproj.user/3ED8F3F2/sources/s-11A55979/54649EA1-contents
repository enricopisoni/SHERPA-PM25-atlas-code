library(tidyverse)
library(readxl)
rm(list=ls())

#load results of the step '1_results'...in inpyt use a final XLSX file containing results from
# a) 1_results/code/python/atlas_run_em_all.py: produces all anthropogenic results
# b) 1_results/code/pDUST-pSALT/get_salt_dust_in_fuas.R: produces natural results
df <- read_excel('results150fuas_composite_FINAL.xlsx', skip=5, 
                 col_types = c('text','text','text','text','text','text',
                               'numeric','numeric','numeric','numeric','numeric','numeric','numeric','numeric','numeric','numeric'))

#get full list of cities
cities <- unique(df$target)

#loop on cities
for (CITY in cities) {

#aggregate sectors, reorder sources and sectors
df2 <- df %>% 
  filter(target==CITY) %>%
  select(source, snap, relative_potential) %>%
  mutate(snap = fct_collapse(snap, industry = c('1','2'),
                             residential = c('3'),
                             agriculture = c('11','12'),
                             transport = c('6','9'),
                             shipping = c('7'),
                             other = c('4','5','8','10'),
                             natural = c('DUST','SALT'))) %>%
  mutate(snap = fct_relevel(snap, 'transport', 'industry', 'agriculture',
                            'residential', 'shipping', 'other', 'natural')) %>%
  mutate_if(str_detect(., 'City|Comm|National|International|Nature'), 
            ~str_replace_all(., c(".*City" = "City", ".*Comm" = "Commuting Zone",
                                  ".*National" = "Rest of country", ".*International" = "Transboundary",
                                  'Nature'='Natural'))) %>%
  mutate(source=as.factor(source)) %>%
  mutate(source = fct_relevel(source, 'City', 'Commuting Zone', 'Rest of country',
                            'Transboundary', 'Natural')) %>%
  group_by(source, snap) %>%
  summarize(RP=sum(relative_potential)) %>%
  ungroup() 

#RP to sum to 100, if higher than 100
if (sum(df2$RP)>100) {
  df2 <- df2 %>% 
    mutate(RP=RP/sum(RP)*100)
} 

#restructure dataframe for waterfall graph
df3 <- df2 %>%
  # \_Set the factor levels in the order you want ----
mutate(
  source = factor(source,
                      levels = unique(df2$source)),
  snap = factor(snap,
                   levels = unique(df2$snap))
) %>%
  # \_Sort by Group and Category ----
arrange(source, snap) %>%
  # \_Get the start and end points of the bars ----
mutate(end.Bar = cumsum(RP),
       start.Bar = c(0, head(end.Bar, -1))) %>%
  # \_Add a new Group called 'Total' with total by category ----
rbind(
  df2 %>%
    # \___Sum by Categories ----
  group_by(snap) %>% 
    summarise(RP = sum(RP)) %>%
    # \___Create new Group: 'Total' ----
  mutate(
    source = "Total",
    snap = factor(snap,
                     levels = unique(df2$snap))
  ) %>%
    # \___Sort by Group and Category ----
  arrange(source, snap) %>%
    # \___Get the start and end points of the bars ----
  mutate(end.Bar = cumsum(RP),
         start.Bar = c(0, head(end.Bar, -1))) %>%
    # \___Put variables in the same order ----
  select(source, snap, RP ,end.Bar,start.Bar)
) %>%
  # \_Get numeric index for the groups ----
mutate(group.id = group_indices(., source)) %>%
  # \_Create new variable with total by group ----
group_by(source) %>%
  mutate(total.by.x = sum(RP)) %>%
  # \_Order the columns ----
select(source, snap, group.id, start.Bar, RP, end.Bar, total.by.x)

#create graph
ggplot(df3, aes(x = source, fill = snap)) + 
  scale_fill_manual(values=c('red','yellow','green','blue','orange','violet','grey')) +
  # Waterfall Chart
  geom_rect(aes(x = source,
                xmin = group.id - 0.25, # control bar gap width
                xmax = group.id + 0.25, 
                ymin = end.Bar,
                ymax = start.Bar)
  ) +
  coord_flip() +
  ggtitle(CITY) +
  theme_bw() +
  ylim(0,100)
ggsave(paste0('output/',CITY,'.png'), width=10)
}