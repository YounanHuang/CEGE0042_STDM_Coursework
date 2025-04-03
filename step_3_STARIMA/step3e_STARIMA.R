source("D:\\STDM\\code\\R_package\\Data\\starima_package.R")
library(spdep)
library(writexl)

# Read adjacency matrix
Wmat <- as.matrix(read.csv("D:\\STDM\\code\\data\\crime_data\\step3b_crime_adjacency_matrix_normalized.csv", header = TRUE))
Wmat <- apply(Wmat, 2, as.numeric)

# Read crime count matrix and remove the first column
uk_temp_matrix <- as.matrix(read.csv("D:\\STDM\\code\\data\\crime_data\\step3c_crime_2011-2020_counts_by_grid_transferred.csv", header = TRUE))
uk_temp_matrix <- uk_temp_matrix[, -1]
uk_temp_matrix <- apply(uk_temp_matrix, 2, as.numeric)

# Set STARIMA parameters
p <- 4
q <- 18
d <- 12  

# Train STARIMA model
starima_model <- starima_fit(Z = uk_temp_matrix, W = list(w1 = Wmat), p = p, d = d, q = q)

# ========== Monthly Forecast ========== 
forecast_start <- as.Date("2021-01-01")  # Start date
forecast_end   <- as.Date("2023-12-01")  # End date
n_forecast <- length(seq.Date(from = forecast_start, to = forecast_end, by = "month"))  # Number of months

# Construct initial conditions for forecasting
offset <- p + q  # Required historical data length
init_future <- rbind(uk_temp_matrix[(nrow(uk_temp_matrix) - offset + 1):nrow(uk_temp_matrix), ], 
                     matrix(rep(uk_temp_matrix[nrow(uk_temp_matrix), ], times = n_forecast), 
                            nrow = n_forecast, byrow = TRUE))

# Forecast future data
pre.star_future <- starima_pre(init_future, model = starima_model)

# Extract predicted values
predicted_future <- pre.star_future$PRE
predicted_future <- predicted_future[(nrow(predicted_future) - n_forecast + 1):nrow(predicted_future), ]

# Generate monthly forecast date sequence
forecast_dates <- seq.Date(from = forecast_start, to = forecast_end, by = "month")

# Construct future prediction DataFrame
future_pred_df <- as.data.frame(predicted_future)
colnames(future_pred_df) <- colnames(uk_temp_matrix)  # Keep column names consistent
future_pred_df <- cbind(Date = forecast_dates, future_pred_df)

# ========== Save Forecast Results ========== 
output_excel_path <- "D:\\STDM\\code\\data\\crime_data\\step3e_STARIMA_crime_predict.xlsx"
write_xlsx(future_pred_df, path = output_excel_path)

cat("STARIMA prediction already saved as:", output_excel_path, "\n")