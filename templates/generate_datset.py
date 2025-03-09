import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate date range (e.g., one month of data)
date_range = pd.date_range(start="2025-01-01", end="2025-01-31", freq="H")

# Generate synthetic dataset
data = []
for timestamp in date_range:
    hour = timestamp.hour
    dayofweek = timestamp.dayofweek
    temperature = np.random.uniform(-5, 35)  # Random temperature between -5°C to 35°C
    station_id = np.random.randint(1, 6)  # 5 different charging stations
    base_demand = np.random.randint(5, 20)  # Base charging demand
    peak_adjustment = 10 if 17 <= hour <= 20 else 0  # Peak hours adjustment
    weekend_adjustment = -5 if dayofweek >= 5 else 0  # Lower demand on weekends
    
    charging_demand = max(0, base_demand + peak_adjustment + weekend_adjustment + np.random.randint(-3, 3))
    
    data.append([timestamp, hour, dayofweek, temperature, station_id, charging_demand])

# Convert to DataFrame
df = pd.DataFrame(data, columns=["timestamp", "hour", "dayofweek", "temperature", "station_id", "charging_demand"])

# Save to CSV
df.to_csv("ev_charging_data.csv", index=False)

print("Dataset saved as ev_charging_data.csv")
