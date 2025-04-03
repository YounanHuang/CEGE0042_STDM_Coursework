library(spdep)
source("D:\\STDM\\code\\R_package\\Data\\starima_package.R")

# Read csv file, skip the first row
Wmat <- as.matrix(read.csv("D:\\STDM\\code\\data\\crime_data\\step3b_crime_adjacency_matrix_normalized.csv", header = TRUE))
Wmat <- as.matrix(Wmat)
head(Wmat)

# Read csv file, skip the first row
uk_temp_matrix <- as.matrix(read.csv("D:\\STDM\\code\\data\\crime_data\\step3c_crime_2011-2020_counts_by_grid_transferred.csv", header = TRUE))
# Delete the first column
uk_temp_matrix <- uk_temp_matrix[, -1]
uk_temp_matrix <- as.matrix(uk_temp_matrix)
head(uk_temp_matrix)

# Make sure all values are numeric
uk_temp_matrix <- apply(uk_temp_matrix, 2, as.numeric)
Wmat <- apply(Wmat, 2, as.numeric)

# Calculate STACF and STPACF
stacf(uk_temp_matrix, Wmat, 48)
stpacf(uk_temp_matrix, Wmat, 20)