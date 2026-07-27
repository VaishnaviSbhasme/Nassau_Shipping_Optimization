import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from datetime import datetime
# -------------------------------
# Import custom modules
# -------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.ship_mode_analysis import ship_mode_chart

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Nassau Shipping Optimization Dashboard",
    page_icon="🚚",
    layout="wide"
)

# -------------------------------
# Load Dataset
# -------------------------------
df = pd.read_csv("data/processed/final_shipping_dataset.csv")

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.title("📊 Dashboard Controls")

st.sidebar.markdown(
    "Use the filters below to analyse shipment performance."
)

st.sidebar.markdown("---")

selected_region = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

selected_division = st.sidebar.multiselect(
    "Division",
    options=sorted(df["Division"].unique()),
    default=sorted(df["Division"].unique())
)

selected_shipmode = st.sidebar.multiselect(
    "Ship Mode",
    options=sorted(df["Ship Mode"].unique()),
    default=sorted(df["Ship Mode"].unique())
)

df = df[
    (df["Region"].isin(selected_region)) &
    (df["Division"].isin(selected_division)) &
    (df["Ship Mode"].isin(selected_shipmode))
]

# ============================================================
# Product Search
# ============================================================

search_product = st.sidebar.text_input(
    "🔎 Search Product Name"
)

if search_product:
    df = df[
        df["Product Name"]
        .str.contains(search_product, case=False, na=False)
    ]

# ============================================================
# Download Filtered Data
# ============================================================

csv = df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_shipping_data.csv",
    mime="text/csv"
)

# -------------------------------
# Date Conversion
# -------------------------------
df["Order Date"] = pd.to_datetime(df["Order Date"])

# -------------------------------
# KPI Calculations
# -------------------------------
total_shipments = len(df)
total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
average_lead_time = df["Shipping Lead Time"].mean()

# -------------------------------
# Dashboard Header
# -------------------------------
st.title("🚚 Nassau Candy Distributor")
st.subheader("Shipping Route Optimization Dashboard")
st.markdown(
    """
    **Logistics & Sales Performance Analysis**

    Analyse shipments, sales, profitability, shipping efficiency,
    factory performance and delivery delays using interactive filters.
    """
)
st.caption(
    f"Last Updated: {datetime.now().strftime('%d %B %Y %I:%M %p')}"
)
st.markdown("""
Welcome to the **Nassau Candy Distributor Shipping Dashboard**.

This dashboard provides real-time insights into:

- 📦 Shipment Performance
- 🌍 Regional Sales
- 💰 Gross Profit
- 🚚 Shipping Efficiency
- 🏭 Factory Operations
- 📈 Business Performance

Use the filters on the left to interact with the dashboard.
""")

st.markdown("---")

# -------------------------------
# KPI Cards
# -------------------------------
k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Total Shipments",
    f"{total_shipments:,}"
)

k2.metric(
    "Total Sales",
    f"${total_sales:,.2f}"
)

k3.metric(
    "Gross Profit",
    f"${total_profit:,.2f}"
)

k4.metric(
    "Average Lead Time",
    f"{average_lead_time:.2f} Days"
)
st.success(f"Showing **{len(df)}** filtered records.")
st.info(
    f"""
### Current Filters

📍 Region: {', '.join(selected_region)}

🏢 Division: {', '.join(selected_division)}

🚚 Ship Mode: {', '.join(selected_shipmode)}
"""
)
# ============================================================
# Dashboard Highlights
# ============================================================

colA, colB, colC = st.columns(3)

best_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

best_division = (
    df.groupby("Division")["Gross Profit"]
    .sum()
    .idxmax()
)

fastest_mode = (
    df.groupby("Ship Mode")["Shipping Lead Time"]
    .mean()
    .idxmin()
)

with colA:
    st.success(f"🏆 Best Sales Region\n\n**{best_region}**")

with colB:
    st.success(f"💰 Highest Profit Division\n\n**{best_division}**")

with colC:
    st.success(f"🚚 Fastest Ship Mode\n\n**{fastest_mode}**")
st.markdown("---")

# ============================================================
# Create All Figures First
# ============================================================

# -------------------------------
# Sales by Region
# -------------------------------
sales_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    sales_region,
    x="Region",
    y="Sales",
    color="Region",
    title="Sales by Region"
)

# -------------------------------
# Ship Mode Distribution
# -------------------------------
fig2 = ship_mode_chart(df)

# -------------------------------
# Monthly Sales Trend
# -------------------------------
df["Month"] = df["Order Date"].dt.strftime("%b")

month_order = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

