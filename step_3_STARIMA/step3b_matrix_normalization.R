# Read adjacency matrix csv file
adj_matrix <- as.matrix(read.csv("D:\\STDM\\code\\data\\crime_data\\step3a_crime_adjacency_matrix.csv", header = TRUE))
adj_matrix <- as.matrix(adj_matrix)

# Normalization
row_sums <- rowSums(adj_matrix)
row_sums[row_sums == 0] <- 1
normalized_matrix <- sweep(adj_matrix, 1, row_sums, FUN = "/")

# Save normalized matrix as csv file
write.csv(normalized_matrix, "D:\\STDM\\code\\data\\crime_data\\step3b_crime_adjacency_matrix_normalized.csv", row.names = FALSE)
