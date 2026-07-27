import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_shipping_data.csv")

# Product → Factory Mapping
factory_mapping = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory"
}

# Factory Coordinates
factory_coordinates = {
    "Lot's O' Nuts": (32.881893, -111.768036),
    "Wicked Choccy's": (32.076176, -81.088371),
    "Sugar Shack": (48.119140, -96.181150),
    "Secret Factory": (41.446333, -90.565487),
    "The Other Factory": (35.117500, -89.971107)
}

# Assign Factory
df["Factory"] = df["Product Name"].map(factory_mapping)

# Assign Latitude & Longitude
df["Factory Latitude"] = df["Factory"].map(
    lambda x: factory_coordinates[x][0]
)

df["Factory Longitude"] = df["Factory"].map(
    lambda x: factory_coordinates[x][1]
)

# Create Routes
df["Factory → State"] = df["Factory"] + " → " + df["State/Province"]

df["Factory → Region"] = df["Factory"] + " → " + df["Region"]

# Route Efficiency Score
max_lead = df["Shipping Lead Time"].max()

df["Route Efficiency Score"] = (
    (max_lead - df["Shipping Lead Time"])
    / max_lead
    * 100
).round(2)

# Save dataset
df.to_csv(
    "data/processed/final_shipping_dataset.csv",
    index=False
)

print("✅ Feature Engineering Completed Successfully!")
print(df.head())