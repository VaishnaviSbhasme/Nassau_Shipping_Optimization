import pandas as pd

# Load the dataset
df = pd.read_csv("data/raw/Shipping_Analysis_Final.csv")

# Display first 5 rows
print(df.head())

# Display dataset information
print("\nDataset Information:")
print(df.info())

# Display number of rows and columns
print("\nDataset Shape:")
print(df.shape)