monthly_sales = (
    df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Month"] = pd.Categorical(
    monthly_sales["Month"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month")

fig3 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

# -------------------------------
# Gross Profit by Division
# -------------------------------
division_profit = (
    df.groupby("Division")["Gross Profit"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    division_profit,
    x="Division",
    y="Gross Profit",
    color="Division",
    title="Gross Profit by Division"
)

# -------------------------------
# Route Efficiency Score
# -------------------------------
route = (
    df.groupby("Region")["Route Efficiency Score"]
    .mean()
    .reset_index()
)

fig5 = px.bar(
    route,
    x="Region",
    y="Route Efficiency Score",
    color="Region",
    title="Average Route Efficiency Score"
)

# -------------------------------
# Delayed Shipments Analysis
# -------------------------------
delay = (
    df.groupby("Delayed")
    .size()
    .reset_index(name="Shipments")
)

fig6 = px.pie(
    delay,
    names="Delayed",
    values="Shipments",
    hole=0.45,
    title="Delayed vs On-Time Shipments"
)

# -------------------------------
# Factory-wise Shipments
# -------------------------------
factory_shipments = (
    df.groupby("Factory")
    .size()
    .reset_index(name="Shipments")
)

fig7 = px.bar(
    factory_shipments,
    x="Factory",
    y="Shipments",
    color="Factory",
    title="Factory-wise Shipments"
)

# -------------------------------
# Average Shipping Lead Time
# -------------------------------
lead_time = (
    df.groupby("Ship Mode")["Shipping Lead Time"]
    .mean()
    .reset_index()
)

fig8 = px.bar(
    lead_time,
    x="Ship Mode",
    y="Shipping Lead Time",
    color="Ship Mode",
    title="Average Shipping Lead Time"
)

# ============================================================
# DASHBOARD LAYOUT
# ============================================================

st.markdown("---")
st.header("📊 Dashboard Insights")

# -------------------------------
# Row 1
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# Row 2
# -------------------------------
col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# Row 3
# -------------------------------
col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.plotly_chart(fig6, use_container_width=True)

# -------------------------------
# Row 4
# -------------------------------
col7, col8 = st.columns(2)

with col7:
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    st.plotly_chart(fig8, use_container_width=True)

    # ============================================================
# Top 10 Products by Sales
# ============================================================

st.markdown("---")
st.header("🏆 Top 10 Products by Sales")

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig9 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    title="Top 10 Products by Sales"
)

st.plotly_chart(fig9, use_container_width=True)

# ============================================================
# Top 10 Products by Gross Profit
# ============================================================

st.markdown("---")
st.header("💰 Top 10 Products by Gross Profit")

top_profit = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig10 = px.bar(
    top_profit,
    x="Gross Profit",
    y="Product Name",
    orientation="h",
    color="Gross Profit",
    title="Top 10 Products by Gross Profit"
)

st.plotly_chart(fig10, use_container_width=True)

# ============================================================
# Factory Locations Map
# ============================================================

st.markdown("---")
st.header("🗺️ Factory Locations")

factory_map = (
    df[
        ["Factory", "Factory Latitude", "Factory Longitude"]
    ]
    .drop_duplicates()
)

fig11 = px.scatter_map(
    factory_map,
    lat="Factory Latitude",
    lon="Factory Longitude",
    hover_name="Factory",
    zoom=3,
    height=500,
    title="Factory Locations"
)

st.plotly_chart(fig11, use_container_width=True)

# ============================================================
# Business Insights
# ============================================================

st.markdown("---")
st.header("📌 Business Insights")

highest_sales_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

highest_profit_division = (
    df.groupby("Division")["Gross Profit"]
    .sum()
    .idxmax()
)

best_ship_mode = (
    df.groupby("Ship Mode")["Shipping Lead Time"]
    .mean()
    .idxmin()
)

delay_percentage = (
    df["Delayed"].sum() / len(df)
) * 100

st.success(f"🏆 Highest Sales Region: {highest_sales_region}")

st.success(f"💰 Highest Profit Division: {highest_profit_division}")

st.success(f"🚚 Fastest Ship Mode: {best_ship_mode}")

st.warning(f"⏳ Delay Percentage: {delay_percentage:.2f}%")

# ============================================================
# Executive Summary
# ============================================================

st.markdown("---")
st.header("📈 Executive Summary")

col1, col2 = st.columns(2)

with col1:
    st.info(f"""
### 📊 Sales Overview

- Total Shipments: **{total_shipments:,}**
- Total Sales: **${total_sales:,.2f}**
- Gross Profit: **${total_profit:,.2f}**
- Average Lead Time: **{average_lead_time:.2f} Days**
""")

with col2:
    st.info(f"""
### 🚚 Operational Overview

- Best Sales Region: **{highest_sales_region}**
- Best Profit Division: **{highest_profit_division}**
- Fastest Ship Mode: **{best_ship_mode}**
- Delay Percentage: **{delay_percentage:.2f}%**
""")
# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🚚 Nassau Candy Distributor Logistics Dashboard | "
    "Built using Python, Streamlit, Pandas and Plotly"
)