library(spdep)
library(dplyr)

# Read csv file
data <- read.csv("D:\\STDM\\code\\data\\crime_data\\step1e_crime_2011-2020_counts_by_grid.csv")
grids <- data %>% distinct(Grid_X, Grid_Y)

# Construct adjacency matrix
coords <- as.matrix(grids[, c("Grid_X", "Grid_Y")])
nb <- dnearneigh(coords, 0, 1.5, longlat = FALSE) 
adj_matrix <- nb2mat(nb, style = "B", zero.policy = TRUE)

# Save adjacency matrix as csv
write.csv(adj_matrix, "D:\\STDM\\code\\data\\crime_data\\step3a_crime_adjacency_matrix.csv", row.names = FALSE)

