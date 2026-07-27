import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/Shipping_Analysis_Final.csv")

# Convert dates to datetime format
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Create Shipping Lead Time
df["Shipping Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# Remove negative lead times (if any)
df = df[df["Shipping Lead Time"] >= 0]

# Remove duplicate rows
df = df.drop_duplicates()

# Check missing values
print("Missing Values:")
print(df.isnull().sum())

# Save cleaned dataset
df.to_csv("data/processed/cleaned_shipping_data.csv", index=False)

print("\n✅ Data cleaning completed successfully!")
print(f"Final Dataset Shape: {df.shape}")