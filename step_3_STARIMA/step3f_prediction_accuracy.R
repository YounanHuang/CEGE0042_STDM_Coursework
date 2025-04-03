library(readxl)
library(readr)
library(dplyr)
library(Metrics)
library(writexl)

# Load predicted data
predicted_df <- read_xlsx("D:\\STDM\\code\\data\\crime_data\\step3e_STARIMA_crime_predict.xlsx")

# Load actual data
actual_df <- read_csv("D:\\STDM\\code\\data\\crime_data\\step3c_crime_2021-2023_counts_by_grid_transferred.csv")

# Ensure Date format is consistent
predicted_df$Date <- as.Date(paste0(predicted_df$Date, "-01"), format = "%Y-%m-%d")
actual_df$Date <- as.Date(paste0(actual_df$Date, "-01"), format = "%Y-%m-%d")

# Ensure both datasets have the same time range
actual_df <- actual_df %>% filter(Date %in% predicted_df$Date)

# Remove Date column before calculation
pred_values <- predicted_df %>% select(-Date)
actual_values <- actual_df %>% select(-Date)

common_cols <- intersect(colnames(pred_values), colnames(actual_values))
pred_values <- pred_values[, common_cols, drop = FALSE]
actual_values <- actual_values[, common_cols, drop = FALSE]

# ---------------------------
# Calculate overall acuracy
# ---------------------------

# 展平所有数据为向量
all_pred <- unlist(pred_values)
all_actual <- unlist(actual_values)

# Calculate overall acuracy
overall_mse <- mean((all_pred - all_actual)^2, na.rm = TRUE)
overall_rmse <- sqrt(overall_mse)
overall_mape <- mean(abs((all_pred - all_actual)/all_actual) * 100, na.rm = TRUE)

# ---------------------------
# Calculate acuracy regionally
# ---------------------------
mse_values <- colMeans((pred_values - actual_values)^2, na.rm = TRUE)
rmse_values <- sqrt(mse_values)
mape_values <- colMeans(abs((pred_values - actual_values)/actual_values) * 100, na.rm = TRUE)

# Combine results
error_metrics_df <- data.frame(
  Region = c(colnames(pred_values), "Overall"),
  MSE = c(mse_values, overall_mse),
  RMSE = c(rmse_values, overall_rmse),
  MAPE = c(mape_values, overall_mape)
)

# Save error metrics to Excel
error_metrics_path <- "D:\\STDM\\code\\data\\crime_data\\step3f_STARIMA_error_metrics.xlsx"
write_xlsx(error_metrics_df, path = error_metrics_path)
