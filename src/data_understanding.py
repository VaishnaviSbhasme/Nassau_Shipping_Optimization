import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/Shipping_Analysis_Final.csv")

# Display column names
print("\n📌 Columns in the dataset:")
print(df.columns.tolist())

# Check missing values
print("\n📌 Missing Values:")
print(df.isnull().sum())

# Check duplicate rows
print("\n📌 Duplicate Rows:")
print(df.duplicated().sum())

# Summary statistics
print("\n📌 Summary Statistics:")
print(df.describe())